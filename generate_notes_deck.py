import random
import genanki

# ==============================================================================
# CONFIGURATION DU DECK ET DU MODÈLE ANKI
# ==============================================================================

MODEL_ID = 1684930215
DECK_BASE_NAME = "Music ♫::Theory::Partition"

NOTE_MODEL = genanki.Model(
    MODEL_ID,
    "Modele_Note_Portee_SVG_V3",
    fields=[
        {"name": "Clef"},
        {"name": "Tonalite"},
        {"name": "NoteNom"},
        {"name": "Octave"},
        {"name": "SVG"},
    ],
    templates=[
        {
            "name": "Lecture de Note",
            "qfmt": """
            <div style="text-align: center; font-family: Arial, sans-serif;">
                <div style="font-size: 14px; color: #666; margin-bottom: 10px;">Quelle est cette note ?</div>
                <div>{{{SVG}}}</div>
            </div>
            """,
            "afmt": """
            {{FrontSide}}
            <hr id="answer">
            <div style="text-align: center; font-family: Arial, sans-serif;">
                <div style="font-size: 24px; font-weight: bold; color: #2c3e50;">
                    {{NoteNom}} {{Octave}}
                </div>
                <div style="font-size: 16px; color: #7f8c8d; margin-top: 5px;">
                    Tonalité : <strong>{{Tonalite}}</strong>
                </div>
            </div>
            """,
        },
    ],
    css="""
    .card {
        font-family: arial;
        text-align: center;
        color: black;
        background-color: white;
    }
    """,
)

# 15 Tonalités majeures standards
TONALITIES = [
    ("Do Majeur", 0),
    ("Sol Majeur", 1),
    ("Ré Majeur", 2),
    ("La Majeur", 3),
    ("Mi Majeur", 4),
    ("Si Majeur", 5),
    ("Fa# Majeur", 6),
    ("Do# Majeur", 7),
    ("Fa Majeur", -1),
    ("Si bémol Majeur", -2),
    ("Mi bémol Majeur", -3),
    ("La bémol Majeur", -4),
    ("Ré bémol Majeur", -5),
    ("Sol bémol Majeur", -6),
    ("Do bémol Majeur", -7),
]

# Clés disponibles
CLEFS = {
    "Clé de Sol 2e": {"symbol": "𝄞", "ref_pos": 10, "clef_y_offset": 32},
    "Clé de Fa 4e": {"symbol": "𝄢", "ref_pos": -2, "clef_y_offset": 22},
    "Clé d'Ut 1re": {"symbol": "𝄡", "ref_pos": 8, "clef_y_offset": 32},
    "Clé d'Ut 2e": {"symbol": "𝄡", "ref_pos": 6, "clef_y_offset": 27},
    "Clé d'Ut 3e": {"symbol": "𝄡", "ref_pos": 4, "clef_y_offset": 22},
    "Clé d'Ut 4e": {"symbol": "𝄡", "ref_pos": 2, "clef_y_offset": 17},
}

SHARP_POSITIONS = {
    "Clé de Sol 2e": [0, 3, -1, 2, 5, 1, 4],
    "Clé de Fa 4e": [2, 5, 1, 4, 7, 3, 6],
    "Clé d'Ut 1re": [3, 6, 2, 5, 1, 4, 0],
    "Clé d'Ut 2e": [2, 5, 1, 4, 0, 3, -1],
    "Clé d'Ut 3e": [1, 4, 0, 3, 6, 2, 5],
    "Clé d'Ut 4e": [-1, 2, -2, 1, 4, 0, 3],
}

FLAT_POSITIONS = {
    "Clé de Sol 2e": [4, 1, 5, 2, 6, 3, 7],
    "Clé de Fa 4e": [6, 3, 7, 4, 8, 5, 9],
    "Clé d'Ut 1re": [0, 4, 1, 5, 2, 6, 3],
    "Clé d'Ut 2e": [6, 3, 7, 4, 1, 5, 2],
    "Clé d'Ut 3e": [5, 2, 6, 3, 7, 4, 8],
    "Clé d'Ut 4e": [3, 0, 4, 1, 5, 2, 6],
}

# Dictionnaire des tessitures mis à jour avec les saxophones et la basse
INSTRUMENT_RANGES = {
    "piano": (21, 108),          # A0 à C8
    "guitare": (40, 79),         # E2 à G5
    "guitare_basse": (28, 64),   # E1 à E4 (Basse 4 cordes)
    "sax_soprano": (56, 88),     # Ab3 à E6 (Soprano en Bb, sons réels)
    "sax_alto": (49, 81),        # Db3 à A5 (Alto en Eb, sons réels)
    "sax_tenor": (44, 76),       # Ab2 à E5 (Ténor en Bb, sons réels)
    "soprano": (60, 84),         # C4 à C6 (Tessiture vocale)
    "alto": (53, 77),            # F3 à F5 (Tessiture vocale)
    "tenor": (48, 72),           # C3 à C5 (Tessiture vocale)
    "basse": (40, 64),           # E2 à E4 (Tessiture vocale)
}

NOTE_NAMES_FR = ["Do", "Ré", "Mi", "Fa", "Sol", "La", "Si"]


