import csv
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent
PROCESSED = ROOT / "data" / "processed"
STATIC = ROOT / "dashboard"


def read_csv(filename, delimiter=";"):
    with (PROCESSED / filename).open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file, delimiter=delimiter))


def number(value):
    if value in ("", None):
        return None
    return float(value.replace(",", "."))


def build_payload():
    notes = read_csv("notas_upv_uv_unificado_CONTRASTADAS.csv")
    reference_notes = read_csv("grados_upv_uv_unificado.csv", delimiter=",")
    salaries = read_csv("bases_cotizacion_unificadas_2021_2024_SIN_CRUCE.csv")
    coverage = read_csv("cobertura_notas_anio.csv", delimiter=",")
    mapping = read_csv("propuesta_mapeo_grado_a_campo_sin_salarios.csv")
    enrichment = read_csv("enriquecimiento_ramas_insercion_2024.csv")
    exploratory = read_csv("SCRUM45_campos_subconjunto.csv")
    correlation = read_csv("correlaciones_notas_salarios_2024.csv")
    mapping_by_degree = {
        (row["Universidad"], row["Grado_original"], row["Campus"]): row
        for row in mapping
    }
    enrichment_by_degree = {
        (row["Universidad"], row["Grado"], row["Campus"]): row
        for row in enrichment
    }
    reference_by_degree = {
        (row["Universidad"], row["Grado"], row["Campus"]): row
        for row in reference_notes
    }
    university_offer = {"UPV": 5812, "UV": 9283}
    university_rows = {}
    degree_campus_counts = {}
    for row in notes:
        university_rows[row["Universidad"]] = university_rows.get(row["Universidad"], 0) + 1
        key = (row["Universidad"], row["Grado"])
        degree_campus_counts[key] = degree_campus_counts.get(key, 0) + 1

    note_rows = []
    for row in notes:
        years = {year: number(row[year]) for year in ("2022", "2023", "2024", "2025", "2026")}
        enriched = enrichment_by_degree.get(
            (row["Universidad"], row["Grado"], row["Campus"]),
            {},
        )
        reference = reference_by_degree.get(
            (row["Universidad"], row["Grado"], row["Campus"]),
            {},
        )
        verified_average = number(row["Media_verificada_2022_2026"])
        reference_average = number(
            reference.get("Media_2022_2026_Final")
            or reference.get("Media_2022_2026")
        )
        average = verified_average if verified_average is not None else reference_average
        university = row["Universidad"]
        degree_key = (university, row["Grado"])
        estimated_places = None
        if university in university_offer and university_rows[university]:
            estimated_places = (
                university_offer[university]
                * degree_campus_counts[degree_key]
                / university_rows[university]
            )
        note_rows.append(
            {
                "university": row["Universidad"],
                "degree": row["Grado"],
                "campus": row["Campus"],
                "years": years,
                "average": average,
                "averageType": "verified" if verified_average is not None else "reference_unverified",
                "referenceAverage": reference_average,
                "yearsWithData": int(row["Anos_con_dato"] or 0),
                "status": row["Estado_revision"],
                "source": row["Fuente_nota"],
                "mapping": mapping_by_degree.get(
                    (row["Universidad"], row["Grado"], row["Campus"]),
                    {},
                ).get("Campo_U_Ranking_candidato"),
                "mappingStatus": mapping_by_degree.get(
                    (row["Universidad"], row["Grado"], row["Campus"]),
                    {},
                ).get("Estado_mapeo"),
                "branch": enriched.get("Rama_conocimiento"),
                "offeredPlaces": estimated_places,
                "affiliationRate": number(enriched.get("tasa_afiliacion_2024")),
                "adequacyRate": number(enriched.get("tasa_adecuacion_2024")),
                "firstYearCotization": number(enriched.get("cotizacion_anio1_eur")),
            }
        )

    salary_rows = [
        {
            "level": row["nivel_desglose"],
            "field": row["campo_estudio"],
            "year": int(row["anio_observacion"]),
            "value": number(row["valor_eur_anual"]),
            "source": row["fuente_id"],
        }
        for row in salaries
    ]
    return {
        "notes": note_rows,
        "salaries": salary_rows,
        "coverage": [
            {
                "university": row["Universidad"],
                "campus": row["Campus"],
                "year": int(row["Anio"]),
                "expected": int(row["n_esperadas"]),
                "available": int(row["n_disponibles"]),
                "coverage": number(row["porcentaje_cobertura"]),
            }
            for row in coverage
        ],
        "exploratory": [
            {
                "field": row["campo_uranking_candidato"],
                "note": number(row["nota_media_2024"]),
                "degrees": row["grados"],
                "salary": number(row["cotizacion_2024"]),
                "influential": row["influyente"].lower() == "true",
                "decision": row["decision"],
            }
            for row in exploratory
        ],
        "correlation": [
            {
                "unit": row["unidad_analisis"],
                "observations": int(row["n_observaciones"]),
                "pearson": number(row["pearson_r"]),
                "spearman": number(row["spearman_rho"]),
                "warning": row["advertencia"],
            }
            for row in correlation
        ],
        "sources": [
            {
                "name": "Notas contrastadas",
                "detail": "UPV / UV · última adjudicación recopilada",
                "url": "https://apren.ai/selectividad-pau-3/pau-valencia-235/notas-de-corte/",
            },
            {
                "name": "Afiliación SIIU",
                "detail": "Ámbitos amplios · 2021–2024 · España",
                "url": "https://www.ciencia.gob.es/Ministerio/Estadisticas/SIIU/Afiliacion.html",
            },
            {
                "name": "U-Ranking",
                "detail": "111 campos · afiliación y adecuación · 2024 · España",
                "url": "https://www.u-ranking.es/insercion-SUE",
            },
        ],
        "universityOffer2024": {
            "UPV": 5812,
            "UV": 9283,
            "source": "https://universitats.gva.es/documents/389338055/389340612/Informe+General+Preinscripci%C3%B3n+2024+Oficial.pdf/9c474b81-14de-667f-cad9-d321cb1d43a9",
        },
    }


PAYLOAD = build_payload()


class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/data":
            body = json.dumps(PAYLOAD, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
        else:
            relative = "index.html" if path == "/" else path.lstrip("/")
            target = (STATIC / relative).resolve()
            if STATIC not in target.parents or not target.is_file():
                self.send_error(404)
                return
            body = target.read_bytes()
            content_type = "text/html; charset=utf-8" if target.suffix == ".html" else "text/css; charset=utf-8" if target.suffix == ".css" else "application/javascript; charset=utf-8"
            self.send_response(200)
            self.send_header("Content-Type", content_type)

        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8000), DashboardHandler)
    print("Dashboard disponible en http://127.0.0.1:8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
        server.server_close()
