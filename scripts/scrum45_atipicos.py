"""SCRUM-45 · Detección de valores atípicos en el subconjunto validado.

Ejecutar desde la raíz del repositorio:

    python scripts/scrum45_atipicos.py

Entradas (no se modifican):
    data/processed/SCRUM42_borrador_por_grado_NO_VALIDADO.csv   (cruce grado→campo U-Ranking)
    data/raw/grados_upv_notas_corte_2022_2026.csv               (series de notas por campus)
    data/raw/grados_uv_notas_corte_2022_2026.csv
    data/raw/mapeo_carreras_cno11_final.csv                     (opcional: mapeo alternativo en main)

Salidas:
    data/processed/SCRUM45_registro_atipicos.csv    una fila por grado×campus (109), con todas las marcas
    data/processed/SCRUM45_campos_subconjunto.csv   una fila por campo U-Ranking del subconjunto
    data/processed/SCRUM45_sensibilidad.csv         asociación nota–cotización con y sin atípicos
    docs/figuras/SCRUM45_dispersion_campos.png
    docs/figuras/SCRUM45_series_notas.png

Principio: NINGUNA observación se elimina. Cada marca indica variable, grupo,
umbral y la decisión tomada, para que el resto del equipo pueda revisarla.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
RAW = ROOT / "data" / "raw"
FIGURES = ROOT / "docs" / "figuras"

YEARS = ["2022", "2023", "2024", "2025", "2026"]

# --- Criterios (documentados en docs/entregables/SCRUM45_atipicos.md) -------
# Subconjunto: equivalencias por nombre literal o sinónimo propuesto. Cuando Dani
# cierre SCRUM-37/38, basta con cambiar esta lista o leer la columna de validación.
ESTADOS_SUBCONJUNTO = {"COINCIDENCIA_NOMBRE", "SINONIMO_PROPUESTO"}
NOTA_MIN, NOTA_MAX = 5.0, 14.0   # escala de acceso a grado en la Comunitat Valenciana
UMBRAL_SALTO = 0.5               # puntos entre años consecutivos (> 3 desv. típ. de los cambios)
TUKEY_K = 1.5                    # regla de Tukey sobre el rango intercuartílico
UMBRAL_RESIDUO = 2.0             # residuo estandarizado del ajuste nota→cotización por campo


def tukey_limits(values: pd.Series, k: float = TUKEY_K) -> tuple[float, float]:
    q1, q3 = values.quantile([0.25, 0.75])
    iqr = q3 - q1
    return q1 - k * iqr, q3 + k * iqr


def add_flag(df: pd.DataFrame, mask: pd.Series, code: str, text: str) -> None:
    mask = mask.fillna(False)
    df.loc[mask, "marcas"] = df.loc[mask, "marcas"] + code + ";"
    df.loc[mask, "detalle"] = df.loc[mask, "detalle"] + text + " | "


def load_series() -> pd.DataFrame:
    frames = []
    for uni, name in (("UPV", "grados_upv_notas_corte_2022_2026.csv"),
                      ("UV", "grados_uv_notas_corte_2022_2026.csv")):
        f = pd.read_csv(RAW / name, encoding="utf-8-sig", dtype=str)
        f["universidad"] = uni
        frames.append(f)
    s = pd.concat(frames, ignore_index=True)
    s[YEARS] = s[YEARS].apply(pd.to_numeric, errors="coerce")
    return s.rename(columns={"Grado": "grado_original", "Campus": "campus"})[
        ["universidad", "grado_original", "campus", *YEARS]]


def fit(x: np.ndarray, y: np.ndarray) -> dict:
    """OLS simple con residuos estandarizados internamente y distancia de Cook."""
    n = len(x)
    X = np.column_stack([np.ones(n), x])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    h = np.diag(X @ np.linalg.inv(X.T @ X) @ X.T)
    s2 = resid @ resid / (n - 2)
    std_resid = resid / np.sqrt(s2 * (1 - h))
    cooks = std_resid**2 / 2 * h / (1 - h)
    return {"beta": beta, "std_resid": std_resid, "cooks": cooks}


def rank(a: np.ndarray) -> np.ndarray:
    return pd.Series(a).rank().to_numpy()


def assoc(x: np.ndarray, y: np.ndarray, label: str) -> dict:
    return {"escenario": label, "n_campos": len(x),
            "pearson_r": round(float(np.corrcoef(x, y)[0, 1]), 3),
            "spearman_rho": round(float(np.corrcoef(rank(x), rank(y))[0, 1]), 3)}


def main() -> None:
    base = pd.read_csv(PROCESSED / "SCRUM42_borrador_por_grado_NO_VALIDADO.csv",
                       sep=";", encoding="utf-8-sig")
    series = load_series()
    df = base.merge(series, on=["universidad", "grado_original", "campus"],
                    how="left", validate="one_to_one", indicator=True)
    df["marcas"] = ""
    df["detalle"] = ""
    nota = df["nota_corte_2024_original_campus"]

    # ---------------- U · Uniones / mapeo ----------------
    add_flag(df, df["_merge"] != "both", "U0",
             "La fila del cruce no encuentra su serie en el CSV original de notas")
    df["incluido_subconjunto"] = (df["estado_mapeo_propuesta"].isin(ESTADOS_SUBCONJUNTO)
                                  & nota.notna() & df["cotizacion_2024_eur_candidata"].notna())
    df["motivo_exclusion"] = np.select(
        [~df["estado_mapeo_propuesta"].isin(ESTADOS_SUBCONJUNTO),
         nota.isna(), df["cotizacion_2024_eur_candidata"].isna()],
        ["Mapeo " + df["estado_mapeo_propuesta"].astype(str) + " (no validado)",
         "Sin nota 2024 en el original", "Sin cotización asignada"], default="")

    add_flag(df, df["estado_mapeo_propuesta"].eq("REVISION_MANUAL"), "U1",
             "Equivalencia dudosa: campo U-Ranking más amplio o distinto del grado")
    shared = df.groupby("campo_uranking_candidato")["grado_original"].transform("nunique")
    add_flag(df, shared > 1, "U2",
             "Varios grados distintos comparten campo y, por tanto, la misma cotización")

    mapping_path = RAW / "mapeo_carreras_cno11_final.csv"
    if mapping_path.exists():
        alt = (pd.read_csv(mapping_path, encoding="utf-8-sig")
               .drop_duplicates("Grado")
               .rename(columns={"Grado": "grado_original", "campo_estudio": "campo_mapeo_main"}))
        df = df.merge(alt[["grado_original", "campo_mapeo_main"]], on="grado_original", how="left")
        differs = (df["campo_mapeo_main"].notna() & df["campo_uranking_candidato"].notna()
                   & (df["campo_mapeo_main"].str.lower() != df["campo_uranking_candidato"].str.lower()))
        add_flag(df, differs, "U3",
                 "El mapeo de main asigna otro campo: "
                 + df["campo_mapeo_main"].fillna("") + " ≠ " + df["campo_uranking_candidato"].fillna(""))

    # ---------------- N · Notas de corte ----------------
    vals = df[YEARS]
    add_flag(df, ((vals < NOTA_MIN) | (vals > NOTA_MAX) | (vals == 0)).any(axis=1), "N1",
             f"Alguna nota fuera de [{NOTA_MIN}, {NOTA_MAX}] o igual a cero")
    add_flag(df, vals.nunique(axis=1).eq(1) & vals.notna().all(axis=1), "N2",
             "Misma nota los 5 años: probablemente nota mínima de acceso (5,00), no de corte")
    jumps = vals.diff(axis=1).iloc[:, 1:].abs()
    df["salto_max"] = jumps.max(axis=1).round(2)
    add_flag(df, df["salto_max"] > UMBRAL_SALTO, "N3",
             f"Cambio interanual > {UMBRAL_SALTO} puntos (máx. " + df["salto_max"].astype(str) + ")")
    add_flag(df, vals.isna().any(axis=1), "N4",
             "Serie incompleta: faltan años (posible grado de nueva implantación)")
    lo, hi = tukey_limits(nota[df["incluido_subconjunto"]])
    add_flag(df, df["incluido_subconjunto"] & ((nota < lo) | (nota > hi)), "N5",
             f"Nota 2024 fuera de Tukey 1,5·IQR del subconjunto [{lo:.2f}, {hi:.2f}]")

    # ---------------- S · Cotización (unidad: campo, evita duplicar la misma cifra) ----------------
    sub = df[df["incluido_subconjunto"]]
    campos = (sub.groupby("campo_uranking_candidato")
              .agg(nota_media_2024=("nota_corte_2024_original_campus", "mean"),
                   n_filas=("grado_original", "size"),
                   grados=("grado_original", lambda s: " / ".join(sorted(set(s)))),
                   cotizacion_2024=("cotizacion_2024_eur_candidata", "first"))
              .reset_index())
    clo, chi = tukey_limits(campos["cotizacion_2024"])
    campos["cotizacion_atipica"] = (campos["cotizacion_2024"] < clo) | (campos["cotizacion_2024"] > chi)
    m = fit(campos["nota_media_2024"].to_numpy(), campos["cotizacion_2024"].to_numpy())
    campos["residuo_estandarizado"] = m["std_resid"].round(2)
    campos["distancia_cook"] = m["cooks"].round(3)
    umbral_cook = 4 / len(campos)
    campos["residuo_atipico"] = campos["residuo_estandarizado"].abs() > UMBRAL_RESIDUO
    campos["influyente"] = campos["distancia_cook"] > umbral_cook
    campos["decision"] = np.where(
        campos[["cotizacion_atipica", "residuo_atipico", "influyente"]].any(axis=1),
        "MANTENER y señalar: indicador nacional plausible; ver análisis de sensibilidad", "MANTENER")

    look = campos.set_index("campo_uranking_candidato")
    c = df["campo_uranking_candidato"]
    in_sub = df["incluido_subconjunto"]
    add_flag(df, in_sub & c.map(look["cotizacion_atipica"]).astype("boolean"), "S1",
             f"Cotización fuera de Tukey 1,5·IQR entre campos [{clo:,.0f}, {chi:,.0f}] €")
    add_flag(df, in_sub & c.map(look["residuo_atipico"]).astype("boolean"), "S2",
             f"Residuo estandarizado del campo > {UMBRAL_RESIDUO}: cotización lejos de lo esperado por su nota")
    add_flag(df, in_sub & c.map(look["influyente"]).astype("boolean"), "S3",
             f"Campo influyente (Cook > 4/n = {umbral_cook:.3f})")

    # ---------------- Clasificación y decisión ----------------
    def tipo(m: str) -> str:
        kinds = [k for k, p in (("Nota", "N"), ("Unión/mapeo", "U"), ("Salarial plausible", "S"))
                 if any(t.startswith(p) for t in m.split(";") if t)]
        return " + ".join(kinds) if kinds else "Sin marca"
    df["tipo_anomalia"] = df["marcas"].map(tipo)
    df["decision"] = np.where(df["marcas"].eq(""), "MANTENER",
                              "MANTENER y revisar (no se suprime ninguna observación)")
    df["procedencia_nota"] = "data/raw/grados_" + df["universidad"].str.lower() + "_notas_corte_2022_2026.csv"
    df["procedencia_cruce"] = "data/processed/SCRUM42_borrador_por_grado_NO_VALIDADO.csv"
    df["detalle"] = df["detalle"].str.rstrip(" |")
    df["marcas"] = df["marcas"].str.rstrip(";")

    cols = ["universidad", "grado_original", "campus", *YEARS, "salto_max",
            "nota_corte_2024_original_campus", "campo_uranking_candidato", "estado_mapeo_propuesta",
            "cotizacion_2024_eur_candidata", "incluido_subconjunto", "motivo_exclusion",
            "marcas", "tipo_anomalia", "detalle", "decision", "procedencia_nota", "procedencia_cruce"]
    if "campo_mapeo_main" in df:
        cols.insert(cols.index("estado_mapeo_propuesta"), "campo_mapeo_main")
    df[cols].to_csv(PROCESSED / "SCRUM45_registro_atipicos.csv", sep=";", index=False, encoding="utf-8-sig")
    campos.to_csv(PROCESSED / "SCRUM45_campos_subconjunto.csv", sep=";", index=False, encoding="utf-8-sig")

    # ---------------- Sensibilidad ----------------
    x, y = campos["nota_media_2024"].to_numpy(), campos["cotizacion_2024"].to_numpy()
    flagged = campos[["cotizacion_atipica", "residuo_atipico", "influyente"]].any(axis=1).to_numpy()
    sens = pd.DataFrame([assoc(x, y, "Todos los campos del subconjunto"),
                         assoc(x[~flagged], y[~flagged], "Sin campos marcados (S1/S2/S3)")])
    sens["advertencia"] = "Exploratorio; mapeo pendiente de validar; no implica causalidad"
    sens.to_csv(PROCESSED / "SCRUM45_sensibilidad.csv", sep=";", index=False, encoding="utf-8-sig")

    # ---------------- Figuras ----------------
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 6.5))
    ax.scatter(x[~flagged], y[~flagged], s=30 + 25 * campos["n_filas"][~flagged], alpha=.6,
               color="#4C72B0", label="Campo sin marca")
    ax.scatter(x[flagged], y[flagged], s=30 + 25 * campos["n_filas"][flagged], alpha=.9,
               color="#DD5544", edgecolor="black", label="Campo marcado (S1/S2/S3)")
    xs = np.linspace(x.min(), x.max(), 50)
    ax.plot(xs, m["beta"][0] + m["beta"][1] * xs, "--", color="gray", lw=1, label="Ajuste lineal (todos)")
    for _, r in campos[flagged].iterrows():
        ax.annotate(r["campo_uranking_candidato"], (r["nota_media_2024"], r["cotizacion_2024"]),
                    xytext=(6, 4), textcoords="offset points", fontsize=8)
    ax.set_xlabel("Nota de corte 2024 (media de los grados×campus del campo)")
    ax.set_ylabel("Base media de cotización 2024, España (€/año)")
    ax.set_title(f"SCRUM-45 · Atípicos por campo U-Ranking (n = {len(campos)} campos, {int(in_sub.sum())} grados×campus)")
    ax.legend(fontsize=8, loc="upper left")
    ax.text(0.99, 0.01, "Tamaño del punto = nº de grados×campus. Fuente: SCRUM-42 (mapeo provisional) y U-Ranking 2026.",
            transform=ax.transAxes, ha="right", fontsize=7, color="gray")
    fig.tight_layout()
    fig.savefig(FIGURES / "SCRUM45_dispersion_campos.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 5.5))
    yrs = [int(v) for v in YEARS]
    for _, r in df.iterrows():
        ax.plot(yrs, r[YEARS].to_numpy(float), color="lightgray", lw=.8, zorder=1)
    for _, r in df[df["marcas"].str.contains("N2|N3", regex=True)].iterrows():
        ax.plot(yrs, r[YEARS].to_numpy(float), lw=2.2, marker="o", zorder=3,
                label=f"{r['grado_original']} ({r['universidad']} {r['campus']})")
    ax.set_xticks(yrs)
    ax.set_ylabel("Nota de corte")
    ax.set_title("SCRUM-45 · Series de notas 2022–2026: saltos > 0,5 (N3) y notas constantes (N2)")
    ax.legend(fontsize=8, loc="upper right", framealpha=.95)
    fig.tight_layout()
    fig.savefig(FIGURES / "SCRUM45_series_notas.png", dpi=150)
    plt.close(fig)

    print(f"Filas: {len(df)} | subconjunto: {int(in_sub.sum())} | campos: {len(campos)}")
    print(df["tipo_anomalia"].value_counts().to_string())
    print(sens.to_string(index=False))


if __name__ == "__main__":
    main()
