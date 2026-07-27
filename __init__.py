# Filtered Deck From Tag (Multi-tags Interactif avec Sélection Multiple)
#
# Copyright (C) 2022  Sachin Govind (Modifié pour sélection multiple dans les tags existants)
# from https://github.com/sachingooo/anki-filtered-deck-by-tag/blob/main/anki-filtered-deck-by-tag/__init__.py

from aqt import mw
from aqt.qt import *
from aqt.utils import tooltip
from anki.collection import SearchNode
from aqt.browser import SidebarItem, SidebarTreeView, SidebarItemType
from aqt.gui_hooks import browser_sidebar_will_show_context_menu
from anki.consts import DYN_OLDEST, DYN_RANDOM, DYN_SMALLINT, DYN_BIGINT, DYN_LAPSES, DYN_ADDED, DYN_DUE, DYN_REVADDED, \
    DYN_DUEPRIORITY

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aqt.browser import SidebarTreeView  # type: ignore


class MultiTagSelectionDialog(QDialog):
    """Fenêtre de dialogue personnalisée pour cocher plusieurs tags existants."""

    def __init__(self, parent=None, tags=None):
        super().__init__(parent)
        self.setWindowTitle("Croiser avec d'autres tags")
        self.setMinimumWidth(350)
        self.setMinimumHeight(400)

        self.selected_tags = []

        layout = QVBoxLayout(self)

        # Instruction
        label = QLabel("Sélectionnez un ou plusieurs tags à croiser :")
        layout.addWidget(label)

        # Liste déroulante avec cases à cocher
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)  # Géré par les checkbox

        if tags:
            for tag in sorted(tags):
                item = QListWidgetItem(tag)
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                item.setCheckState(Qt.CheckState.Unchecked)
                self.list_widget.addItem(item)

        layout.addWidget(self.list_widget)

        # Boutons de validation / annulation
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept_selection)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def accept_selection(self):
        self.selected_tags = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                self.selected_tags.append(item.text())
        self.accept()


def _filteredDeckFromTag(sidebar: "SidebarTreeView", menu: QMenu, item: SidebarItem, index: QModelIndex):
    # S'active uniquement sur un clic droit sur un tag dans la barre latérale
    if item.item_type == SidebarItemType.TAG:
        menu.addSeparator()
        menu.addAction("Create Filtered Deck (Croiser avec tags existants...)",
                       lambda: _promptAndCreateFilteredDeck(item))


def _promptAndCreateFilteredDeck(item: SidebarItem):
    if not item.full_name:
        return

    col = mw.col
    if not col:
        return

    # Récupérer tous les tags existants dans la collection Anki
    all_tags = col.tags.all()

    # Ouvrir la boîte de dialogue à choix multiples
    dialog = MultiTagSelectionDialog(mw, all_tags)
    if dialog.exec() != QDialog.DialogCode.Accepted:
        return

    chosen_tags = dialog.selected_tags

    # Construction de la recherche Anki de base
    search = f"tag:\"{item.full_name}\""

    # Ajouter chaque tag supplémentaire sélectionné avec un opérateur ET (AND)
    for t in chosen_tags:
        search += f" tag:\"{t}\""

    config = col.conf.get("dynFilterConfig", {})

    # Nommage automatique du paquet filtré
    deckName = _formatDeckNameFromTag(item.full_name)
    if chosen_tags:
        deckName += " + " + " + ".join(chosen_tags)

    numberCards = 300
    if config:
        if config.get("numCards", 0) > 0:
            numberCards = config["numCards"]
        if config.get("unsuspendAutomatically"):
            cidsToUnsuspend = col.find_cards(search)
            col.sched.unsuspend_cards(cidsToUnsuspend)

    defaultOrder = config.get("defaultOrder", DYN_DUE)
    if defaultOrder not in [DYN_OLDEST, DYN_RANDOM, DYN_SMALLINT, DYN_BIGINT, DYN_LAPSES, DYN_ADDED, DYN_DUE,
                            DYN_REVADDED, DYN_DUEPRIORITY]:
        defaultOrder = DYN_DUE

    mw.progress.start()
    did = col.decks.new_filtered(deckName)
    deck = col.decks.get(did)
    deck["terms"] = [[search, numberCards, defaultOrder]]
    col.decks.save(deck)
    col.sched.rebuildDyn(did)
    mw.progress.finish()
    mw.reset()
    tooltip("Paquet filtré créé : %s" % (deckName))


def _formatDeckNameFromTag(tagName: str):
    pieces = tagName.split("_")
    if len(pieces) == 1:
        return pieces[0].capitalize()
    return " ".join([p.capitalize() for p in pieces])


# Enregistrement du hook pour afficher l'option dans le menu contextuel du navigateur
browser_sidebar_will_show_context_menu.append(_filteredDeckFromTag)