# Entregables SCRUM-32 y avance SCRUM-42 — GPR

8 de noviembre de 2026. Preparados para la revisión del grupo antes de la presentación del 10 de noviembre.

## Qué está preparado

**SCRUM-32 (Jose Miguel):** he separado y comprobado las bases de cotización ya recogidas. Hay 40 registros de diez campos seleccionados entre 2021 y 2024 y 111 campos detallados en 2024. Los registros están separados en dos CSV. También hay un control de calidad y un diccionario sencillo. Los archivos de origen no se modifican. **No se mezclan con los salarios regionales del INE.** Falta que se integren y validen en GitHub y se confirme la procedencia de SCRUM-30.

**SCRUM-42 (Jose Miguel):** he preparado una tabla provisional de 109 grados/campus con las notas originales por campus y los campos U-Ranking candidatos. De esas 109 filas, 84 tienen un importe nacional propuesto; 25 quedan sin valor. **Esto no significa que existan 84 equivalencias aprobadas.** Dani debe validar la correspondencia y la unidad de análisis antes de usar los datos para calcular una correlación. El campo `apto_para_correlacion_final` está en `NO` para todas las filas hasta completar ese paso.

## Archivos que debe mirar cada compañero

- **Jose Miguel:** `docs/fuentes/SCRUM32_diccionario_y_control.md` y `docs/fuentes/SCRUM42_guia_borrador_y_pendientes.md`.
- **Dani:** `data/processed/SCRUM42_borrador_por_grado_NO_VALIDADO.csv` para revisar las equivalencias y preparar el cruce definitivo en SCRUM-35/37/38.
- **Lianghao:** `docs/auditoria/SCRUM32_control_de_fuentes.csv` y las dos tablas separadas para verificar unidades, nulos y duplicados en SCRUM-34.
- **Marc:** puede explicar en la presentación las fuentes, la metodología, los límites y qué parte del cruce está validada.

## Reproducir los resultados

Desde la raíz del repositorio, con los archivos de la PR #2 disponibles:

```
python scripts/preparar_scrum32_42.py
```

No hacen falta librerías adicionales. El script **no edita** los CSV originales; solo vuelve a generar los archivos con prefijos `SCRUM32_` y `SCRUM42_`.

## Precauciones metodológicas

1. El importe de U-Ranking 2024 es una **base media anual de cotización en España**, no el salario de un recién graduado de la UPV/UV. La cohorte se graduó en 2019–2020.
2. Las cifras de 2021–2024 en los diez campos corresponden a **promociones de egreso distintas**, no al seguimiento de una única promoción. No se debe hablar de evolución de los ingresos de las mismas personas.
3. Las notas originales de 2024 pertenecen a campus concretos; la columna de **media conjunta UPV/UV** no se usa como nota individual.
4. Las diferencias entre las notas originales y el recopilador secundario **no prueban** por sí solas que el CSV original sea incorrecto. SCRUM-71 se eliminó por decisión del grupo; mantener la limitación explícita.
5. El valor de un campo nacional puede repetirse en varios grados/campus. **No usar directamente las 109 filas como observaciones independientes** en una correlación.

## Estado final

- SCRUM-32: archivo y documentación preparados para revisión. Falta integrar la nueva entrega y comprobar la fuente con SCRUM-30.
- SCRUM-42: borrador con importes candidatos y exclusiones. **Pendiente de Dani (SCRUM-35/37/38)** para cerrarla como resultado analítico.
- No se ha generado ninguna correlación ni se han asignado salarios ficticios a dobles grados.
