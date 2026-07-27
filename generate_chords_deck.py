import genanki
import json

MODEL_ID = 2748591038
MAIN_DECK_NAME = 'Music ♫::Guitar::Chords'

# -----------------------------------------------------------------------------
# Palette de Couleurs Strictes par Degré
# -----------------------------------------------------------------------------
DEGREE_COLORS = {
    "1": "#f85149",  # Tonique -> ROUGE
    "3": "#d97706", "b3": "#d97706",  # Tierces -> ORANGE
    "5": "#2563eb", "b5": "#2563eb", "#5": "#2563eb",  # Quintes -> BLEU
    "7": "#9333ea", "b7": "#9333ea", "bb7": "#9333ea"  # Septièmes -> VIOLET
}
DEFAULT_QUESTION_COLOR = "#388bfd"


def get_degree_color(degre):
    return DEGREE_COLORS.get(degre, "#6e7681")


# -----------------------------------------------------------------------------
# MOTEUR HARMONIQUE EXHAUSTIF
# -----------------------------------------------------------------------------
PITCH_CLASSES = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5,
                 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}
PITCH_TO_NAME = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']

GUITAR_TUNING = [64, 59, 55, 50, 45, 40]  # E4, B3, G3, D3, A2, E2

CHORD_DEFINITIONS = {
    # --- TRIADES ---
    "Majeur": {"type": "Triades", "formula": [("1", 0), ("3", 4), ("5", 7)]},
    "Mineur": {"type": "Triades", "formula": [("1", 0), ("b3", 3), ("5", 7)]},
    "Diminué": {"type": "Triades", "formula": [("1", 0), ("b3", 3), ("b5", 6)]},
    "Augmenté": {"type": "Triades", "formula": [("1", 0), ("3", 4), ("#5", 8)]},
    "Sus2": {"type": "Triades", "formula": [("1", 0), ("2", 2), ("5", 7)]},
    "Sus4": {"type": "Triades", "formula": [("1", 0), ("4", 5), ("5", 7)]},

    # --- TÉTRADES ---
    "Majeur 7": {"type": "Tétrades", "formula": [("1", 0), ("3", 4), ("5", 7), ("7", 11)]},
    "Dominante 7": {"type": "Tétrades", "formula": [("1", 0), ("3", 4), ("5", 7), ("b7", 10)]},
    "Mineur 7": {"type": "Tétrades", "formula": [("1", 0), ("b3", 3), ("5", 7), ("b7", 10)]},
    "Demi-diminué (m7b5)": {"type": "Tétrades", "formula": [("1", 0), ("b3", 3), ("b5", 6), ("b7", 10)]},
    "Diminué 7": {"type": "Tétrades", "formula": [("1", 0), ("b3", 3), ("b5", 6), ("bb7", 9)]},
    "Mineur Majeur 7": {"type": "Tétrades", "formula": [("1", 0), ("b3", 3), ("5", 7), ("7", 11)]},
    "Septième Augmentée (7#5)": {"type": "Tétrades", "formula": [("1", 0), ("3", 4), ("#5", 8), ("b7", 10)]}
}

INVERSION_NAMES = ["Fondamental", "1ère Inversion", "2ème Inversion", "3ème Inversion"]


