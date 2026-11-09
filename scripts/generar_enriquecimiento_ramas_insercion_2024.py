import csv
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUTPUT = PROCESSED / "enriquecimiento_ramas_insercion_2024.csv"

FIELDS = [
    "Universidad",
    "Grado",
    "Campus",
    "campo_uranking_candidato",
    "Rama_conocimiento",
    "Plazas_ofertadas_2024",
    "tasa_afiliacion_2024",
    "tasa_adecuacion_2024",
    "cotizacion_anio1_eur",
]

# U-Ranking 2024, graduates 2019-20, four years after graduation.
# Values are national field-level indicators, not campus-level observations.
INSERTION_BY_FIELD = {
    "Actividad física y del deporte": (78.6, 35.9),
    "Administración y empresa": (80.3, 42.1),
    "Arquitectura": (76.7, 73.1),
    "Arquitectura técnica": (87.0, 67.2),
    "Audiovisual, imagen y multimedia": (71.5, 31.6),
    "Biología": (72.3, 61.8),
    "Bioquímica": (76.1, 78.4),
    "Biotecnología": (75.3, 74.9),
    "Ciencia y tecnología de los alimentos": (82.3, 39.3),
    "Ciencias ambientales": (76.0, 52.8),
    "Comercio": (69.5, 27.9),
    "Conservación y restauración": (61.3, 38.8),
    "Criminología": (67.0, 21.4),
    "Derecho": (66.3, 52.3),
    "Diseño": (71.2, 37.2),
    "Economía": (77.8, 45.1),
    "Educación infantil": (76.5, 45.7),
    "Educación primaria": (79.4, 70.5),
    "Educación social": (84.0, 61.4),
    "Enfermería": (84.3, 97.6),
    "Farmacia": (85.1, 86.7),
    "Filosofía": (65.0, 58.0),
    "Finanzas y contabilidad": (81.2, 32.0),
    "Fisioterapia": (81.7, 85.2),
    "Física": (77.6, 83.2),
    "Geografía": (77.7, 39.5),
    "Historia": (61.5, 43.7),
    "Informática": (88.8, 70.2),
    "Ingeniería aeronáutica": (74.9, 86.9),
    "Ingeniería agrícola, agropecuaria y medio rural": (87.2, 71.9),
    "Ingeniería biomédica y de la salud": (75.7, 77.1),
    "Ingeniería civil": (86.0, 84.8),
    "Ingeniería de organización industrial": (88.2, 77.3),
    "Ingeniería de sonido e imagen": (88.5, 69.6),
    "Ingeniería de telecomunicación": (86.1, 77.4),
    "Ingeniería electrónica industrial y automática": (86.6, 78.3),
    "Ingeniería eléctrica": (89.3, 78.4),
    "Ingeniería en diseño industrial y desarrollo del producto": (83.0, 59.0),
    "Ingeniería en tecnologías industriales": (81.5, 78.8),
    "Ingeniería forestal y montes": (87.6, 78.3),
    "Ingeniería geomática, topografía y cartografía": (91.5, 74.0),
    "Ingeniería mecánica": (86.8, 75.5),
    "Ingeniería multimedia": (80.3, 63.1),
    "Ingeniería química industrial": (83.0, 70.9),
    "Lengua inglesa": (68.9, 59.7),
    "Lenguas modernas y aplicadas": (64.3, 50.2),
    "Lenguas y dialectos españoles": (72.5, 70.9),
    "Matemáticas": (85.1, 78.0),
    "Medicina": (95.3, 99.7),
    "Nutrición humana y dietética": (80.9, 57.8),
    "Odontología": (75.5, 96.5),
    "Pedagogía": (77.2, 47.1),
    "Periodismo": (77.0, 38.7),
    "Podología": (85.2, 80.9),
    "Política y gestión pública": (67.7, 43.3),
    "Psicología": (75.1, 64.1),
    "Química": (79.0, 64.4),
    "Relaciones laborales y recursos humanos": (80.8, 30.6),
    "Sociología": (71.2, 42.2),
    "Trabajo social": (80.2, 64.0),
    "Traducción e interpretación": (64.2, 53.7),
    "Turismo": (71.6, 17.0),
    "Óptica y optometría": (88.8, 90.8),
}


def read_csv(filename, delimiter=";"):
    with (PROCESSED / filename).open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file, delimiter=delimiter))


def plain(text):
    normalized = unicodedata.normalize("NFKD", text or "")
    return "".join(char for char in normalized if not unicodedata.combining(char)).lower()


def classify_branch(degree):
    """Assign one SIIU branch using the degree name; mixed degrees use a stable priority."""
    value = plain(degree)
    if any(term in value for term in ("medicina", "enfermeria", "farmacia", "fisioterapia", "odontologia", "podologia", "psicologia", "nutricion", "optica", "biomedica")):
        return "Ciencias de la Salud"
    if any(term in value for term in ("ingenier", "arquitect", "datos", "informatica", "telecom", "telematica", "multimedia", "matematicas", "fisica")):
        return "Ingeniería y Arquitectura"
    if any(term in value for term in ("administracion", "empresa", "economia", "derecho", "politic", "criminologia", "sociologia", "turismo", "finanzas", "contabilidad", "laborales", "trabajo social", "educacion social")):
        return "Ciencias Sociales y Jurídicas"
    if any(term in value for term in ("biolog", "bioquim", "biotecnolog", "quimica", "ambiental", "ciencias del mar", "alimentos", "geografia")):
        return "Ciencias"
    return "Artes y Humanidades"


def main():
    notes = read_csv("notas_upv_uv_unificado_CONTRASTADAS.csv")
    mappings = read_csv("propuesta_mapeo_grado_a_campo_sin_salarios.csv")
    mapping_by_key = {
        (row["Universidad"], row["Grado_original"], row["Campus"]): row
        for row in mappings
    }

    rows = []
    for note in notes:
        mapping = mapping_by_key.get(
            (note["Universidad"], note["Grado"], note["Campus"]),
            {},
        )
        affiliation, adequacy = INSERTION_BY_FIELD.get(
            mapping.get("Campo_U_Ranking_candidato"),
            (None, None),
        )
        rows.append(
            {
                "Universidad": note["Universidad"],
                "Grado": note["Grado"],
                "Campus": note["Campus"],
                "campo_uranking_candidato": mapping.get("Campo_U_Ranking_candidato", ""),
                "Rama_conocimiento": classify_branch(note["Grado"]),
                # These measures are intentionally empty until an official table is imported.
                "Plazas_ofertadas_2024": "",
                "tasa_afiliacion_2024": affiliation,
                "tasa_adecuacion_2024": adequacy,
                "cotizacion_anio1_eur": "",
            }
        )

    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generadas {len(rows)} filas en {OUTPUT}")


if __name__ == "__main__":
    main()
