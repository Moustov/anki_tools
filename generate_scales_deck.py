import genanki
import json

# Identifiants uniques pour Anki
MODEL_ID = 1893475202
MAIN_DECK_ID = 2948576103
DECK_NAME = 'Music ♫::Guitar::Scales::Gamme Mineure et Pentatonique'
# Données inchangées (DATA_PENTA, DATA_NATURELLE)...

main_deck = genanki.Deck(MAIN_DECK_ID, DECK_NAME)
all_decks = [main_deck]

# Définition des cordes (Mi, Si, Sol, Ré, La, Mi) et frettes par box en Am
# Format : (corde_index, frette, nom_note, degre, intervalle_nom, demi_tons)
# Corde 0 = Mi aigu, Corde 5 = Mi grave
# Corde 5 = Mi grave, Corde 0 = Mi aigu
# Corde, Frette, Note, Degré, Nom de l'intervalle, Demi-tons depuis la tonique

DATA_PENTA = {
    "Box 1 (Frettes 5-8)": [
        (5, 5, "A", "1", "Tonique", 0), (5, 8, "C", "b3", "Tierce mineure", 3),
        (4, 5, "D", "4", "Quarte juste", 5), (4, 7, "E", "5", "Quinte juste", 7),
        (3, 5, "G", "b7", "Septième mineure", 10), (3, 7, "A", "1", "Tonique", 0),
        (2, 5, "C", "b3", "Tierce mineure", 3), (2, 7, "D", "4", "Quarte juste", 5),
        (1, 5, "E", "5", "Quinte juste", 7), (1, 8, "G", "b7", "Septième mineure", 10),
        (0, 5, "A", "1", "Tonique", 0), (0, 8, "C", "b3", "Tierce mineure", 3)
    ],
    "Box 2 (Frettes 7-10)": [
        (5, 8, "C", "b3", "Tierce mineure", 3), (5, 10, "D", "4", "Quarte juste", 5),
        (4, 7, "E", "5", "Quinte juste", 7), (4, 10, "G", "b7", "Septième mineure", 10),
        (3, 7, "A", "1", "Tonique", 0), (3, 10, "C", "b3", "Tierce mineure", 3),
        (2, 7, "D", "4", "Quarte juste", 5), (2, 9, "E", "5", "Quinte juste", 7),
        (1, 8, "G", "b7", "Septième mineure", 10), (1, 10, "A", "1", "Tonique", 0),
        (0, 8, "C", "b3", "Tierce mineure", 3), (0, 10, "D", "4", "Quarte juste", 5)
    ],
    "Box 3 (Frettes 9-12)": [
        (5, 10, "D", "4", "Quarte juste", 5), (5, 12, "E", "5", "Quinte juste", 7),
        (4, 10, "G", "b7", "Septième mineure", 10), (4, 12, "A", "1", "Tonique", 0),
        (3, 10, "C", "b3", "Tierce mineure", 3), (3, 12, "D", "4", "Quarte juste", 5),
        (2, 9, "E", "5", "Quinte juste", 7), (2, 12, "G", "b7", "Septième mineure", 10),
        (1, 10, "A", "1", "Tonique", 0), (1, 13, "C", "b3", "Tierce mineure", 3),
        (0, 10, "D", "4", "Quarte juste", 5), (0, 12, "E", "5", "Quinte juste", 7)
    ],
    "Box 4 (Frettes 12-15)": [
        (5, 12, "E", "5", "Quinte juste", 7), (5, 15, "G", "b7", "Septième mineure", 10),
        (4, 12, "A", "1", "Tonique", 0), (4, 15, "C", "b3", "Tierce mineure", 3),
        (3, 12, "D", "4", "Quarte juste", 5), (3, 14, "E", "5", "Quinte juste", 7),
        (2, 12, "G", "b7", "Septième mineure", 10), (2, 14, "A", "1", "Tonique", 0),
        (1, 13, "C", "b3", "Tierce mineure", 3), (1, 15, "D", "4", "Quarte juste", 5),
        (0, 12, "E", "5", "Quinte juste", 7), (0, 15, "G", "b7", "Septième mineure", 10)
    ],
    "Box 5 (Frettes 15-17)": [
        (5, 15, "G", "b7", "Septième mineure", 10), (5, 17, "A", "1", "Tonique", 0),
        (4, 15, "C", "b3", "Tierce mineure", 3), (4, 17, "D", "4", "Quarte juste", 5),
        (3, 14, "E", "5", "Quinte juste", 7), (3, 17, "G", "b7", "Septième mineure", 10),
        (2, 14, "A", "1", "Tonique", 0), (2, 17, "C", "b3", "Tierce mineure", 3),
        (1, 15, "D", "4", "Quarte juste", 5), (1, 17, "E", "5", "Quinte juste", 7),
        (0, 15, "G", "b7", "Septième mineure", 10), (0, 17, "A", "1", "Tonique", 0)
    ]
}

