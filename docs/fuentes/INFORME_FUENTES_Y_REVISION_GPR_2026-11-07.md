# Informe de fuentes y revisión de datos — GPR
**Fecha:** 7 de noviembre de 2026  
**Proyecto:** Notas de corte y salarios en Valencia (UPV / UV)  
**Objetivo:** dejar archivos auditables para que el grupo siga trabajando. **No se han calculado correlaciones ni realizado el cruce final grado–ingreso.**

## 1. Qué hemos podido obtener

El fichero original tiene **109 filas**, correspondientes a 91 nombres de grado distintos (incluidos dobles grados). Su información sobre notas de corte se ha comparado con tablas públicas de la última adjudicación recopiladas por AprenAI. Se han localizado series para **40 combinaciones de grado, universidad y campus**; son **199 valores con fuente** (hay un caso sin dato en 2026). Los otros **69 casos permanecen en blanco en la tabla contrastada**, no porque se haya comprobado que no existan, sino porque **no ha dado tiempo a verificar sus cifras**. Se mantienen íntegros los originales en `docs/auditoria/`.

Las **199 cifras contrastadas difieren** del CSV inicial. Esto obliga a **no usar el CSV original como verdad**. En la tabla contrastada, cada registro enlaza su fuente y el promedio solo se calcula con los años observados. Los campos no contrastados están vacíos: no se han rellenado con valores inventados.

**Aviso sobre las notas:** AprenAI es un recopilador externo que identifica su serie como **última lista**. No es el fichero original de la Generalitat. La UPV publica para Ciencia de Datos una nota 2026/27 de **10,59** en su ficha oficial, mientras que la última lista de AprenAI indica **9,198**: pueden referirse a adjudicaciones distintas. Para una comparación definitiva, se debe fijar **una convocatoria y una lista homogénea** y contrastarla con los PDF originales de admisión. Mantengo ambas cifras como evidencia de la discrepancia y no mezclo automáticamente las dos listas.

## 2. Qué datos de ingresos hay realmente y en qué años

Se aportan **cinco CSV individuales**: uno por año 2021, 2022, 2023 y 2024, además del fichero específico de **111 campos de U-Ranking (solo 2024)**. Y hay un **CSV conjunto de 151 registros** con la columna `nivel_desglose` para que los valores nunca se confundan.

| Origen y detalle | Periodo | Cohortes y observación | Cantidad | Ámbito |
|---|---|---|---:|---|
| SIIU / DatosUni, **ámbito amplio** | 2021–2024 | Diferentes cohortes: 2016–17 a 2019–20, medidas 4 años después del egreso | 10 ámbitos × 4 = 40 filas | España |
| U-Ranking 2026, **campo detallado** | Solo 2024 | Una cohorte: graduados 2019–20, 4 años después | 111 campos | España |

Son **bases medias de cotización anualizadas de titulados afiliados por cuenta ajena**, utilizadas como indicador aproximado de ingresos: **no es salario neto, sueldo de entrada ni salario por campus o provincia**. Los datos de los distintos niveles no deben sumarse ni promediarse entre sí. Por ejemplo, el valor de «Administración y gestión de empresas» del SIIU no tiene por qué coincidir con el campo «Administración y empresa» de U-Ranking: el grado de agregación no es idéntico.

Fuentes:
- Ministerio (SIIU/AFIL): https://www.ciencia.gob.es/Ministerio/Estadisticas/SIIU/Afiliacion.html
- Tablas UNIVbase: https://estadisticas.ciencia.gob.es/dynPx/inebase/index.htm?L=0&file=pcaxis&path=%2FUniversitaria%2FAFIL%2FGRADO_BCM%2F&type=pcaxis
- U-Ranking 2026 por campo: https://www.u-ranking.es/insercion-SUE
- U-Ranking por universidad (consulta selectiva, con secreto estadístico): https://www.u-ranking.es/insercion-uni-campos
- Series históricas por ámbito SIIU reproducidas por DatosUni: hay una URL específica de procedencia en **cada fila** de los CSV.

