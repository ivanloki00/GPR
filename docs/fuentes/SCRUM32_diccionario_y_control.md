# SCRUM-32 — Fuentes de cotización organizadas

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