DATA_NATURELLE = {
    "Box 1 (Frettes 5-8)": [
        (5, 5, "A", "1", "Tonique", 0), (5, 7, "B", "2", "Seconde majeure", 2), (5, 8, "C", "b3", "Tierce mineure", 3),
        (4, 5, "D", "4", "Quarte juste", 5), (4, 7, "E", "5", "Quinte juste", 7), (4, 8, "F", "b6", "Sixte mineure", 8),
        (3, 5, "G", "b7", "Septième mineure", 10), (3, 7, "A", "1", "Tonique", 0),
        (2, 5, "C", "b3", "Tierce mineure", 3), (2, 7, "D", "4", "Quarte juste", 5),
        (1, 5, "E", "5", "Quinte juste", 7), (1, 6, "F", "b6", "Sixte mineure", 8),
        (1, 8, "G", "b7", "Septième mineure", 10),
        (0, 5, "A", "1", "Tonique", 0), (0, 7, "B", "2", "Seconde majeure", 2), (0, 8, "C", "b3", "Tierce mineure", 3)
    ],
    "Box 2 (Frettes 7-10)": [
        (5, 7, "B", "2", "Seconde majeure", 2), (5, 8, "C", "b3", "Tierce mineure", 3),
        (5, 10, "D", "4", "Quarte juste", 5),
        (4, 7, "E", "5", "Quinte juste", 7), (4, 8, "F", "b6", "Sixte mineure", 8),
        (4, 10, "G", "b7", "Septième mineure", 10),
        (3, 7, "A", "1", "Tonique", 0), (3, 9, "B", "2", "Seconde majeure", 2), (3, 10, "C", "b3", "Tierce mineure", 3),
        (2, 7, "D", "4", "Quarte juste", 5), (2, 9, "E", "5", "Quinte juste", 7),
        (2, 10, "F", "b6", "Sixte mineure", 8),
        (1, 8, "G", "b7", "Septième mineure", 10), (1, 10, "A", "1", "Tonique", 0),
        (0, 7, "B", "2", "Seconde majeure", 2), (0, 8, "C", "b3", "Tierce mineure", 3),
        (0, 10, "D", "4", "Quarte juste", 5)
    ],
    "Box 3 (Frettes 9-12)": [
        (5, 10, "D", "4", "Quarte juste", 5), (5, 12, "E", "5", "Quinte juste", 7),
        (5, 13, "F", "b6", "Sixte mineure", 8),
        (4, 10, "G", "b7", "Septième mineure", 10), (4, 12, "A", "1", "Tonique", 0),
        (3, 9, "B", "2", "Seconde majeure", 2), (3, 10, "C", "b3", "Tierce mineure", 3),
        (3, 12, "D", "4", "Quarte juste", 5),
        (2, 9, "E", "5", "Quinte juste", 7), (2, 10, "F", "b6", "Sixte mineure", 8),
        (2, 12, "G", "b7", "Septième mineure", 10),
        (1, 10, "A", "1", "Tonique", 0), (1, 12, "B", "2", "Seconde majeure", 2),
        (1, 13, "C", "b3", "Tierce mineure", 3),
        (0, 10, "D", "4", "Quarte juste", 5), (0, 12, "E", "5", "Quinte juste", 7),
        (0, 13, "F", "b6", "Sixte mineure", 8)
    ],
    "Box 4 (Frettes 12-15)": [
        (5, 12, "E", "5", "Quinte juste", 7), (5, 13, "F", "b6", "Sixte mineure", 8),
        (5, 15, "G", "b7", "Septième mineure", 10),
        (4, 12, "A", "1", "Tonique", 0), (4, 14, "B", "2", "Seconde majeure", 2),
        (4, 15, "C", "b3", "Tierce mineure", 3),
        (3, 12, "D", "4", "Quarte juste", 5), (3, 14, "E", "5", "Quinte juste", 7),
        (3, 15, "F", "b6", "Sixte mineure", 8),
        (2, 12, "G", "b7", "Septième mineure", 10), (2, 14, "A", "1", "Tonique", 0),
        (1, 12, "B", "2", "Seconde majeure", 2), (1, 13, "C", "b3", "Tierce mineure", 3),
        (1, 15, "D", "4", "Quarte juste", 5),
        (0, 12, "E", "5", "Quinte juste", 7), (0, 13, "F", "b6", "Sixte mineure", 8),
        (0, 15, "G", "b7", "Septième mineure", 10)
    ],
    "Box 5 (Frettes 15-18)": [
        (5, 15, "G", "b7", "Septième mineure", 10), (5, 17, "A", "1", "Tonique", 0),
        (4, 14, "B", "2", "Seconde majeure", 2), (4, 15, "C", "b3", "Tierce mineure", 3),
        (4, 17, "D", "4", "Quarte juste", 5),
        (3, 14, "E", "5", "Quinte juste", 7), (3, 15, "F", "b6", "Sixte mineure", 8),
        (3, 17, "G", "b7", "Septième mineure", 10),
        (2, 14, "A", "1", "Tonique", 0), (2, 16, "B", "2", "Seconde majeure", 2),
        (2, 17, "C", "b3", "Tierce mineure", 3),
        (1, 15, "D", "4", "Quarte juste", 5), (1, 17, "E", "5", "Quinte juste", 7),
        (1, 18, "F", "b6", "Sixte mineure", 8),
        (0, 15, "G", "b7", "Septième mineure", 10), (0, 17, "A", "1", "Tonique", 0)
    ]
}


