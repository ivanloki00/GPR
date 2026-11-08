# SCRUM-45 · Valores atípicos en el subconjunto validado

8 de noviembre de 2026 · Marc. Reproducible con `python scripts/scrum45_atipicos.py`.

## Qué subconjunto se ha usado

Como el mapeo definitivo de SCRUM-37/38 aún no está cerrado, se toma como subconjunto el cruce de SCRUM-42 (`SCRUM42_borrador_por_grado_NO_VALIDADO.csv`) limitado a las equivalencias por **nombre literal** o **sinónimo propuesto** con nota 2024 y cotización disponibles: **71 grados×campus en 57 campos U-Ranking**. Quedan fuera 38 filas (21 dobles grados, 13 de revisión manual y 4 pendientes de homologación), que siguen en el registro con su motivo. Si Dani cambia la lista de equivalencias válidas, basta con modificar `ESTADOS_SUBCONJUNTO` en el script y volver a ejecutarlo.

La nota usada es la **nota de 2024 de cada campus** del CSV original, no la media conjunta UPV/UV. Para la cotización la unidad es el **campo**, porque varios grados×campus comparten exactamente la misma cifra nacional y no pueden contar como observaciones independientes.

## Criterios aplicados

| Código | Variable | Grupo | Umbral / regla |
|---|---|---|---|
| N1 | Notas 2022–2026 | Todas las filas | Fuera de [5, 14] o igual a 0 |
| N2 | Notas 2022–2026 | Todas las filas | Valor idéntico los cinco años |
| N3 | Cambio interanual de nota | Todas las filas | Más de 0,5 puntos (los cambios tienen desv. típ. 0,15; 0,5 supera 3 desv. típ.) |
| N4 | Notas 2022–2026 | Todas las filas | Algún año ausente (informativo) |
| N5 | Nota 2024 | Subconjunto | Fuera de Q1 − 1,5·IQR / Q3 + 1,5·IQR |
| U1 | Mapeo | Todas las filas | Estado `REVISION_MANUAL` |
| U2 | Mapeo | Todas las filas | Varios grados distintos asignados al mismo campo |
| U3 | Mapeo | Todas las filas | El mapeo de `main` (`mapeo_carreras_cno11_final.csv`) da otro campo |
| S1 | Cotización 2024 | 57 campos | Fuera de Q1 − 1,5·IQR / Q3 + 1,5·IQR |
| S2 | Residuo cotización ~ nota | 57 campos | Residuo estandarizado mayor que 2 en valor absoluto |
| S3 | Influencia en el ajuste | 57 campos | Distancia de Cook mayor que 4/n = 0,070 |

Ninguna observación se suprime: todas quedan en `data/processed/SCRUM45_registro_atipicos.csv` con sus marcas, el detalle, la decisión y la procedencia.

## Resultados

**Anomalías en las notas.** El Doble Grado ADE + Turismo (UPV Alcoy) tiene 5,00 los cinco años: es la nota mínima de acceso, no una nota de corte competitiva, y conviene indicarlo si se muestra. Ingeniería en Tecnologías Industriales (UPV Vera) oscila 11,60 → 10,88 → 12,07 → 10,80 → 11,00, con saltos de hasta 1,27 puntos cuando el resto de grados apenas varía (el 99 % de los cambios es menor de 0,32). Hay que comprobar esa serie en la fuente antes de usarla en gráficos de evolución. Tres grados de nueva implantación tienen años ausentes, que se mantienen como ausentes. Ninguna nota está fuera de rango ni es cero, y no hay atípicos de nota 2024 dentro del subconjunto.

**Uniones erróneas o dudosas.** Las 13 equivalencias de revisión manual meten grados distintos en el mismo campo: Física e Ingeniería Física, Historia e Historia del Arte, Bellas Artes y Diseño y Tecnologías Creativas en «Diseño», Ingeniería Civil y Obras Públicas, Telemática y Telecomunicación, y Aeroespacial y su PARS. Por eso están fuera del subconjunto. Más importante: en el repositorio conviven **dos mapeos incompatibles**. El de `main`, que usa el cruce y las correlaciones subidos el 8/11, asigna 31 grados a «Derecho» (Bellas Artes, Periodismo, Magisterio, Historia…) y 29 a «Ciencias físicas, químicas y geológicas» (todas las ingenierías y Arquitectura). Esos campos no existen con ese nombre en el desglose de 111 campos de U-Ranking, de modo que casi todas las ingenierías se pierden y el resto hereda el salario de Derecho. Difiere del mapeo de SCRUM-42 en 77 filas. El cruce y la correlación de `main` no deberían presentarse hasta que se unifique el mapeo.

**Casos salariales plausibles.** Medicina (13,38; 44 153 €) es el único campo con residuo grande (2,63) y el más influyente (Cook 0,26). Bioquímica (13,05; 27 027 €), Arquitectura técnica (6,40; 34 341 €) e Ingeniería geomática (5,80; 33 696 €) también influyen en el ajuste. Ninguna cotización es atípica por la regla de Tukey. Son valores nacionales coherentes con lo que se sabe de esas profesiones, así que **se mantienen** y solo se señalan.

**Sensibilidad.** Con los 57 campos, Pearson r = 0,36 y Spearman ρ = 0,33. Sin los cuatro campos marcados, r = 0,42 y ρ = 0,42. La asociación positiva no depende de los atípicos; Medicina no la está fabricando. Es un resultado exploratorio sobre un mapeo provisional, no el resultado de SCRUM-43.

## Archivos

- `scripts/scrum45_atipicos.py`
- `data/processed/SCRUM45_registro_atipicos.csv` (109 filas)
- `data/processed/SCRUM45_campos_subconjunto.csv` (57 campos)
- `data/processed/SCRUM45_sensibilidad.csv`
- `docs/figuras/SCRUM45_dispersion_campos.png`
- `docs/figuras/SCRUM45_series_notas.png`

## Limitaciones

El mapeo sigue sin validar (SCRUM-37/38). La cotización es una base media nacional de una cohorte que egresó en 2019–20, no el salario de los admitidos en 2024 ni de titulados de UPV/UV. Las notas proceden del CSV original sin certificado de adjudicación. Las series de notas se mueven casi en paralelo entre grados, lo que conviene contrastar con la procedencia pendiente que indica el README.
