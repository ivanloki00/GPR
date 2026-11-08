# MEMORY.md — Contexto compartido del proyecto GPR

> **Última actualización:** 7 de noviembre de 2026.  
> **Para quién:** cualquier miembro del equipo y cualquier IA (Claude, ChatGPT, etc.) que vaya a ayudar con el proyecto.  
> **Importante:** este documento recoge el contexto y las decisiones conocidas, pero **el estado actual de los archivos se comprueba en GitHub y el de las tareas en Jira**. No asumir que una PR se ha fusionado ni que una tarea está terminada solo por leer esta memoria.

## 1. Resumen rápido

**Asignatura:** GPR — Gestión de Proyectos, Universitat Politècnica de València.  
**Nombre del proyecto:** *Notas de corte y salarios Valencia*.  
**Pregunta principal:** ¿Las titulaciones con notas de corte más altas tienden a estar asociadas con mejores indicadores de ingresos laborales?  
**Universidades estudiadas:** Universitat Politècnica de València (UPV) y Universitat de València (UV).  
**Primer MVP/presentación:** **martes 10 de noviembre de 2026**.  
**Repositorio:** https://github.com/ivanloki00/GPR  
**Jira:** https://4tocddgpr.atlassian.net/ — proyecto **SCRUM**.

**El proyecto NO ha cambiado de tema.** Se ha ajustado la fuente y la formulación de la variable laboral, porque los salarios del INE no se pueden atribuir sin más a cada carrera. Para el primer MVP se plantea una comparación **exploratoria** entre notas de corte de grados UPV/UV e **indicadores de base media anual de cotización en España por campo de estudio en 2024**. El INE sirve como contexto regional, no como salario de cada grado.

**No se ha completado todavía el cruce definitivo grado–ingresos ni hay correlaciones finales verificadas.** Las equivalencias de títulos y campos deben revisarse antes de calcularlas. Si no hay muestra comparable suficiente, el MVP presentará resultados descriptivos, cobertura y limitaciones, sin inventar coeficientes.

## 2. Personas y reparto de responsabilidades

| Persona | Área habitual / tareas clave |
|---|---|
| **Jose Miguel (Miguelinchen en GitHub)** | Fuentes salariales y documentación; SCRUM-26 y 29 terminadas; SCRUM-32 (organizar cotizaciones), SCRUM-42 (preparar indicador laboral por grado). Ha reorganizado el repositorio y publicado el paquete de revisión en una PR. |
| **Iván Navarro** | Extracción original de notas UPV/UV, limpieza de notas, estadísticos y comparativa UPV–UV (SCRUM-11, 12, 33, 39 y 41); también exclusiones/outliers en SCRUM-46. |
| **Dani (Daniel Herran)** | Correspondencias entre titulaciones y campos salariales, validación del mapeo, cruce de tablas, asociación estadística (SCRUM-30, 35, 37, 38 y 43). |
| **Lianghao Zhan** | Control de calidad de datos salariales, evolución de notas y visualizaciones (SCRUM-34, 40 y 44). Ya preparó datos INE de contexto regional y gráficos V1. |
| **Marc Fernández** | Normalización de denominaciones/salidas, prototipo, presentación, demo y ensayo (SCRUM-36, 45, 60, 61 y 62). |

La asignación definitiva y el estado de cada incidencia se consultan en Jira. **No mover tareas ni modificar GitHub sin acordarlo con el grupo**.

## 3. Estructura del repositorio y cómo trabajar

La estructura base del repositorio es:

```text
GPR/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/             # Datos de entrada: nunca sobrescribir originales sin respaldo
│   └── processed/       # Unificados, resúmenes y resultados transformados
├── notebooks/           # Notebooks Jupyter
├── scripts/             # Scripts de validación y procesamiento
└── docs/
    ├── fuentes/         # Investigaciones, metodología y referencias
    ├── auditoria/       # Copias originales y comparaciones de versiones
    ├── figuras/         # Gráficos exportados
    └── entregables/     # Presentaciones y memorias
```

### Ramas y Pull Requests