def generate_svg(min_fret, target_corde, target_frette, notes_box, show_degrees=False):
    svg = ['<svg width="400" height="180" viewBox="0 0 400 180">']

    # 1. Cordes
    for i in range(6):
        y = 20 + i * 25
        svg.append(f'<line x1="20" y1="{y}" x2="380" y2="{y}" stroke="#888" stroke-width="2"/>')

    # 2. Frettes
    num_frets = 6 if (target_frette - min_fret) > 4 else 5
    for f in range(num_frets + 1):
        x = 40 + f * 70
        svg.append(f'<line x1="{x}" y1="20" x2="{x}" y2="145" stroke="#444" stroke-width="3"/>')

    # 3. Pastilles de la box (Bleu ciel)
    for corde, frette, _, degre, _, _ in notes_box:
        # On ne dessine pas tout de suite la cible en bleu, elle sera faite en rouge par-dessus
        if corde == target_corde and frette == target_frette:
            continue
        nx = 40 + (frette - min_fret) * 70 + 35
        ny = 20 + corde * 25

        # Le rayon reste 9 ou 10 pour permettre au texte d'être bien lisible
        r = 10 if show_degrees else 8
        svg.append(
            f'<circle cx="{nx}" cy="{ny}" r="{r}" fill="#87CEEB" opacity="0.95" stroke="#5fa4c4" stroke-width="1"/>')

        if show_degrees:
            svg.append(
                f'<text x="{nx}" y="{ny + 3.5}" font-size="9" fill="#121212" font-weight="bold" text-anchor="middle">{degre}</text>')

    # 4. Note cible en rouge par-dessus
    tx = 40 + (target_frette - min_fret) * 70 + 35
    ty = 20 + target_corde * 25
    target_degre = next(deg for c, f, _, deg, _, _ in notes_box if c == target_corde and f == target_frette)

    svg.append(f'<circle cx="{tx}" cy="{ty}" r="11" fill="red" stroke="#900" stroke-width="1.5"/>')
    if show_degrees:
        svg.append(
            f'<text x="{tx}" y="{ty + 3.5}" font-size="9" fill="#ffffff" font-weight="bold" text-anchor="middle">{target_degre}</text>')

    svg.append('</svg>')
    return "".join(svg)


