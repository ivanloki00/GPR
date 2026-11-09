# Demo dashboard: capas de información

La demo local reúne cuatro niveles de lectura para la presentación:

1. **Descripción:** notas de corte verificadas, campus y evolución de bases de cotización.
2. **Calidad:** cobertura de notas por universidad, campus y año.
3. **Comparación:** campos detallados de U-Ranking 2024 y equivalencias propuestas entre grados y campos.
4. **Diagnóstico:** correlaciones exploratorias y ficha individual de cada grado con su estado de mapeo.

## Fuentes incorporadas

- `data/processed/notas_upv_uv_unificado_CONTRASTADAS.csv`: 109 fichas de notas, con 40 combinaciones contrastadas.
- `data/processed/cobertura_notas_anio.csv`: disponibilidad esperada y observada por campus y año.
- `data/processed/bases_cotizacion_unificadas_2021_2024_SIN_CRUCE.csv`: 40 registros de ámbitos amplios 2021–2024 y 111 campos detallados de 2024.
- `data/processed/propuesta_mapeo_grado_a_campo_sin_salarios.csv`: correspondencias candidatas sin convertirlas en equivalencias definitivas.
- `data/processed/SCRUM45_campos_subconjunto.csv`: subconjunto usado para el diagnóstico exploratorio y sensibilidad.
- `data/processed/correlaciones_notas_salarios_2024.csv`: resultados descriptivos ya calculados por el proyecto.

## Precauciones para la exposición

Las bases de cotización son un indicador anualizado de titulados afiliados por cuenta ajena a jornada completa, cuatro años después del egreso. No son salario neto ni sueldo de entrada. Las notas proceden de una fuente secundaria y las equivalencias de grado a campo requieren validación; por ello la aplicación etiqueta el cruce como exploratorio y no causal.