- `main`: versión compartida del proyecto; contiene, entre otros, `notebooks/analisis_unificacion_upv_uv.ipynb`, los CSV originales, `README.md` y archivos de estadísticos iniciales.
- **PR #1**, ya fusionada: reorganización de carpetas y documentación del repositorio.
- **PR #2 — revisión de datos:** https://github.com/ivanloki00/GPR/pull/2 . Rama: `data/revision-07-nov`; commit inicial `0d7ffc9`, 20 archivos nuevos. **Última comprobación visual:** la PR estaba **abierta y sin conflictos**, pero **no se ha verificado posteriormente si se ha fusionado**. Comprobarlo antes de trabajar; no asumir que los archivos ya estén en `main`.
- Los 20 archivos de la PR #2 están **organizados en subcarpetas** (`data/raw`, `data/processed`, `docs/auditoria`, `docs/fuentes`, `scripts`), no son 20 archivos sueltos en la raíz.
- `LEEME_PRIMERO.md`, en la PR #2, explica cómo interpretar el paquete.

**Regla:** nunca reemplazar directamente los originales. Trabajar sobre una rama, comprobar los cambios y compartir una PR; conservar originales y procedencia para auditar resultados. La PR #2 debe ser revisada por los responsables de notas y mapeo antes de fusionarla.

## 4. Datos de notas de corte: 2022–2026

### 4.1. Dataset original

Archivos originales en `data/raw/`:

- `grados_upv_notas_corte_2022_2026.csv`
- `grados_uv_notas_corte_2022_2026.csv`
- `grados_upv_uv_unificado.csv` en `data/processed/`

**Tamaño:** 109 filas (51 UPV y 58 UV), con **91 nombres distintos de grado**. Cada fila representa una combinación **universidad × grado × campus**; no son 109 grados únicos. Incluye notas para los cursos de acceso indicados como 2022–2026, con algunos años ausentes.

El archivo unificado original tiene, entre otras, estas columnas:

- `Universidad`, `Grado`, `Campus`: identifican el registro.
- `2022`, `2023`, `2024`, `2025`, `2026`: **notas de un campus y universidad concretos** según el CSV original.
- `Media_2022_2026`: media temporal de las notas de **esa fila/campus**.
- `Coincidencia`: «Común» o «Exclusivo» según aparezca en varias universidades.
- `Media_Conjunta_2022_2026`: media compartida calculada para determinados grados comunes entre UPV y UV (y sus sedes).
- `Media_2022_2026_Final`: en grados comunes puede repetir la media conjunta; **no necesariamente es la nota individual de ese campus**.

**Ejemplo confirmado en el CSV — ADE:**

| Grado/campus | `Media_2022_2026` individual | `Media_2022_2026_Final` |
|---|---:|---:|
| ADE UPV Alcoy | 8,35 | 9,53 |
| ADE UPV Vera | 10,65 | 9,53 |
| ADE UV Ontinyent | 9,01 | 9,53 |
| ADE UV Tarongers | 10,11 | 9,53 |

Ese **9,53 es una media conjunta calculada**, no una nota oficial de acceso para cada uno de los cuatro campus. Comparar 9,53 con una nota oficial individual y concluir que la fuente es errónea sería incorrecto. Para comparar sedes se necesitan valores de campus; para comparar por grado hay que fijar **una regla de agregación coherente**, sin duplicar observaciones.

**Equivalencia de nombres:** «ADE» = «Administración y Dirección de Empresas». Para U-Ranking el campo candidato es «Administración y empresa». Es una equivalencia de denominación/categoría que se debe documentar, no un salario asignado automáticamente.

### 4.2. Revisión de notas y DECISIÓN NUEVA DEL EQUIPO sobre SCRUM-71

En la revisión del 7/11 se preparó una comparación con un recopilador externo de notas de últimas adjudicaciones (AprenAI):

- 40 combinaciones de grado × universidad × campus con información secundaria; 199 notas anuales contrastadas y 69 combinaciones sin contraste en el nuevo fichero.
- Los 199 valores difieren de los valores iniciales comparados; **esta diferencia no demuestra que los 199 valores originales fueran erróneos**. Pueden intervenir distintas adjudicaciones (primera/última), criterios de agregación, sedes y fuente.
- La revisión secundaria **no es una certificación oficial**, ni autoriza a sustituir indiscriminadamente los CSV originales.

**Decisión del grupo (7/11/2026): ELIMINAR SCRUM-71.** Se había creado para verificar una muestra de notas oficiales, pero el equipo detectó que parte de los desacuerdos venía de comparar datos de distinto nivel, especialmente **medias conjuntas UPV/UV frente a notas individuales de campus**. Se decidió no continuar esa tarea separada. **Comprobado en Jira: SCRUM-71 ya no existe (404).**