def generate_full_harmony_dataset():
    dataset = []
    root_note = "C"
    root_pitch = PITCH_CLASSES[root_note]

    for qualite, defn in CHORD_DEFINITIONS.items():
        chord_type = defn["type"]
        base_formula = defn["formula"]
        num_notes = len(base_formula)

        # Générer toutes les inversions
        for inv_idx in range(num_notes):
            inv_name = INVERSION_NAMES[inv_idx]

            # Rotation de la formule pour l'inversion
            current_formula = base_formula[inv_idx:] + base_formula[:inv_idx]

            # Calcul des degrés, notes et intervalles
            degres_list = [item[0] for item in current_formula]
            semitones_from_root = [item[1] for item in current_formula]

            notes_list = [PITCH_TO_NAME[(root_pitch + st) % 12] for st in semitones_from_root]

            # Intervalle relatif entre notes consécutives
            prev_st = 0
            analysis = []
            for idx, (deg, st) in enumerate(zip(degres_list, semitones_from_root)):
                diff_prev = (st - prev_st) % 12 if idx > 0 else 0
                analysis.append({
                    "degre": deg,
                    "note": notes_list[idx],
                    "semitones_root": st,
                    "semitones_prev": diff_prev
                })
                prev_st = st

            top_note_str = f"{notes_list[-1]} ({degres_list[-1]})"

            # Recherche des positions physiques sur les ensembles de cordes (String Sets)
            # Triades: cordes (E-A-D, A-D-G, D-G-B, G-B-E) | Tétrades: (E-A-D-G, A-D-G-B, D-G-B-E)
            string_sets = [[5, 4, 3], [4, 3, 2], [3, 2, 1], [2, 1, 0]] if num_notes == 3 else [[5, 4, 3, 2],
                                                                                               [4, 3, 2, 1],
                                                                                               [3, 2, 1, 0]]

            for string_set in string_sets:
                guitare_pos = []
                piano_pos = []

                # Calcul des frettes
                frettes_temp = []

                for idx, corde_idx in enumerate(string_set):
                    target_pitch = (root_pitch + semitones_from_root[idx]) % 12
                    open_pitch = GUITAR_TUNING[corde_idx] % 12
                    frette = (target_pitch - open_pitch) % 12

                    if frette == 0:  # Si à vide, ajouter une octave pour la lisibilité visuelle du manche
                        frette += 12

                    frettes_temp.append(frette)
                    guitare_pos.append((corde_idx, frette, degres_list[idx], notes_list[idx]))

                # Vérification de l'écartement physique (écarte max de 4 frettes)
                min_f = min(frettes_temp)
                max_f = max(frettes_temp)
                fret_span = (max_f - min_f) + 1  # Nombre total de frettes couvertes par le doigté

                # FILTRE REVISITÉ : Jusqu'à 6 frettes au maximum (1, 2, 3, 4, 5 ou 6 frettes)
                if fret_span > 6:
                    continue

                # Calcul touches piano (Index 0-11)
                for idx, st in enumerate(semitones_from_root):
                    key_idx = (root_pitch + st) % 12
                    piano_pos.append((key_idx, degres_list[idx], notes_list[idx]))

                set_str = f"Cordes {'-'.join([str(6 - c) for c in string_set])}"
                nom_accord = f"Do {qualite} ({root_note}) - {inv_name} [{set_str}]"

                dataset.append({
                    "type": chord_type,
                    "qualite": qualite,
                    "nom": nom_accord,
                    "inversion": inv_name,
                    "degres": " - ".join(degres_list),
                    "notes": " - ".join(notes_list),
                    "top_note": top_note_str,
                    "fret_span": fret_span,
                    "guitare": guitare_pos,
                    "piano": piano_pos,
                    "analysis": analysis
                })

    return dataset


# -----------------------------------------------------------------------------
# Modèle Anki (Champs, CSS et Templates)
# -----------------------------------------------------------------------------
chord_model = genanki.Model(
    MODEL_ID,
    'Guitare & Piano - Centered Notes Chords',
    fields=[
        {'name': 'NomAccord'},
        {'name': 'TypeAccord'},
        {'name': 'Qualite'},
        {'name': 'Inversion'},
        {'name': 'TopNote'},
        {'name': 'Degres'},
        {'name': 'Notes'},
        {'name': 'TableAnalyseHtml'},
        {'name': 'SvgGuitareQuestion'},
        {'name': 'SvgGuitareReponse'},
        {'name': 'SvgPiano'}
    ],
    templates=[
        {
            'name': 'Harmonie & Doigtés',
            'qfmt': '''
                <div class="card-container">
                    <div class="badge">{{TypeAccord}} • {{Qualite}}</div>
                    <h2>{{NomAccord}}</h2>
                    <div class="sub-info">Inversion : <strong>{{Inversion}}</strong></div>

                    <div class="section-title">Positions Guitare</div>
                    <div class="svg-box">{{{SvgGuitareQuestion}}}</div>

                    <div class="question-prompt">Quels sont les <strong>degrés</strong>, les <strong>notes</strong> et les <strong>intervalles</strong> ?</div>
                </div>
            ''',
            'afmt': '''
                {{FrontSide}}
                <hr id="answer">
                <div class="answer-box">
                    <div class="section-title" style="margin-top: 0;">Doigté avec Degrés</div>
                    <div class="svg-box">{{{SvgGuitareReponse}}}</div>

                    <div class="section-title">Analyse des Intervalles</div>
                    {{{TableAnalyseHtml}}}

                    <p style="margin-top: 15px;"><strong>Note la plus aiguë (Top Note) :</strong> {{TopNote}}</p>

                    <div class="section-title">Piano</div>
                    <div class="svg-box">{{{SvgPiano}}}</div>
                </div>
            ''',
        },
    ],
    css='''
        .card { font-family: system-ui, -apple-system, sans-serif; text-align: center; color: #f0f0f0; background-color: #121212; }
        .card-container { max-width: 550px; margin: 0 auto; padding: 10px; }
        h2 { color: #58a6ff; margin: 5px 0 10px 0; font-size: 1.6em; }
        .badge { display: inline-block; background: #238636; color: #fff; padding: 4px 10px; border-radius: 12px; font-size: 0.8em; font-weight: bold; }
        .sub-info { color: #8b949e; margin-bottom: 15px; font-size: 1em; }
        .section-title { font-weight: bold; color: #8b949e; text-transform: uppercase; letter-spacing: 1px; margin-top: 15px; font-size: 0.85em; text-align: left; }
        .svg-box { margin: 10px 0; display: flex; justify-content: center; background: #1c2128; border-radius: 8px; padding: 10px; }
        .question-prompt { font-size: 0.95em; color: #d2a8ff; margin-top: 15px; font-style: italic; }
        .answer-box { font-size: 1em; padding: 15px; background: #130f0e; color: #ffffff; border-radius: 8px; margin-top: 15px; border: 1px solid #30363d; text-align: left; }

        .interval-table { width: 100%; border-collapse: collapse; margin-top: 8px; font-size: 0.9em; }
        .interval-table th, .interval-table td { border: 1px solid #30363d; padding: 6px 8px; text-align: center; }
        .interval-table th { background-color: #161b22; color: #58a6ff; }
        .interval-table tr:nth-child(even) { background-color: #161b22; }

        .degree-badge { display: inline-block; width: 24px; height: 24px; line-height: 24px; border-radius: 50%; color: #fff; font-weight: bold; font-size: 0.85em; }
    '''
)