# Modèle Anki
guitar_model = genanki.Model(
    MODEL_ID,
    'Guitare Degres Structure Complete Native Fixed',
    fields=[
        {'name': 'Gamme'},
        {'name': 'Box'},
        {'name': 'FretteDebut'},
        {'name': 'FretteFin'},
        {'name': 'NoteCorde'},
        {'name': 'NoteFrette'},
        {'name': 'PositionsToniques'},
        {'name': 'Intervalle'},
        {'name': 'DemiTons'},
        {'name': 'BoxNotes'},
        {'name': 'SvgMancheQuestion'},
        {'name': 'SvgMancheReponse'}
    ],
    templates=[
        {
            'name': 'Trouver le Degré',
            'qfmt': '''
                <div class="info">
                    <h2>{{Gamme}}</h2>
                    <h3>{{Box}}</h3>
                </div>
                <div class="canvas-container">
                    {{{SvgMancheQuestion}}}
                </div>
                <p>Quel est le degré de la note en rouge, son intervalle et sa distance en demi-tons ?</p>
            ''',
            'afmt': '''
                {{FrontSide}}
                <hr id="answer">
                <div class="answer-box">
                    <div class="canvas-container">
                        {{{SvgMancheReponse}}}
                    </div>
                    <p><strong>Degré / Intervalle :</strong> {{Intervalle}}</p>
                    <p><strong>Distance :</strong> {{DemiTons}} demi-tons</p>
                </div>
            ''',
        },
    ],
    css='''
            .card { font-family: system-ui, sans-serif; text-align: center; color: #333; background-color: #fefefe; }
            .info h2 { color: #2c3e50; margin-bottom: 5px; }
            .info h3 { color: #7f8c8d; margin-top: 0; }
            .canvas-container { margin: 15px auto; width: 100%; max-width: 500px; display: flex; justify-content: center; }
            .answer-box { font-size: 1.1em; padding: 15px; background: #130f0e; color: #ffffff; border-radius: 8px; display: inline-block; margin-top: 10px; width: 90%; }
        '''
)


def populate_deck_advanced(data_dict, gamme_name, gamme_order_prefix):
    tag_gamme = gamme_name.replace(" ", "_").replace("(", "").replace(")", "").replace("/", "")

    for box_idx, (box_name, notes) in enumerate(data_dict.items(), start=1):

        subdeck_name = f"{DECK_NAME}::{gamme_order_prefix} - {gamme_name}::Box {box_idx:02d}"
        subdeck_id = MAIN_DECK_ID + hash(subdeck_name) % 10000000
        subdeck = genanki.Deck(subdeck_id, subdeck_name)
        all_decks.append(subdeck)

        sorted_notes = sorted(notes, key=lambda n: (-n[0], n[1]))

        frettes = [n[1] for n in sorted_notes]
        min_fret = min(frettes)
        max_fret = max(frettes)
        toniques = [{"corde": n[0], "frette": n[1]} for n in sorted_notes if n[3] == "1"]

        for note_seq, (corde, frette, nom_note, degre, intervalle, demi_tons) in enumerate(sorted_notes, start=1):
            svg_question = generate_svg(min_fret, corde, frette, sorted_notes, show_degrees=False)
            svg_reponse = generate_svg(min_fret, corde, frette, sorted_notes, show_degrees=True)

            box_number_tag = f"Box_{box_idx}"
            degre_tag = f"Degre_{degre}"

            # Clé d'ordre unique pour forcer le tri dans le navigateur Anki (Sort Field)
            sort_key = f"{gamme_order_prefix}_Box{box_idx:02d}_Seq{note_seq:02d}_Corde{corde}_Frette{frette}"

            note = genanki.Note(
                model=guitar_model,
                fields=[
                    gamme_name,
                    box_name,
                    str(min_fret),
                    str(max_fret),
                    str(corde),
                    str(frette),
                    json.dumps(toniques),
                    f"{degre} ({intervalle})",
                    str(demi_tons),
                    json.dumps(sorted_notes),
                    svg_question,
                    svg_reponse
                ],
                tags=[tag_gamme, box_number_tag, degre_tag]
            )
            subdeck.add_note(note)


# Génération séquentielle : 01. Pentatonique d'abord, puis 02. Gamme naturelle
populate_deck_advanced(DATA_PENTA, "Pentatonique mineure (La / A)", "01")
populate_deck_advanced(DATA_NATURELLE, "Gamme mineure naturelle (La / A)", "02")

genanki.Package(all_decks).write_to_file('degrees_manche_guitare.apkg')
print("Fichier Anki généré avec affichage des degrés sur la box au verso !")