**Aclaración crucial para cualquier IA:** eliminar SCRUM-71 **no implica** que las notas de 2022–2026 estén completamente verificadas ni que toda discrepancia anual se explique por la media conjunta. El ejemplo anterior demuestra que **la columna final es un promedio**, mientras que las columnas anuales del CSV original son otra cosa. Antes de rehacer gráficos o cruzar datos, distinguir exactamente qué columna se usa y cuál es su unidad de observación. No volver a crear SCRUM-71 por iniciativa propia; si se necesita un control concreto, discutirlo con el equipo dentro de las tareas ya existentes.

### 4.3. Archivos de auditoría y revisión (PR #2)

Se conservan para consulta y trazabilidad, NO como sustitución automática:

- `docs/auditoria/grados_upv_notas_corte_2022_2026_ORIGINAL_SIN_VERIFICAR.csv`
- `docs/auditoria/grados_uv_notas_corte_2022_2026_ORIGINAL_SIN_VERIFICAR.csv`
- `docs/auditoria/grados_upv_uv_unificado_ORIGINAL_SIN_VERIFICAR.csv`
- `docs/auditoria/auditoria_nota_original_vs_contrastada.csv`
- `data/raw/notas_upv_2022_2026_CONTRASTADAS.csv`
- `data/raw/notas_uv_2022_2026_CONTRASTADAS.csv`
- `data/processed/notas_upv_uv_unificado_CONTRASTADAS.csv`
- `data/processed/notas_SUBCONJUNTO_40_filas_para_revision.csv`

**No mezclar** `Media_2022_2026`, `Media_Conjunta_2022_2026`, `Media_2022_2026_Final` ni una nota anual como si significaran lo mismo. **No rellenar nulos por cero**. Los resultados basados en el conjunto anterior son **V1**, y pueden necesitar revisión si se cambia la columna, regla de agregación o fuente que se utiliza.

## 5. Datos de salarios y cotizaciones: qué se ha conseguido realmente

### 5.1. Fuente principal propuesta: SIIU / U-Ranking

Los indicadores disponibles son **bases medias de cotización anual de personas tituladas**, generalmente trabajadoras por cuenta ajena de la población cubierta por la fuente. **NO** son salarios netos, sueldos de primer empleo ni remuneraciones de una persona concreta, y **NO** miden necesariamente Valencia ni los titulados de UPV/UV por separado.

| Fuente/nivel | Años de observación | Nivel de detalle | Ámbito | Cohortes |
|---|---|---|---|---|
| SIIU / DatosUni | **2021, 2022, 2023 y 2024** | **10 ámbitos generales por año** (40 registros) | España | Cohortes egresadas de 2016–17 a 2019–20, observadas cuatro años después |
| U-Ranking 2026 | **2024 solamente** | **111 campos de estudio** (111 registros) | España | Graduados 2019–20, observados cuatro años después |
| INE — Encuesta de Estructura Salarial | **2018–2024** | Media salarial de la Comunitat Valenciana (y otros desgloses según tabla) | CCAA | Asalariados encuestados; no cohorte por grado |

**Total conjunto preparado:** 40 + 111 = **151 registros**, pero **NO 151 grados ni una serie de 111 campos para 2021–2024**. El nivel de desglose se conserva mediante `nivel_desglose`. En 2024 hay dos niveles en paralelo, no dos medidas intercambiables.

**Principales archivos de la PR #2:**

- `data/raw/bases_cotizacion_2021_ESPAÑA.csv`
- `data/raw/bases_cotizacion_2022_ESPAÑA.csv`
- `data/raw/bases_cotizacion_2023_ESPAÑA.csv`
- `data/raw/bases_cotizacion_2024_ESPAÑA.csv` (10 ámbitos generales + 111 campos)
- `data/raw/uranking_2026_111_campos_2024_ESPAÑA.csv` (solo campos detallados)
- `data/processed/bases_cotizacion_unificadas_2021_2024_SIN_CRUCE.csv` (151 filas, **sin** unir con notas de corte)
- `docs/fuentes/INFORME_FUENTES_Y_REVISION_GPR_2026-11-07.md` y `.docx`
- `docs/fuentes/resumen_validaciones.json`
- `scripts/validar_paquete.py`

