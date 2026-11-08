"""Evalúa Pearson y Spearman entre notas de corte y salarios de 2024.

El resultado principal usa un registro por grado, promediando sus notas cuando
aparece en más de un campus o universidad. También se calcula una sensibilidad
con todos los registros grado-campus. El salario sigue siendo un indicador de
campo de estudio, por lo que puede repetirse entre varios grados.
"""

from pathlib import Path

import pandas as pd
from scipy.stats import pearsonr, spearmanr


INPUT_NAME = "cruce_notas_2024_salarios_uranking_2024.csv"
RESULT_NAME = "correlaciones_notas_salarios_2024.csv"
OBSERVATIONS_NAME = "observaciones_correlacion_notas_salarios_2024.csv"


def load_cross(path: Path) -> pd.DataFrame:
    """Carga el cruce en formato regional español y valida sus variables."""
    frame = pd.read_csv(path, sep=";", decimal=",", encoding="utf-8-sig")
    required = {"Grado", "Campus", "Nota_corte", "campo_estudio", "valor_eur_anual"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Faltan columnas requeridas: {sorted(missing)}")

    frame["Nota_corte"] = pd.to_numeric(frame["Nota_corte"], errors="coerce")
    frame["valor_eur_anual"] = pd.to_numeric(
        frame["valor_eur_anual"], errors="coerce"
    )
    frame = frame.dropna(subset=["Nota_corte", "valor_eur_anual"]).copy()
    if frame.empty:
        raise ValueError("No quedan observaciones con nota y salario válidos")
    return frame


def correlation_row(x: pd.Series, y: pd.Series, unit: str) -> dict:
    """Calcula ambas correlaciones y conserva sus p-valores exploratorios."""
    pearson = pearsonr(x, y)
    spearman = spearmanr(x, y)
    return {
        "unidad_analisis": unit,
        "n_observaciones": len(x),
        "n_salarios_unicos": y.nunique(),
        "pearson_r": pearson.statistic,
        "pearson_p_valor": pearson.pvalue,
        "spearman_rho": spearman.statistic,
        "spearman_p_valor": spearman.pvalue,
    }


def main() -> None:
    base_dir = Path(__file__).resolve().parents[1]
    processed_dir = base_dir / "data" / "processed"
    cross = load_cross(processed_dir / INPUT_NAME)

    degree_level = (
        cross.groupby("Grado", as_index=False)
        .agg(
            Nota_corte=("Nota_corte", "mean"),
            valor_eur_anual=("valor_eur_anual", "first"),
            campo_estudio=("campo_estudio", "first"),
            n_registros_nota=("Nota_corte", "size"),
        )
    )
    if degree_level.groupby("Grado")["valor_eur_anual"].nunique().gt(1).any():
        raise ValueError("Un grado tiene más de un salario tras la agregación")

    results = pd.DataFrame(
        [
            correlation_row(
                degree_level["Nota_corte"],
                degree_level["valor_eur_anual"],
                "grado (nota media entre campus/universidades)",
            ),
            correlation_row(
                cross["Nota_corte"],
                cross["valor_eur_anual"],
                "grado-campus (sensibilidad)",
            ),
        ]
    )
    results["advertencia"] = (
        "Exploratorio: solo 5 salarios únicos; no implica causalidad."
    )

    observations = degree_level.rename(
        columns={"n_registros_nota": "n_notas_agregadas"}
    )
    results.to_csv(
        processed_dir / RESULT_NAME,
        index=False,
        sep=";",
        decimal=",",
        encoding="utf-8-sig",
    )
    observations.to_csv(
        processed_dir / OBSERVATIONS_NAME,
        index=False,
        sep=";",
        decimal=",",
        encoding="utf-8-sig",
    )

    print(results.to_string(index=False))
    print(f"Resultados: {processed_dir / RESULT_NAME}")
    print(f"Observaciones agregadas: {processed_dir / OBSERVATIONS_NAME}")


if __name__ == "__main__":
    main()