const state = { data: null, university: "all", salaryField: "", fieldSort: "desc" };
const money = value => new Intl.NumberFormat("es-ES", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(value);
const avg = values => values.filter(Number.isFinite).reduce((a, b) => a + b, 0) / values.filter(Number.isFinite).length;

function lineChart(container, labels, values, formatValue) {
  const width = 700, height = 220, pad = { l: 38, r: 12, t: 18, b: 30 };
  const valid = values.filter(Number.isFinite), min = Math.min(...valid), max = Math.max(...valid);
  const x = i => pad.l + i * (width - pad.l - pad.r) / (labels.length - 1);
  const y = value => pad.t + (max === min ? .5 : (max - value) / (max - min)) * (height - pad.t - pad.b);
  const points = values.map((value, i) => `${x(i)},${y(value)}`).join(" ");
  const grid = [0, .5, 1].map(r => `<line class="gridline" x1="${pad.l}" x2="${width - pad.r}" y1="${pad.t + r * (height - pad.t - pad.b)}" y2="${pad.t + r * (height - pad.t - pad.b)}"/>`).join("");
  const labelsSvg = labels.map((label, i) => `<text class="chart-label" x="${x(i)}" y="${height - 5}" text-anchor="middle">${label}</text>`).join("");
  const dots = values.map((value, i) => Number.isFinite(value) ? `<circle class="line-dot" cx="${x(i)}" cy="${y(value)}" r="5"/><text class="chart-value" x="${x(i)}" y="${y(value) - 13}" text-anchor="middle">${formatValue(value)}</text>` : "").join("");
  container.innerHTML = `<svg viewBox="0 0 ${width} ${height}" role="img">${grid}<polyline class="line-path" points="${points}"/>${dots}${labelsSvg}</svg>`;
}

function updateNotes() {
  const rows = state.data.notes.filter(row => state.university === "all" || row.university === state.university);
  const values = ["2022", "2023", "2024", "2025", "2026"].map(year => avg(rows.map(row => row.years[year]).filter(Number.isFinite)));
  lineChart(document.querySelector("#notes-chart"), ["2022", "2023", "2024", "2025", "2026"], values, value => value.toFixed(1));
  const byCampus = Object.entries(rows.reduce((acc, row) => {
    acc[row.campus] = acc[row.campus] || [];
    acc[row.campus].push(row.average);
    return acc;
  }, {})).map(([campus, values]) => [campus, avg(values.filter(Number.isFinite))]).filter(([, value]) => Number.isFinite(value)).sort((a, b) => b[1] - a[1]).slice(0, 5);
  const max = byCampus[0]?.[1] || 1;
  document.querySelector("#campus-ranking").innerHTML = byCampus.map(([campus, value], i) => `<div class="ranking-row"><span class="rank">0${i + 1}</span><span class="rank-name">${campus}</span><span class="rank-bar"><i style="width:${value / max * 100}%"></i></span><span class="rank-value">${value.toFixed(2)}</span></div>`).join("");
}

function updateSalary() {
  const rows = state.data.salaries.filter(row => row.level === "ambito_amplio" && row.field === state.salaryField);
  lineChart(document.querySelector("#salary-chart"), rows.map(row => row.year), rows.map(row => row.value), value => `${Math.round(value / 1000)}k`);
}

function updateFields() {
  const allRows = state.data.salaries.filter(row => row.level === "campo_detallado");
  const rows = [...allRows].sort((a, b) => state.fieldSort === "asc" ? a.value - b.value : b.value - a.value).slice(0, 10);
  const max = Math.max(...allRows.map(row => row.value), 1);
  document.querySelector("#fields-chart").innerHTML = rows.map(row => `<div class="field-row"><span class="field-name" title="${row.field}">${row.field}</span><span class="field-track"><i style="width:${row.value / max * 100}%"></i></span><span class="field-value">${money(row.value)}</span></div>`).join("");
}

function updateExploration() {
  const correlation = state.data.correlation;
  document.querySelector("#correlation-results").innerHTML = correlation.map(row => `<div class="correlation-row"><span>${row.unit}</span><strong>${row.spearman.toFixed(2)}</strong><small>rho de Spearman · n=${row.observations}</small></div>`).join("");
  const byYear = Object.entries(state.data.coverage.reduce((acc, row) => {
    acc[row.year] = acc[row.year] || { expected: 0, available: 0 };
    acc[row.year].expected += row.expected;
    acc[row.year].available += row.available;
    return acc;
  }, {}));
  const averageCoverage = avg(byYear.map(([, row]) => row.available / row.expected * 100));
  document.querySelector("#coverage-summary").innerHTML = `<strong>${averageCoverage.toFixed(1)}%</strong><span>cobertura media 2022–2026</span>`;
  document.querySelector("#coverage-bars").innerHTML = byYear.map(([year, row]) => `<div class="coverage-row"><span>${year}</span><i><b style="width:${row.available / row.expected * 100}%"></b></i><small>${(row.available / row.expected * 100).toFixed(0)}%</small></div>`).join("");
  const degrees = state.data.notes.filter(row => row.mapping).sort((a, b) => a.degree.localeCompare(b.degree, "es"));
  const byDegree = Object.groupBy ? Object.groupBy(degrees, row => row.degree) : degrees.reduce((groups, row) => {
    (groups[row.degree] ||= []).push(row);
    return groups;
  }, {});
  const selector = document.querySelector("#degree-filter");
  const resultList = document.querySelector("#degree-results");
  const degreeNames = Object.keys(byDegree).sort((a, b) => a.localeCompare(b, "es"));
  const renderDegree = degree => {
    const matches = byDegree[degree];
    if (!matches?.length) return;
    const row = matches[0];
    const metric = value => value == null ? "—" : value.toFixed(1) + "%";
    const campuses = matches.map(item => `${item.university} · ${item.campus}`).join(" / ");
    const averages = matches.map(item => item.average).filter(Number.isFinite);
    const hasUnverified = matches.some(item => item.averageType === "reference_unverified");
    const offersByUniversity = [...new Set(matches.map(item => item.university))].map(university => {
      const offer = matches.find(item => item.university === university)?.offeredPlaces;
      return `${university}: ${offer ? Math.round(offer).toLocaleString("es-ES") : "—"} plazas estimadas`;
    }).join(" / ");
    const noteLabel = hasUnverified ? "Nota media (incluye referencia)" : "Nota media verificada";
    const noteStatus = hasUnverified ? "Parte de la media procede de cifras no verificadas" : `${matches.length} campus · media de fichas verificadas`;
    document.querySelector("#degree-detail").innerHTML = `<div><span class="detail-label">Rama SIIU</span><strong>${row.branch || "—"}</strong><small>Área general de conocimiento del grado.</small></div><div><span class="detail-label">${noteLabel}</span><strong>${averages.length ? avg(averages).toFixed(2) : "—"}</strong><small>${noteStatus}</small></div><div><span class="detail-label">Campo ajustado</span><strong>${row.mapping || "—"}</strong><small>Campo nacional utilizado para comparar la inserción laboral.</small></div><div><span class="detail-label">Afiliación a la Seguridad Social</span><strong>${metric(row.affiliationRate)}</strong><small>Graduados que siguen dados de alta cuatro años después.</small></div><div><span class="detail-label">Adecuación al nivel universitario</span><strong>${metric(row.adequacyRate)}</strong><small>Mide si el empleo se ajusta al nivel de formación universitaria.</small></div><div><span class="detail-label">Plazas 2024 estimadas</span><strong>${offersByUniversity}</strong></div>`;
  };
  const renderResults = query => {
    const normalized = query.trim().toLocaleLowerCase("es");
    const matches = degreeNames.filter(degree => {
      const campuses = byDegree[degree].map(row => `${row.university} ${row.campus}`).join(" ");
      return `${degree} ${campuses}`.toLocaleLowerCase("es").includes(normalized);
    });
    resultList.innerHTML = matches.slice(0, 18).map(degree => {
      const campuses = [...new Set(byDegree[degree].map(row => `${row.university} · ${row.campus}`))].join(" / ");
      return `<button type="button" class="degree-result" data-degree="${degree}"><strong>${degree}</strong><span>${campuses}</span></button>`;
    }).join("") || `<span class="empty-results">No hay grados que coincidan.</span>`;
    resultList.querySelectorAll(".degree-result").forEach(button => button.addEventListener("click", () => {
      selector.value = button.dataset.degree;
      renderDegree(button.dataset.degree);
    }));
  };
  selector.addEventListener("input", event => {
    renderResults(event.target.value);
    if (byDegree[event.target.value]) renderDegree(event.target.value);
  });
  renderResults("");
  if (degrees.length) { selector.value = degrees[0].degree; renderDegree(degrees[0].degree); }
  document.querySelector("#sources").innerHTML = state.data.sources.map(source => `<a class="source-card" href="${source.url}" target="_blank" rel="noreferrer"><span class="source-icon">↗</span><strong>${source.name}</strong><span>${source.detail}</span></a>`).join("");
}

async function init() {
  state.data = await fetch("/api/data").then(response => response.json());
  const notes = state.data.notes, salaries = state.data.salaries;
  const verified = notes.filter(row => row.status === "CONTRASTADO_SECUNDARIA");
  const references = notes.filter(row => row.averageType === "reference_unverified");
  const fields = salaries.filter(row => row.level === "campo_detallado");
  document.querySelector("#kpi-notes").textContent = notes.length;
  document.querySelector("#kpi-verified").textContent = verified.length;
  document.querySelector("#kpi-reference").textContent = references.length;
  document.querySelector("#kpi-salaries").textContent = salaries.length;
  document.querySelector("#kpi-fields").textContent = fields.length;
  const areas = new Set(salaries.filter(row => row.level === "ambito_amplio").map(row => row.field));
  [...new Set(notes.map(row => row.university))].sort().forEach(value => document.querySelector("#university-filter").insertAdjacentHTML("beforeend", `<option>${value}</option>`));
  [...areas].sort().forEach(value => document.querySelector("#salary-filter").insertAdjacentHTML("beforeend", `<option>${value}</option>`));
  state.salaryField = [...areas].sort()[0];
  document.querySelector("#salary-filter").value = state.salaryField;
  document.querySelector("#university-filter").addEventListener("change", event => { state.university = event.target.value; updateNotes(); });
  document.querySelector("#salary-filter").addEventListener("change", event => { state.salaryField = event.target.value; updateSalary(); });
  document.querySelector("#field-sort").addEventListener("change", event => { state.fieldSort = event.target.value; updateFields(); });
  updateNotes(); updateSalary(); updateFields();
  updateExploration();
}
init().catch(error => { document.querySelector("main").insertAdjacentHTML("afterbegin", `<p style="padding:20px;color:#b33">No se han podido cargar los datos: ${error.message}</p>`); });
