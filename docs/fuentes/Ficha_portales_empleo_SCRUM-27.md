# SCRUM-29 — Portales de empleo y salarios junior en Valencia

**Fecha de consulta:** 25/10/2026  
**Objetivo:** identificar y evaluar fuentes de salarios para perfiles junior en Valencia a
partir de InfoJobs, LinkedIn e Indeed. Esta ficha registra el método, no una muestra
estadística exhaustiva de todas las vacantes.

## Método de consulta

Se realizaron búsquedas públicas, sin iniciar sesión, con estos criterios:

1. Ubicación: `Valencia` o `Valencia, Valencian Community, Spain`. Se aceptó
   también `Valencia provincia` cuando la propia fuente solo ofrece ese nivel
   geográfico.
2. Experiencia: términos `junior`, `entry level` o una ocupación cuyo nombre
   incluyera `junior`.
3. Ocupación: se registró el título exacto mostrado por el portal; no se mezclaron
   ocupaciones diferentes para construir un único salario.
4. Tipo de dato: se distinguió **oferta** (importe asociado a una vacante) de
   **estimación salarial** (agregación o cálculo del portal).
5. Remuneración: se anotó solo si aparecía explícitamente. Se conservaron el
   rango, la unidad temporal y la indicación bruto/neto y fijo/variable. Un campo
   no visible se registró como `ausente/no indicado`, nunca como cero.
6. Trazabilidad: se guardó la URL de resultados o de salario y la fecha de
   consulta. Los portales son dinámicos; una repetición posterior puede devolver
   un conjunto distinto.

## Registro de fuentes consultadas

| Portal y URL | Ubicación | Experiencia | Ocupación observada | Fecha | Tipo | Salario observado | Unidad y componentes |
|---|---|---|---|---|---|---|---|
| [InfoJobs — ofertas junior en Valencia](https://infojobs.net/ofertas-trabajo/valencia-junior) | Torrent/Valencia; el resultado incluye municipios de la provincia | Junior | Técnico/a Junior de Tratamiento y Control de Agua | 25/10/2026 | Oferta | 18.000–20.000 € | Bruto anual; fijo/variable no indicado |
| [InfoJobs — ofertas junior en Valencia](https://infojobs.net/ofertas-trabajo/valencia-junior) | Valencia | Junior | Comercial junior (sector energético) | 25/10/2026 | Oferta | **Ausente en el resumen consultado** | Unidad, bruto/neto y fijo/variable no indicados |
| [LinkedIn — búsqueda de empleos junior en Valencia](https://www.linkedin.com/jobs/search/?keywords=junior&location=Valencia%2C%20Valencian%20Community%2C%20Spain) | Valencia y municipios próximos | Junior | Junior Pega Developer; también aparece Junior Data & BI Analyst | 25/10/2026 | Oferta | **Ausente en el listado consultado** | Unidad, bruto/neto y fijo/variable no indicados |
| [Indeed — salario de Comercial junior en Valencia provincia](https://es.indeed.com/career/comercial-junior/salaries/Valencia-provincia) | Valencia provincia | Junior (incluido en la ocupación) | Comercial junior | 25/10/2026 | Estimación salarial | 20.860 € aproximadamente | Anual; se presenta como bruto; fijo/variable no desglosado |

### Lectura del registro

- El rango de InfoJobs es un salario **publicado en una oferta**, no una media
  de mercado. La oferta localizada es de Torrent, por lo que no debe etiquetarse
  como municipio de Valencia sin conservar ese detalle.
- La cifra de Indeed es una **estimación del portal**, no una oferta concreta.
  La página está agregada por ocupación y provincia y no expone en la consulta
  el tamaño de muestra ni un año de referencia verificable.
- En el resultado de LinkedIn sí se observan vacantes y su ubicación, pero no un
  importe salarial. La ausencia de salario es un resultado válido del registro.
- Ninguna de estas observaciones permite inferir salario neto mensual. Para
  presentar importes mensuales habría que disponer de pagas, retenciones y
  estructura contractual; no se hará una conversión inventada.

## Criterios de selección de una fuente utilizable

Se consideró utilizable una fuente si:

- permite repetir la consulta con una URL estable;
- identifica simultáneamente ocupación y ámbito geográfico;
- diferencia oferta de estimación;
- muestra el salario y su unidad, o permite registrar explícitamente que falta;
- aporta cobertura suficiente para la pregunta sin mezclar títulos no comparables.

### Fuente elegida para el análisis base

**Indeed — páginas de salarios por ocupación y ubicación.**

**Cobertura:** perfiles agrupados por título ocupacional (en esta consulta,
`Comercial junior`) y por `Valencia provincia`; representa estimaciones salariales
de los datos que Indeed ha recabado en la plataforma, no el universo de vacantes
ni exclusivamente titulados universitarios. La consulta no muestra un periodo
histórico o año de cobertura auditable, por lo que la cobertura temporal se
registra como **no especificada** y debe actualizarse con la fecha de extracción.

**Años:** no publicados de forma verificable en la página consultada; la fecha
de consulta es 2026, pero no debe interpretarse como que todas las observaciones
corresponden a 2026.

**Formato:** euros brutos anuales, con un valor estimado para la ocupación y
provincia. No separa en la cifra consultada salario fijo, variable, pagas,
neto mensual ni tipo de contrato.

**Fiabilidad para este proyecto:** adecuada como indicador comparable entre
ocupaciones solo si se mantiene el mismo título, ubicación y fecha de extracción.
Es menos adecuada que una oferta para conocer la remuneración de un puesto
concreto y su paquete retributivo. La fiabilidad se limita por la falta de
transparencia visible sobre muestra, periodo y método de agregación; por ello se
debe citar como `estimación Indeed` y no como salario observado de una persona.

**Decisión de uso:** usar Indeed como fuente salarial principal y conservar
InfoJobs y LinkedIn como fuentes complementarias de transparencia de ofertas.
No combinar la estimación de Indeed con el rango de InfoJobs en una media: son
unidades de observación distintas (estimación agregada frente a oferta concreta).

## Plantilla de extracción para futuras consultas

Para cada observación se recomienda conservar:

`portal, url, fecha_consulta, ubicación, municipio, ocupación, nivel_experiencia,
tipo_dato, salario_min_eur, salario_max_eur, salario_estimado_eur,
periodicidad, bruto_neto, fijo_variable, salario_publicado, notas, fecha_publicacion`

Los valores desconocidos deben ser `NA`/`ausente`, diferenciándolos de un importe
igual a cero. Antes de comparar con notas de corte, debe fijarse una fecha de
referencia y documentarse cualquier cambio de ocupación o de ámbito geográfico.

## Incidencias de acceso y reproducibilidad

En esta consulta, el resultado público de InfoJobs respondió con una restricción
HTTP al intentar abrirlo directamente y la página salarial de Indeed limitó el
acceso automatizado. LinkedIn sí permitió leer el listado público, pero no
mostró salario en las tarjetas observadas. Por tanto, los importes de esta ficha
se deben volver a comprobar manualmente en el portal antes de una publicación
definitiva y no se presentan como un volcado completo de resultados.