# -----------------------------------------------------------------------------
# Générateur SVG avec Centrage Précis des Notes
# -----------------------------------------------------------------------------
def generate_guitar_svg(frets_and_strings, is_question=False):
    frets_played = [f for _, f, _, _ in frets_and_strings if f > 0]
    min_fret = min(frets_played) if frets_played else 1

    # Paramètres de grille
    start_x = 40  # Marge à gauche (frette de départ)
    fret_width = 50  # Largeur de chaque case

    svg = ['<svg width="360" height="170" viewBox="0 0 360 170">']

    # Texte indiquant la frette minimale (placé au-dessus de la 1ère case affichée)
    first_case_center = start_x + (fret_width / 2)
    svg.append(
        f'<text x="{first_case_center}" y="15" font-size="12" fill="#d2a8ff" font-weight="bold" text-anchor="middle">Frette {min_fret}</text>')

    # Cordes horizontales (de la corde 1 en haut à la corde 6 en bas)
    for i in range(6):
        y = 30 + i * 20
        svg.append(f'<line x1="30" y1="{y}" x2="340" y2="{y}" stroke="#6e7681" stroke-width="2"/>')

    # Frettes verticales (les barres métalliques)
    for f in range(7):  # 6 cases complètes
        x = start_x + f * fret_width
        svg.append(f'<line x1="{x}" y1="30" x2="{x}" y2="130" stroke="#8b949e" stroke-width="3"/>')

    # Placement des puces (notes)
    for corde, frette, degre, _ in frets_and_strings:
        cy = 30 + corde * 20

        if frette > 0:
            # Calcul du centre exact de la case relative
            fret_offset = frette - min_fret
            cx = start_x + (fret_offset * fret_width) + (fret_width / 2)
        else:
            # Note à vide (à gauche de la première frette)
            cx = 20

        color = DEFAULT_QUESTION_COLOR if is_question else get_degree_color(degre)

        svg.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="{color}" stroke="#fff" stroke-width="1.5"/>')

        if not is_question:
            svg.append(
                f'<text x="{cx}" y="{cy + 3.5}" font-size="9" fill="#fff" text-anchor="middle" font-weight="bold">{degre}</text>')

    svg.append('</svg>')
    return "".join(svg)


