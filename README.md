# GPR — Notas de corte y salarios en Valencia

## Objetivo

Estudiar la posible asociación entre las notas de corte de grados de la UPV y la UV y los indicadores salariales vinculados a sus titulaciones o ámbitos profesionales. La correlación no implica causalidad.

## Estructura

- `data/raw/`: datos de entrada originales (`.csv` y `.txt`); no modificar sus valores.
- `data/processed/`: resultados de limpieza y unificación.
- `notebooks/`: notebooks de Python para preparar y analizar los datos.
- `scripts/`: scripts reutilizables, cuando se incorporen.
- `docs/fuentes/`: fichas de fuentes, cobertura y limitaciones.
- `docs/figuras/`: gráficos exportados.
- `docs/entregables/`: documentación y presentaciones finales.

## Reproducir el archivo de notas unificado

1. Preparar Python e instalar dependencias: `python -m pip install -r requirements.txt`.
2. Arrancar Jupyter desde la raíz: `jupyter lab`.
3. Abrir `notebooks/analisis_unificacion_upv_uv.ipynb` y ejecutar todas sus celdas.
4. Comprobar el resultado en `data/processed/grados_upv_uv_unificado.csv`.

El notebook también genera:

- `data/processed/resumen_notas_grado_anio.csv`: número de notas disponibles, media,
  mediana, desviación estándar muestral e intervalo intercuartílico por universidad,
  campus, grado y año.
- `data/processed/cobertura_notas_anio.csv`: observaciones esperadas, disponibles,
  ausentes y con valor cero, además del porcentaje de cobertura por universidad,
  campus y año.

La unidad de observación del resumen es una nota de corte de un grado en un campus,
universidad y año. Los valores ausentes se mantienen como ausentes y no se
recodifican como cero.

## Datos y procedencia

- Notas de corte UPV y UV de 2022 a 2026: CSV en `data/raw/`.
- Los TXT de origen se conservan en `data/raw/`.
- Las fuentes salariales se investigan y documentan en `docs/fuentes/`.
- **Pendiente:** registrar las URL oficiales exactas y fechas de extracción originales de los CSV de notas; el ZIP inicial no las proporciona.

## Limitaciones

Los salarios y las notas de corte pueden pertenecer a cohortes y periodos distintos. Debe documentarse la correspondencia entre titulaciones, instituciones, años, unidades y medidas salariales antes de realizar comparaciones.

## Gestión del proyecto

Tareas y planificación en Jira. Primer MVP: **10 de noviembre de 2026**.

## Demo local

La demo visual se puede arrancar sin instalar dependencias adicionales:

```powershell
python app.py
```

Después abre `http://127.0.0.1:8000`. La interfaz lee los CSV revisados de
`data/processed/` en cada arranque y muestra las notas contrastadas, la serie
2021–2024 de ámbitos amplios, una comparación exploratoria de campos 2024,
la cobertura por campus/año, el mapeo de grados y las correlaciones descriptivas.
La organización de las capas y sus precauciones está documentada en
[`docs/demo_dashboard.md`](docs/demo_dashboard.md).
El enriquecimiento de ramas y la lista de fuentes pendientes está documentado en
[`docs/enriquecimiento_ramas_insercion_2024.md`](docs/enriquecimiento_ramas_insercion_2024.md).
Para detenerla, pulsa `Ctrl+C`.