**Campos orientativos en el CSV salarial:** `fuente_id`, `nivel_desglose`, `campo_estudio`, `anio_observacion`, `cohorte_egreso`, `anos_despues_egreso`, `valor_eur_anual`, `ambito_geografico`, `tipo_indicador`, `poblacion`, `fuente_url`, `fuente_primaria`, `nota`.

**Cuidado con la relación temporal:** una nota de corte del acceso de 2024 no es el salario de esos admitidos en 2024. El dato de cotización de 2024 pertenece a titulados **de una promoción anterior**. La investigación es exploratoria/transversal, no un seguimiento de los mismos estudiantes ni una prueba de causalidad.

**Fuentes de referencia:**

- Ministerio, afiliación de egresados SIIU: https://www.ciencia.gob.es/Ministerio/Estadisticas/SIIU/Afiliacion.html
- U-Ranking, inserción por campos: https://www.u-ranking.es/insercion-SUE
- U-Ranking por universidad/campo, para posible ampliación futura: https://www.u-ranking.es/insercion-uni-campos
- QEDU: https://www.ciencia.gob.es/qedu

### 5.2. INE como contexto salarial (no variable por carrera)

La investigación de SCRUM-26 y el trabajo de Lianghao en SCRUM-34 han documentado datos de salario bruto medio anual de la Comunitat Valenciana para **2018–2024**, usando la tabla INE 28191. Hay un ZIP y un Excel de verificación adjuntos en Jira SCRUM-34.

- Tabla de referencia: https://www.ine.es/jaxiT3/Tabla.htm?t=28191
- `data/raw/ine_salarios_cno11_2018_2024.csv` (repositorio inicial) contiene grupos ocupacionales **sin campo de territorio**, por lo que **no debe etiquetarse como salarios de la Comunitat Valenciana** si no se demuestra dicho alcance.
- No asignar una media general del INE a todos los grados. No mezclar bases de cotización de U-Ranking con ganancias medias del INE en la misma columna como si fueran una sola medida.

### 5.3. Portales de empleo e informes profesionales

- SCRUM-27 (Iván): comparación de InfoJobs/LinkedIn/Indeed, con una estimación consultada en octubre de 2026 para una ocupación junior. Es **una instantánea**, no un histórico por grado. `docs/fuentes/Ficha_portales_empleo_SCRUM-27.md`.
- SCRUM-28 (Lianghao): revisión de informes de colegios profesionales, útiles como contexto pero no suficientes para imputar salarios anuales junior por título. Dossier adjunto en Jira.
- SCRUM-31: queda como vía **opcional para MVP2**, no se necesita para el MVP1.

## 6. Cómo se relacionan los grados con U-Ranking

Archivo de propuesta (NO una correspondencia final aprobada):

`data/processed/propuesta_mapeo_grado_a_campo_sin_salarios.csv`

Contiene 109 registros. En la propuesta inicial aparecen **24 coincidencias literales, 47 sinónimos, 13 casos de revisión manual, 21 dobles grados y 4 sin candidato**. Son categorías de revisión del mapeo, no 109 salarios obtenidos.

Ejemplos:

- `Administración y Dirección de Empresas (ADE)` → candidato `Administración y empresa`.
- `Ingeniería Informática` → candidato `Informática`.
- Algunos dobles grados y `Ciencia de Datos` requieren decisión manual: no asignar automáticamente el sueldo de uno de sus componentes.

El indicador de U-Ranking es por **campo de estudio** y ámbito **España**, no necesariamente por titulación exacta en la UPV/UV. Si varios grados se asignan al mismo campo, **no tratar sus bases de cotización repetidas como observaciones salariales independientes** sin una estrategia de agregación. Dani valida la correspondencia en SCRUM-37/38; Marc apoya con nombres en SCRUM-36.

## 7. Estado y planificación de Jira (instantánea del 7/11/2026)

**Nota:** el estado puede cambiar con el trabajo del equipo; comprobar Jira antes de responder o modificar una tarea.

