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

## Datos y procedencia

- Notas de corte UPV y UV de 2022 a 2026: CSV en `data/raw/`.
- Los TXT de origen se conservan en `data/raw/`.
- Las fuentes salariales se investigan y documentan en `docs/fuentes/`.
- **Pendiente:** registrar las URL oficiales exactas y fechas de extracción originales de los CSV de notas; el ZIP inicial no las proporciona.

## Limitaciones

Los salarios y las notas de corte pueden pertenecer a cohortes y periodos distintos. Debe documentarse la correspondencia entre titulaciones, instituciones, años, unidades y medidas salariales antes de realizar comparaciones.

## Gestión del proyecto

Tareas y planificación en Jira. Primer MVP: **10 de noviembre de 2026**.
