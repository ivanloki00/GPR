# Paquete de datos revisados — GPR (7 noviembre 2026)

ESTA ENTREGA ES UNA REVISIÓN PARCIAL CON TRAZABILIDAD; NO ELIMINA LOS ORIGINALES DEL REPOSITORIO.

- `data/raw/bases_cotizacion_2021_ESPAÑA.csv` ... `2024`: 10 ámbitos de estudio SIIU por año y en 2024 también los 111 campos de U-Ranking (distinguir `nivel_desglose`).
- `data/raw/uranking_2026_111_campos_2024_ESPAÑA.csv`: solo 111 campos 2024.
- `data/processed/bases_cotizacion_unificadas_2021_2024_SIN_CRUCE.csv`: unión vertical de esos 151 registros, SIN emparejar notas.
- `data/raw/notas_upv_2022_2026_CONTRASTADAS.csv`, `notas_uv_...`: catálogos originales completos, valores únicamente cuando haya fuente contrastada (externa). Los demás están VACÍOS, no aprobados.
- `data/processed/notas_upv_uv_unificado_CONTRASTADAS.csv`: unión de 109 registros con medias recalculadas solo entre años contrastados.
- `data/processed/notas_SUBCONJUNTO_40_filas_para_revision.csv`: 40 combinaciones con fuente para avanzar rápido en el MVP.
- `data/processed/propuesta_mapeo_grado_a_campo_sin_salarios.csv`: equivalencias propuestas, sin salarios mezclados.
- `docs/auditoria`: copias originales de los CSV y comparación fila-a-fila, nunca sustituir silenciosamente.
- `docs/fuentes/INFORME_FUENTES_Y_REVISION_GPR_2026-11-07.md`: explicación con URLs, definiciones y riesgos.
- `scripts/validar_paquete.py`: comprueba estructura, conteos, claves y límites de notas; ejecutar `python scripts/validar_paquete.py` desde la raíz del paquete.

**CSV UTF-8 con BOM, separados por punto y coma; punto como decimal.** En Excel seleccionar delimitador `;`, decimal `.` si se importa como número (según configuración regional).

**MUY IMPORTANTE**: `AprenAI` afirma reproducir últimas listas, pero NO es Generalitat. El dato oficial inicial 2026 de UPV Ciencia de Datos difiere de la última adjudicación recopilada. La política de fechas/convocatorias debe acordarse y verificarse oficialmente antes del análisis final. Los datos de SIIU 2021–23 son ámbitos amplios; en 2024 existe otra serie de 111 campos detallados. No son la misma clasificación.
