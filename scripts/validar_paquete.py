from pathlib import Path
import csv
p=Path(__file__).resolve().parents[1]
def read(relative):
 with open(p/relative,encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f,delimiter=";"))
notes=read("data/processed/notas_upv_uv_unificado_CONTRASTADAS.csv")
assert len(notes)==109
assert len({(r["Universidad"],r["Grado"],r["Campus"]) for r in notes})==109
assert sum(r["Estado_revision"]=="CONTRASTADO_SECUNDARIA" for r in notes)==40
for r in notes:
 for y in range(2022,2027):
  if r[str(y)]: assert 5<=float(r[str(y)])<=14, (r["Grado"],y)
 if r["Estado_revision"]=="SIN_CONTRASTE_EXCLUIDO": assert not any(r[str(y)] for y in range(2022,2027))
salary=read("data/processed/bases_cotizacion_unificadas_2021_2024_SIN_CRUCE.csv")
assert len(salary)==151
assert sum(r["fuente_id"]=="URANKING2026_CAMPO" for r in salary)==111
assert sum(r["fuente_id"]=="SIIU_DatosUni_AMBITO" for r in salary)==40
assert all(float(r["valor_eur_anual"])>0 for r in salary)
assert len({(r["fuente_id"],r["campo_estudio"],r["anio_observacion"]) for r in salary})==151
print("OK: 109 fichas (40 contrastadas), 151 registros de cotización, sin duplicados ni notas fuera de escala.")