def generate_piano_svg(active_keys):
    svg = ['<svg width="350" height="100" viewBox="0 0 350 100">']
    white_keys = [0, 2, 4, 5, 7, 9, 11]
    black_keys = {1: 0, 3: 1, 6: 3, 8: 4, 10: 5}

    for idx, key_num in enumerate(white_keys):
        x = idx * 50
        svg.append(f'<rect x="{x}" y="0" width="48" height="95" fill="#f0f6fc" rx="3" stroke="#d0d7de"/>')

    for key_num, idx in black_keys.items():
        x = idx * 50 + 33
        svg.append(f'<rect x="{x}" y="0" width="28" height="58" fill="#161b22" rx="2"/>')

    active_dict = {k: d for k, d, _ in active_keys}
    for key_num, degre in active_dict.items():
        color = get_degree_color(degre)

        if key_num in white_keys:
            w_idx = white_keys.index(key_num)
            cx, cy = w_idx * 50 + 24, 75
        else:
            b_idx = black_keys[key_num]
            cx, cy = b_idx * 50 + 47, 40

        svg.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="{color}" stroke="#fff" stroke-width="1"/>')
        svg.append(
            f'<text x="{cx}" y="{cy + 3.5}" font-size="9" fill="#fff" text-anchor="middle" font-weight="bold">{degre}</text>')

    svg.append('</svg>')
    return "".join(svg)


def generate_analysis_table(notes_info):
    html = ['<table class="interval-table">']
    html.append('<tr><th>Degré</th><th>Note</th><th>Δ Tonique</th><th>Δ Précédent</th></tr>')

    for n in notes_info:
        bg_color = get_degree_color(n["degre"])
        dt_root = f'+{n["semitones_root"]} st' if n["semitones_root"] > 0 else '0 st (Tonique)'
        dt_prev = f'+{n["semitones_prev"]} st' if n["semitones_prev"] > 0 else '-'

        html.append('<tr>')
        html.append(f'<td><span class="degree-badge" style="background-color: {bg_color};">{n["degre"]}</span></td>')
        html.append(f'<td>{n["note"]}</td>')
        html.append(f'<td>{dt_root}</td>')
        html.append(f'<td>{dt_prev}</td>')
        html.append('</tr>')

    html.append('</table>')
    return "".join(html)


# -----------------------------------------------------------------------------
# Exécution & Exportation avec Sous-Decks Hiérarchisés
# -----------------------------------------------------------------------------
main_deck_id = 9812734912
all_decks = []

root_deck = genanki.Deck(main_deck_id, MAIN_DECK_NAME)
all_decks.append(root_deck)

subdeck_registry = {}
full_dataset = generate_full_harmony_dataset()

for item in full_dataset:
    category = item["type"]  # "Triades" ou "Tétrades"
    qualite = item["qualite"]  # ex: "Majeur", "Mineur 7", etc.

    # Hiérarchie dynamique de decks : Music ♫::Guitar::Chords::<Type>::<Qualité>
    subdeck_name = f"{MAIN_DECK_NAME}::{category}::{qualite}"

    if subdeck_name not in subdeck_registry:
        s_id = main_deck_id + hash(subdeck_name) % 10000000
        subdeck = genanki.Deck(s_id, subdeck_name)
        subdeck_registry[subdeck_name] = subdeck
        all_decks.append(subdeck)
    else:
        subdeck = subdeck_registry[subdeck_name]

    svg_guitare_q = generate_guitar_svg(item["guitare"], is_question=True)
    svg_guitare_r = generate_guitar_svg(item["guitare"], is_question=False)
    svg_piano = generate_piano_svg(item["piano"])

    table_analysis = generate_analysis_table(item["analysis"])

    tag_type = item["type"].lower()
    tag_inversion = item["inversion"].replace(" ", "_").lower()
    tag_degres = f"degres_{item['degres'].replace(' ', '')}"
    tag_top_note = f"top_note_{item['top_note'].split(' ')[0]}"

    # Tag singulier / pluriel selon le span
    span_unit = "frette" if item['fret_span'] == 1 else "frettes"
    tag_span = f"span_{item['fret_span']}_{span_unit}"

    tags = [
        tag_type,
        f"qualite_{item['qualite'].lower().replace(' ', '_')}",
        f"inversion_{tag_inversion}",
        tag_degres,
        tag_top_note,
        tag_span
    ]

    note = genanki.Note(
        model=chord_model,
        fields=[
            item["nom"],
            item["type"],
            item["qualite"],
            item["inversion"],
            item["top_note"],
            item["degres"],
            item["notes"],
            table_analysis,
            svg_guitare_q,
            svg_guitare_r,
            svg_piano
        ],
        tags=tags
    )
    subdeck.add_note(note)

genanki.Package(all_decks).write_to_file('music_guitar_chords.apkg')
print(f"Fichier 'music_guitar_chords.apkg' généré avec succès ({len(full_dataset)} cartes créées) !")