| Tarea | Responsable | Estado comprobado | Qué significa / próximo paso |
|---|---|---|---|
| SCRUM-26 · Revisar INE | Jose Miguel | Done | Ficha de fuente y limitaciones. |
| SCRUM-27 · Portales de empleo | Iván | Done | Investigación de portales, fuente complementaria. |
| SCRUM-28 · Colegios | Lianghao | Done | Informe profesional adjunto. |
| SCRUM-29 · Documentar fuentes | Jose Miguel | Done | Ficha consolidada con procedencia y limitaciones. |
| SCRUM-30 · Verificar fuentes salariales | Dani | En curso | Completar cobertura y definiciones de INE/SIIU/U-Ranking; fecha 8 nov. |
| SCRUM-32 · Organizar bases de cotización | Jose Miguel | Por hacer | Paquete de 20 archivos ya subido en PR #2; falta revisión/integración; fecha 8 nov. |
| SCRUM-34 · Control de calidad salarial | Lianghao | En curso | Trabajó INE real; revisar indicadores de cotización; fecha 9 nov. |
| SCRUM-35 · Cruce notas–U-Ranking | Dani | En curso | Depende de equivalencias y de un criterio coherente de notas; fecha 9 nov. |
| SCRUM-36 · Denominaciones de grados | Marc | Por hacer | Aclarar títulos y campus; fecha 8 nov. |
| SCRUM-37/38 · Mapeo y validación | Dani | En curso | Decidir equivalencias; fecha 8 nov. |
| SCRUM-39 · Estadísticos de notas | Iván | En revisión | Versión inicial hecha; actualizar solo si cambian/precisan datos o agregación; fecha 9 nov. |
| SCRUM-40 · Gráficos de notas | Lianghao | En revisión | Hay figuras V1: revisar si presentan medias conjuntas o notas individuales, y actualizar lo afectado; fecha 9 nov. |
| SCRUM-41 · Comparativa UPV/UV | Iván | En revisión | Comprobar comparabilidad campus/año y no usar media conjunta como nota local; fecha 9 nov. |
| SCRUM-42 · Indicador 2024 por grado | Jose Miguel | Por hacer | Preparar tabla únicamente con mapeo validado; fecha 9 nov. |
| SCRUM-43 · Correlación | Dani | En curso | Solo con pares comparables; fecha 9 nov. |
| SCRUM-44 · Gráfico nota–cotización | Lianghao | Por hacer | Dependiente de SCRUM-43; fecha 9 nov. |
| SCRUM-45/46 · Atípicos | Marc / Iván | Por hacer | Si existen pares válidos; de lo contrario, explicar exclusiones; fecha 9 nov. |
| SCRUM-60 · Prototipo | Marc | Por hacer | MVP1; fecha 9 nov. |
| SCRUM-61 · Diapositivas | Marc | Por hacer | Presentación del 10 nov; fecha 9 nov. |
| SCRUM-62 · Ensayo | Marc | Por hacer | Ensayo del 9 nov. |
| **SCRUM-71 · Verificación oficial adicional** | — | **Eliminada** | **Decisión del grupo:** no continuar tarea separada al detectar confusión entre notas individuales y medias conjuntas. No recrearla automáticamente. |

**Tareas históricas en Done:** SCRUM-11/12 (extracción inicial notas), SCRUM-14 (primera revisión de salarios), SCRUM-15 (nombres), SCRUM-16/33 (limpieza V1). Conservan mérito e historial; no deben utilizarse para afirmar que el cruce actual ya está terminado.

**Hitos generales SCRUM-17/18/19/20:** se pasaron a «En revisión» porque sus subtareas o resultados actuales seguían pendientes. En sus descripciones —y en algunas de SCRUM-35/39/40/41— **puede quedar una referencia antigua a SCRUM-71**, ahora eliminada. Considerarla una dependencia obsoleta, no evidencia de que siga existiendo. El grupo debe acordar si la revisión se integra en tareas existentes.

## 8. Qué entregamos el 10 de noviembre y cuál es el alcance futuro

### MVP1 — 10/11/2026

**Mínimo defendible:**

1. Explicar pregunta del proyecto, procedencia, definición de notas y diferencias entre valores por campus y medias conjuntas.
2. Estadísticos/gráficos de notas UPV/UV utilizando una medida de nota bien definida y reproducible; distinguir claramente V1 y cambios posteriores.
3. Datos descriptivos de cotización: 10 ámbitos generales en 2021–2024 y campos detallados de U-Ranking solo en 2024 (indicador nacional).
4. Si las equivalencias son defendibles y hay suficientes pares independientes, presentar **comparación exploratoria** nota–cotización de 2024, con número de campos, exclusiones y Pearson/Spearman si procede.
5. Explicar explícitamente sesgos, distintas promociones, ámbito España frente a títulos UPV/UV, ausencia de salarios junior por grado y límites del mapeo.

