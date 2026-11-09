# Enriquecimiento de ramas e inserción 2024

El archivo [`data/processed/enriquecimiento_ramas_insercion_2024.csv`](../data/processed/enriquecimiento_ramas_insercion_2024.csv) conserva las claves exactas `Universidad`, `Grado` y `Campus` de las notas contrastadas y añade el campo candidato de U-Ranking y una rama SIIU.

La rama se asigna a partir del nombre del grado. En dobles grados se aplica una prioridad estable para obtener una sola rama, por lo que debe considerarse una clasificación operativa para la demo y no una codificación oficial de cada plan de estudios.

Las tasas de afiliación y adecuación se han incorporado para 84 de las 109 fichas, emparejándolas con el `campo_uranking_candidato` y usando los indicadores nacionales de U-Ranking 2024 (cohorte 2019-20, cuatro años después del egreso). No son datos específicos de campus.

Las plazas por grado que muestra la demo son una **estimación proporcional**: el total oficial de cada universidad se reparte según el número de campus en los que aparece cada grado. No es el dato oficial desagregado por titulación y se etiqueta como estimación en la interfaz. La cotización al primer año sigue vacía porque no existe en los CSV locales revisados.

Las fuentes oficiales que deben importarse para completar esas columnas son:

- Afiliación: <https://estadisticas.universidades.gob.es/jaxiPx/files/_px/es/csv_c/Universitaria/Insercion_laboral/2024/GRADO/CAP1_TAS/l0/Afiliacion_Tasa_Sexo_Campo_Grado_Tot.px>
- Base media de cotización: <https://estadisticas.universidades.gob.es/jaxiPx/files/_px/es/csv_c/Universitaria/Insercion_laboral/2024/GRADO/CAP6_BMC/l0/Base_cotizacion_Edad_Campo_Grado_Total.px>
- Consulta U-Ranking: <https://www.u-ranking.es/insercion-uni-campos>
- Indicadores nacionales por campo: <https://www.u-ranking.es/insercion-SUE>

Para regenerar el archivo:

```powershell
python scripts/generar_enriquecimiento_ramas_insercion_2024.py
```
