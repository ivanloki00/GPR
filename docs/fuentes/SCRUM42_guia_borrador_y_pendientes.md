# SCRUM-42 — Borrador para cotización por grado (no definitivo)

Fecha: 8 de noviembre de 2026. Este documento sirve para que Dani y Jose Miguel puedan cerrar el mapeo sin rehacer la tabla.

## Qué se ha preparado

Un CSV con **109 filas**, una por **universidad + grado + campus**, conservando las notas del CSV original por campus y añadiendo el **campo U-Ranking 2024 propuesto** y su base media anual de cotización nacional como valor **candidato**.

- 84 filas tienen un campo con cifra salarial *candidata*, que aún necesita validar equivalencia.
- 25 filas no tienen asignación suficientemente clara (incluye dobles grados y categorías pendientes).
- 2 filas carecen de nota de corte 2024 en el CSV original.
- Reparto de propuesta de mapeo: COINCIDENCIA_NOMBRE: 24, DOBLE_GRADO_SIN_EQUIVALENTE: 21, PENDIENTE_HOMOLOGACION: 4, REVISION_MANUAL: 13, SINONIMO_PROPUESTO: 47.

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
