#!/usr/bin/env python3
"""GPR (MVP1): separar fuentes SCRUM-32 y preparar SCRUM-42 SIN aprobar mapeos.

Ejecutar desde la raíz del repo: python scripts/preparar_scrum32_42.py
Solo crea archivos con prefijo SCRUM32_ o SCRUM42_; no altera los CSV de origen.
Solo usa la biblioteca estándar de Python.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path
import csv
import sys

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = DATA / "processed"
DOC = ROOT / "docs" / "fuentes"
AUDIT = ROOT / "docs" / "auditoria"

SOURCES = {
    "cotizaciones": OUT / "bases_cotizacion_unificadas_2021_2024_SIN_CRUCE.csv",
    "uranking": DATA / "raw" / "uranking_2026_111_campos_2024_ESPAÑA.csv",
    "mapeo": OUT / "propuesta_mapeo_grado_a_campo_sin_salarios.csv",
    "notas": OUT / "grados_upv_uv_unificado.csv",
}


def read_csv(file: Path) -> list[dict[str, str]]:
    if not file.exists():
        raise FileNotFoundError(f"Falta {file.relative_to(ROOT)}. Revisa que estás en la rama con los datos.")
    with file.open(encoding="utf-8-sig", newline="") as f:
        first = f.readline()
        f.seek(0)
        sep = ";" if first.count(";") > first.count(",") else ","
        return list(csv.DictReader(f, delimiter=sep))


def output_csv(path: Path, rows: list[dict], columns: list[str]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, columns, delimiter=";", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def output_md(path: Path, body: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.strip() + "\n", encoding="utf-8")


def num(s: str) -> Decimal:
    try:
        x = Decimal((s or "").strip().replace(",", "."))
    except InvalidOperation as e:
        raise ValueError(f"Importe no numérico en fuente: {s!r}") from e
    if not x.is_finite() or x < 0:
        raise ValueError(f"Importe no válido: {s!r}")
    return x


def main():
    cot = read_csv(SOURCES["cotizaciones"])
    ur = read_csv(SOURCES["uranking"])
    mp = read_csv(SOURCES["mapeo"])
    nt = read_csv(SOURCES["notas"])
    if (len(cot), len(ur), len(mp), len(nt)) != (151, 111, 109, 109):
        raise ValueError(f"Conteos inesperados: cotizaciones={len(cot)}, ranking={len(ur)}, mapeo={len(mp)}, notas={len(nt)}")

    required = ["fuente_id", "nivel_desglose", "campo_estudio", "anio_observacion", "cohorte_egreso", "anos_despues_egreso", "valor_eur_anual", "ambito_geografico", "tipo_indicador", "poblacion", "fuente_url", "fuente_primaria", "nota"]
    if not set(required).issubset(cot[0]):
        raise ValueError("La estructura de bases_cotizacion_unificadas ha cambiado")
    key_counts = Counter((r["fuente_id"],r["nivel_desglose"],r["campo_estudio"],r["anio_observacion"],r["cohorte_egreso"]) for r in cot)
    if any(n > 1 for n in key_counts.values()):
        raise ValueError("Hay duplicados EXACTOS en la clave fuente/nivel/campo/año/cohorte")
    if any(not r["fuente_url"] or not r["fuente_primaria"] or num(r["valor_eur_anual"]) <= 0 for r in cot):
        raise ValueError("Falta referencia o aparece un importe no positivo")
    if any(r["tipo_indicador"] != "base_media_cotizacion_anual" or r["ambito_geografico"] != "España" for r in cot):
        raise ValueError("La fuente contiene indicadores de tipo o territorio distintos")

    selected = [r for r in cot if r["fuente_id"] == "SIIU_DatosUni_AMBITO"]
    detailed = [r for r in cot if r["fuente_id"] == "URANKING2026_CAMPO"]
    year_counts = Counter(r["anio_observacion"] for r in selected)
    if year_counts != {"2021": 10, "2022": 10, "2023": 10, "2024": 10}:
        raise ValueError(f"La selección por año no suma 10 en cada año: {dict(year_counts)}")
    if len(detailed) != 111 or any(r["anio_observacion"] != "2024" for r in detailed):
        raise ValueError("U-Ranking detallado no son 111 campos exclusivos de 2024")
    if {r["campo_estudio"] for r in selected if r["anio_observacion"] == "2024"} != {r["campo_estudio"] for r in selected if r["anio_observacion"] == "2021"}:
        raise ValueError("Los diez campos seleccionados no coinciden entre 2021 y 2024")
    u_src = {(r["campo_estudio"],r["anio_observacion"]):r["valor_eur_anual"] for r in ur}
    for r in detailed:
        if u_src.get((r["campo_estudio"],r["anio_observacion"])) != r["valor_eur_anual"]:
            raise ValueError("El detalle U-Ranking unificado no coincide exactamente con su raw")

    # SCRUM-32: separar tablas homogéneas, sin mezclar períodos ni niveles.
    output_csv(OUT / "SCRUM32_serie_10_campos_seleccionados_2021_2024.csv", selected, required)
    output_csv(OUT / "SCRUM32_campos_detallados_2024_111.csv", detailed, required)
    year_cohorts=defaultdict(set)
    for r in cot:
        year_cohorts[(r["fuente_id"],r["nivel_desglose"],r["anio_observacion"])].add(r["cohorte_egreso"])
    summary=[]
    for (fuente,nivel,anio),cohortes in sorted(year_cohorts.items()):
        group=[r for r in cot if (r["fuente_id"],r["nivel_desglose"],r["anio_observacion"])==(fuente,nivel,anio)]
        summary.append({"fuente_id":fuente,"nivel_desglose":nivel,"anio_observacion":anio,"cohortes_egreso":"; ".join(sorted(cohortes)),"n_registros":len(group),"n_campos_distintos":len(set(x["campo_estudio"] for x in group)),"sin_valor":sum(not x["valor_eur_anual"] for x in group),"valor_min_eur_anual":str(min(num(x["valor_eur_anual"]) for x in group)),"valor_max_eur_anual":str(max(num(x["valor_eur_anual"]) for x in group)),"territorio":"España","tipo_medida":"base_media_cotizacion_anual"})
    audit_cols=["fuente_id","nivel_desglose","anio_observacion","cohortes_egreso","n_registros","n_campos_distintos","sin_valor","valor_min_eur_anual","valor_max_eur_anual","territorio","tipo_medida"]
    output_csv(AUDIT/"SCRUM32_control_de_fuentes.csv",summary,audit_cols)

    # SCRUM-42: tabla provisional usando NOTA ORIGINAL POR CAMPUS, no media conjunta.
    note_map={(r["Universidad"],r["Grado"],r["Campus"]):r for r in nt}
    mapping_keys=[(r["Universidad"],r["Grado_original"],r["Campus"]) for r in mp]
    if len(set(mapping_keys)) != len(mp):
        raise ValueError("Mapeo tiene combinaciones de universidad/grado/campus duplicadas")
    national={r["campo_estudio"]:r for r in detailed}
    repeats=Counter(r["Campo_U_Ranking_candidato"] for r in mp if r["Campo_U_Ranking_candidato"])
    out42=[]
    for r in mp:
        key=(r["Universidad"],r["Grado_original"],r["Campus"])
        n=note_map.get(key)
        if n is None:
            raise ValueError(f"Grado sin notas originales: {key}")
        campo=r["Campo_U_Ranking_candidato"]
        salary=national.get(campo) if campo else None
        if campo and not salary:
            raise ValueError(f"Campo candidato inexistente en catálogo: {campo}")
        reasons=[]
        if not campo: reasons.append("Sin campo salarial compatible propuesto")
        elif r["Estado_mapeo"]=="REVISION_MANUAL": reasons.append("Equivalencia ambigua, revisar Dani")
        elif r["Estado_mapeo"]=="SINONIMO_PROPUESTO": reasons.append("Sinónimo propuesto, confirmar Dani")
        elif r["Estado_mapeo"]=="COINCIDENCIA_NOMBRE": reasons.append("Coincidencia nominal, confirmar cobertura")
        else: reasons.append("Confirmar categoría")
        if campo and repeats[campo]>1: reasons.append("Un indicador salarial compartido por varios grados/campus")
        reasons.append("Nota de origen, sin verificación oficial de adjudicación")
        item={
            "universidad":key[0],"grado_original":key[1],"campus":key[2],
            "nota_corte_2024_original_campus":n["2024"],
            "media_temporal_2022_2026_original_campus":n["Media_2022_2026"],
            "media_conjunta_2022_2026_solo_referencia":n["Media_Conjunta_2022_2026"],
            "campo_uranking_candidato":campo,"estado_mapeo_propuesta":r["Estado_mapeo"],
            "cotizacion_2024_eur_candidata":salary["valor_eur_anual"] if salary else "",
            "anio_cotizacion":"2024" if salary else "",
            "cohorte_egreso":"2019-2020" if salary else "",
            "ambito_cotizacion":"España" if salary else "",
            "tipo_indicador":"base_media_cotizacion_anual" if salary else "",
            "fuente_cotizacion":salary["fuente_url"] if salary else "",
            "numero_registros_con_mismo_campo":repeats[campo] if campo else "",
            "apto_para_correlacion_final":"NO - pendiente validar mapeo y notas",
            "observaciones":" | ".join(reasons)
        }
        out42.append(item)
    cols42=list(out42[0])
    output_csv(OUT/"SCRUM42_borrador_por_grado_NO_VALIDADO.csv",out42,cols42)
    out42counts=Counter(r["estado_mapeo_propuesta"] for r in out42)
    count_salary=sum(bool(r["cotizacion_2024_eur_candidata"]) for r in out42)
    no_map=len(out42)-count_salary
    missing_2024=sum(not r["nota_corte_2024_original_campus"].strip() for r in out42)

    output_md(DOC/"SCRUM32_diccionario_y_control.md", f'''# SCRUM-32 — Fuentes de cotización organizadas

Fecha: 8 de noviembre de 2026. Trabajo preparado por Jose Miguel para revisión del grupo.

## Qué se ha hecho

Se han separado los 151 registros del paquete de datos sin modificar las cifras originales:

- **40 filas** de SIIU/DatosUni: **10 campos seleccionados en cada año, de 2021 a 2024**. Son cuatro promociones de egreso distintas, observadas aproximadamente cuatro años después de graduarse. **No es la serie completa de los 111 campos**.
- **111 filas** de U-Ranking: campos de estudio detallados para **2024**, cohorte de egreso **2019–2020**.

Los dos conjuntos se guardan como archivos distintos en `data/processed/` y se mantiene el CSV original unificado sin cruce (`bases_cotizacion_unificadas_2021_2024_SIN_CRUCE.csv`). **Nunca promediar todas las 151 filas**: en 2024 hay medidas que se solapan por categoría y fuente. Algunos campos tienen nombres distintos o pequeñas diferencias de agregación/redondeo.

## Archivos nuevos

- `data/processed/SCRUM32_serie_10_campos_seleccionados_2021_2024.csv`
- `data/processed/SCRUM32_campos_detallados_2024_111.csv`
- `docs/auditoria/SCRUM32_control_de_fuentes.csv`
- `scripts/preparar_scrum32_42.py` (reproduce los resultados sin instalar librerías).

## Comprobaciones

- 151 filas totales = 40 + 111; 10 registros por año en la primera fuente y 111 en U-Ranking 2024.
- Sin claves duplicadas dentro de una fuente, nivel, campo, año y cohorte.
- Sin importes vacíos ni negativos, y todos con el tipo base media de cotización anual.
- Todos los registros del paquete se etiquetan como **España**. **No son sueldos junior de Valencia**.
- La tabla detallada coincide con su CSV raw de U-Ranking 2024.

Esto comprueba coherencia interna de los archivos suministrados, **no vuelve a verificar uno por uno sus importes en las páginas oficiales**.

## Diccionario corto

| Columna | Qué significa |
|---|---|
| `fuente_id` | De qué fichero o proveedor procede el registro |
| `nivel_desglose` | Selección de 10 campos / 111 campos detallados; no son la misma tabla |
| `campo_estudio` | Categoría de estudios, no grado-carrera de la UPV/UV necesariamente |
| `anio_observacion` | Año en el que se observa el indicador laboral |
| `cohorte_egreso` | Promoción que terminó los estudios (varía entre años en la serie de 10) |
| `anos_despues_egreso` | Años transcurridos desde la graduación |
| `valor_eur_anual` | Base media anual de cotización en euros, **no salario neto** |
| `ambito_geografico` | España |
| `tipo_indicador` | Base media de cotización anual |
| `poblacion` | Personas incluidas en la estadística; excluye otras situaciones laborales |
| `fuente_url` / `fuente_primaria` | Enlaces de procedencia |

## Para quién es cada archivo

- Dani: usar **solo el archivo U-Ranking 2024 de 111 campos** para la equivalencia académica (SCRUM-37/38/35).
- Lianghao: revisar los controles y mantener INE como **contexto independiente**, no combinarlo con cotizaciones.
- Iván y Marc: usar los datos de notas por campus si presentan comparaciones de acceso. La media conjunta UPV/UV no es una nota individual.

## Qué queda para cerrar SCRUM-32 en Jira

Comprobar con el equipo la procedencia de SCRUM-30 y dejar la rama/PR revisada e integrada en GitHub. Este paquete prepara el entregable pero no certifica el cierre de la PR.

**Referencias:** https://www.u-ranking.es/insercion-laboral · https://www.ciencia.gob.es/Ministerio/Estadisticas/SIIU/Afiliacion.html · https://datosuni.com/titulacion/grado/medicina/
''')

    output_md(DOC/"SCRUM42_guia_borrador_y_pendientes.md", f'''# SCRUM-42 — Borrador para cotización por grado (no definitivo)

Fecha: 8 de noviembre de 2026. Este documento sirve para que Dani y Jose Miguel puedan cerrar el mapeo sin rehacer la tabla.

## Qué se ha preparado

Un CSV con **{len(out42)} filas**, una por **universidad + grado + campus**, conservando las notas del CSV original por campus y añadiendo el **campo U-Ranking 2024 propuesto** y su base media anual de cotización nacional como valor **candidato**.

- {count_salary} filas tienen un campo con cifra salarial *candidata*, que aún necesita validar equivalencia.
- {no_map} filas no tienen asignación suficientemente clara (incluye dobles grados y categorías pendientes).
- {missing_2024} filas carecen de nota de corte 2024 en el CSV original.
- Reparto de propuesta de mapeo: {', '.join(f'{k}: {v}' for k,v in sorted(out42counts.items()))}.

**Ojo:** las 109 filas NO son 109 observaciones salariales independientes. Varias carreras/campus comparten el mismo campo nacional y, por tanto, exactamente el mismo valor de cotización. No se puede calcular una correlación duplicando ese valor sin explicar y corregir el nivel de análisis.

## Archivo

`data/processed/SCRUM42_borrador_por_grado_NO_VALIDADO.csv`

### Cómo leer las columnas más importantes

- `nota_corte_2024_original_campus`: nota de 2024 tomada del CSV de origen, **sin certificado de adjudicación oficial**. No es la media entre UPV/UV.
- `media_temporal_2022_2026_original_campus`: media de los años de esa misma carrera/campus en el original.
- `media_conjunta_2022_2026_solo_referencia`: media compartida entre campus/universidades en el CSV antiguo. Se conserva solo para mostrar la diferencia, **no se usa como nota individual**.
- `campo_uranking_candidato`: campo académico que habría que verificar.
- `cotizacion_2024_eur_candidata`: base media anual nacional del campo, no sueldo junior de ese grado.
- `estado_mapeo_propuesta`: indica si se ha emparejado por nombre literal, sinónimo, caso dudoso o no hay equivalente.
- `numero_registros_con_mismo_campo`: ayuda a detectar que el mismo indicador salarial se repite en varias carreras/campus.
- `apto_para_correlacion_final`: por ahora es **NO para todas las filas**. No marca ninguna observación como definitivamente validada.

## Qué falta para terminar de verdad SCRUM-42

1. **Dani (SCRUM-37/38):** aprobar las equivalencias, especialmente sinónimos, manuales y dobles grados. Por ejemplo, ADE (Administración y Dirección de Empresas) → Administración y empresa es razonable, pero debe figurar como equivalencia validada.
2. **Dani (SCRUM-35):** aprobar las claves del cruce y decidir una única unidad estadística (grado, campo, campus), evitando que una sola base nacional cuente varias veces como dato independiente.
3. **Jose Miguel (SCRUM-42):** filtrar las filas aprobadas, documentar cobertura, periodo y n válido, y entregar la tabla a SCRUM-43.

No hace falta ampliar al resto de 2021–2023 para este cruce: los **111 campos detallados están solo en 2024** en el paquete entregado. No declarar ingresos futuros de estudiantes admitidos en 2024. Los graduados son de una promoción anterior.

**Referencias:** https://www.u-ranking.es/insercion-SUE · https://www.u-ranking.es/insercion-uni-campos
''')
    print('VALIDACIÓN CORRECTA')
    print('SCRUM-32: 40 filas (10 campos seleccionados × 4 años) y 111 filas detalladas (2024); 151 originales.')
    print(f'SCRUM-42: {len(out42)} filas; {count_salary} con valor candidato, {no_map} sin campo; todos PENDIENTES de validación.')
    for p in [OUT/"SCRUM32_serie_10_campos_seleccionados_2021_2024.csv",OUT/"SCRUM32_campos_detallados_2024_111.csv",OUT/"SCRUM42_borrador_por_grado_NO_VALIDADO.csv",DOC/"SCRUM32_diccionario_y_control.md",DOC/"SCRUM42_guia_borrador_y_pendientes.md",AUDIT/"SCRUM32_control_de_fuentes.csv"]:
        print('-',p.relative_to(ROOT))

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print('ERROR:',exc,file=sys.stderr)
        sys.exit(1)