**Si no hay pares comparables suficientes:** presentar análisis descriptivo y método del cruce propuesto, con limitaciones y plan de mejora. No inventar correlaciones ni presentar 2021–2023 como histórico de 111 carreras.

### Alcance completo del proyecto (MVP2 y producto final)

Se mantiene el objetivo de estudiar la asociación entre dificultad de acceso e ingresos. Después del primer MVP se puede ampliar cobertura de notas y su procedencia, revisar indicadores por **universidad y campo** si están disponibles, mejorar mapeos, aplicar modelos estadísticos y preparar dashboard y memoria. **La pregunta científica no ha cambiado; ha cambiado la precisión del indicador disponible para el primer MVP.**

## 9. Trabajo inmediato sugerido por persona

- **Iván:** confirmar con el grupo qué nota se ha usado en cada gráfico (anual por campus, media temporal individual o media conjunta); recalcular SCRUM-39/41 solo si el criterio anterior era incorrecto; evitar replantear la SCRUM-71 eliminada. Documentar muestras y resultados.
- **Dani:** decidir con Marc las equivalencias válidas del archivo de mapeo, informar cobertura y ejecutar SCRUM-35/43 únicamente sobre registros comparables. Distinguir 10 ámbitos históricos y 111 campos de 2024.
- **Lianghao:** comprobar unidades y coherencia de los CSV salariales; revisar SCRUM-40/44 y reutilizar código/gráficas V1 si siguen representando correctamente las variables escogidas.
- **Marc:** finalizar títulos, slides y prototipo; llevar a presentación solo gráficos correctos; coordinar ensayo y posibles exclusiones.
- **Jose Miguel:** documentar/integrar con revisión la PR #2, facilitar cotizaciones y, tras la validación del mapeo, preparar SCRUM-42. No declarar Done antes de comprobar cobertura.

**Evitar nuevos cambios masivos en Jira o reemplazar archivos originales a dos días del MVP sin acuerdo del grupo.**

## 10. Reglas para otra IA que reciba este archivo

1. **Leer primero la estructura del repositorio y las tareas de Jira vigentes** si tiene acceso; esta memoria es un punto de partida, no un sustituto de la evidencia actual.
2. **Respetar la decisión del grupo:** SCRUM-71 se eliminó; no recomendar automáticamente reabrirla por las diferencias de la auditoría. Si procede, señalar validaciones específicas en los entregables existentes.
3. **No decir «las notas originales estaban mal» como hecho general.** Parte del problema provino de medias conjuntas frente a notas por campus y de diferencias de adjudicación. Identificar las columnas antes de comparar.
4. **No confundir salario INE, estimación de Indeed y base media de cotización U-Ranking.** Tampoco inventar valores históricos por campo para 2021–2023.
5. **No realizar un cruce por nombre a ciegas.** Normalizar nombres (incluyendo ADE), validar ambigüedades, dobles grados, campus, años y observaciones compartidas.
6. **No afirmar causalidad:** asociación no significa que una nota alta provoque sueldos altos ni que los alumnos admitidos en 2024 ya percibieran la cotización observada ese mismo año.
7. **No tocar Jira ni hacer commits/merges sin petición expresa.** Avisar antes si hay riesgo de perder trabajo ajeno.
8. **Mantener la trazabilidad:** fuente, fecha, versión, código, método y archivo final. Los originales no se borran.
9. **Priorizar el MVP del 10/11:** menos datos bien definidos es preferible a una correlación de 109 registros con unidades o claves incoherentes.
10. Ante dudas, diferenciar siempre entre **hecho comprobado**, **decisión del equipo**, **propuesta** y **pendiente de validar**.

---

**Enlaces principales para empezar:** [Repositorio](https://github.com/ivanloki00/GPR) · [PR #2: datos](https://github.com/ivanloki00/GPR/pull/2) · [Jira SCRUM](https://4tocddgpr.atlassian.net/jira/software/projects/SCRUM) · [U-Ranking](https://www.u-ranking.es/insercion-SUE) · [INE 28191](https://www.ine.es/jaxiT3/Tabla.htm?t=28191).