def get_piano_diatonic_notes():
    """Génère toutes les notes diatoniques de la tessiture du piano (A0 à C8)."""
    notes = []
    diatonic_offsets = [0, 2, 4, 5, 7, 9, 11]

    for midi_pitch in range(21, 109):
        semitone_in_octave = midi_pitch % 12
        if semitone_in_octave in diatonic_offsets:
            note_idx = diatonic_offsets.index(semitone_in_octave)
            note_name = NOTE_NAMES_FR[note_idx]
            octave_num = (midi_pitch // 12) - 2
            octave_from_c4 = (midi_pitch // 12) - 5
            diatonic_step = octave_from_c4 * 7 + note_idx

            notes.append({
                "midi": midi_pitch,
                "name": note_name,
                "octave": f"Octave {octave_num}",
                "diatonic_step": diatonic_step
            })
    return notes


def generate_staff_svg(clef_name, key_acc, pos_y):
    """Génère l'affichage SVG de la portée, la clé, l'armure et la note."""
    svg_width = 340
    svg_height = 220
    line_spacing = 10
    top_margin = 80
    left_margin = 30

    svg_lines = [
        f'<line x1="{left_margin}" y1="{top_margin + i * line_spacing}" x2="{svg_width - left_margin}" y2="{top_margin + i * line_spacing}" stroke="#333" stroke-width="1.5"/>'
        for i in range(5)
    ]

    clef_info = CLEFS[clef_name]
    clef_symbol = clef_info["symbol"]
    clef_y = top_margin + clef_info["clef_y_offset"]
    clef_svg = f'<text x="{left_margin + 10}" y="{clef_y}" font-family="serif" font-size="42" fill="#111">{clef_symbol}</text>'

    armure_svg = []
    x_acc = left_margin + 50

    if key_acc > 0:
        for p in SHARP_POSITIONS[clef_name][:key_acc]:
            y = top_margin + p * (line_spacing / 2)
            armure_svg.append(
                f'<text x="{x_acc}" y="{y + 4}" font-family="sans-serif" font-size="16" font-weight="bold" fill="#333">♯</text>')
            x_acc += 11
    elif key_acc < 0:
        for p in FLAT_POSITIONS[clef_name][:abs(key_acc)]:
            y = top_margin + p * (line_spacing / 2)
            armure_svg.append(
                f'<text x="{x_acc}" y="{y + 4}" font-family="sans-serif" font-size="16" font-weight="bold" fill="#333">♭</text>')
            x_acc += 11

    note_y = top_margin + pos_y * (line_spacing / 2)
    note_x = max(x_acc + 30, left_margin + 190)

    ledger_lines = []
    if pos_y < 0:
        for p in range(-2, pos_y - 1, -2):
            ly = top_margin + p * (line_spacing / 2)
            ledger_lines.append(
                f'<line x1="{note_x - 12}" y1="{ly}" x2="{note_x + 12}" y2="{ly}" stroke="#333" stroke-width="1.5"/>')
    elif pos_y > 8:
        for p in range(10, pos_y + 1, 2):
            ly = top_margin + p * (line_spacing / 2)
            ledger_lines.append(
                f'<line x1="{note_x - 12}" y1="{ly}" x2="{note_x + 12}" y2="{ly}" stroke="#333" stroke-width="1.5"/>')

    note_head = f'<ellipse cx="{note_x}" cy="{note_y}" rx="6.5" ry="4.8" transform="rotate(-20 {note_x} {note_y})" fill="#000"/>'
    stem_dir = -1 if pos_y <= 4 else 1
    stem_x = note_x + 5.5 if stem_dir == -1 else note_x - 5.5
    stem_y2 = note_y + (stem_dir * 28)
    stem = f'<line x1="{stem_x}" y1="{note_y}" x2="{stem_x}" y2="{stem_y2}" stroke="#000" stroke-width="1.5"/>'

    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
        {''.join(svg_lines)}
        {clef_svg}
        {''.join(armure_svg)}
        {''.join(ledger_lines)}
        {note_head}
        {stem}
    </svg>
    """.strip()


def get_tags_for_pitch(midi_pitch):
    """Retourne la liste des tags d'instruments correspondant au pitch MIDI donné."""
    return [inst for inst, (low, high) in INSTRUMENT_RANGES.items() if low <= midi_pitch <= high]


def main():
    all_decks = []
    notes_list = get_piano_diatonic_notes()
    total_cards = 0

    # Deck racine principal
    root_deck_id = random.randrange(10 ** 8, 10 ** 9)
    all_decks.append(genanki.Deck(root_deck_id, DECK_BASE_NAME))

    for clef_name, clef_info in CLEFS.items():
        ref_pos = clef_info["ref_pos"]

        # Deck intermédiaire de Clé
        clef_deck_id = random.randrange(10 ** 8, 10 ** 9)
        clef_deck_name = f"{DECK_BASE_NAME}::{clef_name}"
        all_decks.append(genanki.Deck(clef_deck_id, clef_deck_name))

        for tonality_name, key_acc in TONALITIES:
            deck_id = random.randrange(10 ** 8, 10 ** 9)
            subdeck_name = f"{clef_deck_name}::{tonality_name}"
            deck = genanki.Deck(deck_id, subdeck_name)

            for note_info in notes_list:
                midi_pitch = note_info["midi"]
                pos_y = ref_pos - note_info["diatonic_step"]

                # Limite l'affichage à max 5 lignes supplémentaires
                if -10 <= pos_y <= 18:
                    svg_content = generate_staff_svg(clef_name, key_acc, pos_y)
                    tags = get_tags_for_pitch(midi_pitch)
                    tags.append(clef_name.replace(" ","_"))
                    tags.append(tonality_name.replace(" ", "_"))

                    note = genanki.Note(
                        model=NOTE_MODEL,
                        fields=[
                            clef_name,
                            tonality_name,
                            note_info["name"],
                            note_info["octave"],
                            svg_content,
                        ],
                        tags=tags,
                    )
                    deck.add_note(note)
                    total_cards += 1

            all_decks.append(deck)

    package = genanki.Package(all_decks)
    package.write_to_file("notes_lecture.apkg")
    print(f"Paquet généré avec succès ! {total_cards} cartes créées au total.")


if __name__ == "__main__":
    main()