**Años recomendados para el MVP:** centrar la comparación de notas en **2022–2024**, únicamente cuando estén verificadas, y usar **2024** para el indicador de inserción laboral por campo (2019–20 cohortes de egresados). Los ingresos 2021–2023 sirven para ver tendencias **a nivel de ámbitos amplios**, pero NO permiten fabricar un sueldo histórico detallado para las 111 carreras. Se incluyen porque el grupo pidió los años disponibles, no como falsas observaciones del mismo grupo de estudiantes.

## 3. Nombres de grados y equivalencias propuestas

`propuesta_mapeo_grado_a_campo_sin_salarios.csv` conserva **los 109 registros** con el nombre original del grado, el campus y un posible campo de U-Ranking. Hay 24 coincidencias literales, 47 sinónimos razonables, 13 equivalencias que exigen revisión manual y 21 dobles grados sin un campo único (4 sin candidato). **No incorpora importes**, para que el equipo responsable valide las claves antes de cruzarlas.

Ejemplo: «Administración y Dirección de Empresas (ADE)» corresponde al candidato «Administración y empresa». Otros casos como Ciencia de Datos, Ingeniería Química, Bellas Artes, Historia del Arte y los dobles grados deben estudiarse antes de asignarles una remuneración. No asignar automáticamente a un doble grado el salario de uno de sus componentes.

**En caso de similitud por campo, indicar siempre que el valor salarial se refiere al ámbito nacional y no es un valor individual de ese título en Valencia.** Si varios grados comparten el mismo campo salarial, en una correlación no se deben contar sus ingresos como 2 observaciones independientes sin agrupar o considerar la dependencia.

## 4. Qué significan las columnas

**Notas** (`notas_*_CONTRASTADAS.csv`): `Universidad`, `Grado`, `Campus`; `2022`…`2026` (puntos de admisión, vacíos si no contrastados); `Media_verificada_2022_2026` (media solo de valores contrastados); `Anos_con_dato`; `Estado_revision`; `Fuente_nota` (URL); `Criterio_lista`; `Observaciones`. Un registro = grado × universidad × campus. Los cinco años corresponden a cursos de acceso 2022/23 a 2026/27.

**Salarios** (`bases_cotizacion_*.csv`): `fuente_id`, `nivel_desglose`, `campo_estudio`, `anio_observacion`, `cohorte_egreso`, `anos_despues_egreso`, `valor_eur_anual`, `ambito_geografico`, `tipo_indicador`, `poblacion`, `fuente_url`, `fuente_primaria`, `nota`. Los datos son distintos de una encuesta de salarios del INE; no usar la misma etiqueta para medidas incompatibles.

**Auditoría** (`auditoria_nota_original_vs_contrastada.csv`): una fila por grado × campus × año, valor antiguo, valor revisado, diferencia y fuente. El valor anterior no se considera validado. El archivo es necesario para justificar los cambios al profesor y para poder recuperar la versión inicial.

## 5. Qué haría el equipo de aquí al 10 de noviembre

1. **Iván (notas):** priorizar comprobar el subconjunto de 40 series con primeras/últimas listas **oficiales** de Generalitat; no dar por fiable el histórico original. Acordar si se usa la última adjudicación o la primera y mantenerlo todos los años.
2. **Dani (mapeo/cruce):** revisar el fichero de equivalencias. Elegir el indicador 2024 U-Ranking para un contraste **exploratorio por campo** y registrar cuánto coincide de verdad con UPV/UV. No calcular Pearson/Spearman si faltan observaciones independientes o las notas son insuficientemente fiables.
3. **Jose Miguel (fuentes):** facilitar los CSV salariales 2021–24 y el archivo 2024 de 111 campos con su documentación; no mezclar indiscriminadamente SIIU ámbito e INE por ocupación. La serie regional INE 2018–24 original es un contexto distinto.
4. **Marc / Lianghao:** preparar visualizaciones descriptivas, nota por título/sede y evolución por ámbito salarial. Si el cruce completo queda corto, presentar una comparación exploratoria limitada y las restricciones metodológicas claramente.

**No he cambiado ni eliminado cifras del repositorio GitHub**. Esta entrega es una propuesta auditada para que el equipo la incorpore revisándola en una rama. No conviene sustituir automáticamente `grados_upv_uv_unificado.csv` por los nuevos resultados antes de acordar la política de adjudicaciones.
