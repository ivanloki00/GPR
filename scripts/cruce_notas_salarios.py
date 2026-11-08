"""Construye un cruce exploratorio entre notas de corte y salarios U-Ranking 2024.

La unidad de observación del cruce es un grado, universidad, campus y año de
nota. El salario se incorpora como indicador del campo de estudio equivalente.
Solo se aceptan equivalencias exactas del mapeo final y registros salariales
detallados de 2024; no se mezclan las series de ámbitos amplios de 2022/2023.
"""

from pathlib import Path

import pandas as pd


YEARS = ["2022", "2023", "2024", "2025", "2026"]
OUTPUT_COLUMNS = [
    "Universidad",
    "Grado",
    "Campus",
    "Anio_nota",
    "Nota_corte",
    "campo_estudio",
    "valor_eur_anual",
    "cohorte_egreso",
    "anos_despues_egreso",
    "ambito_geografico",
    "tipo_indicador",
    "poblacion",
    "fuente_salarial",
    "equivalencia_validada",
]


def find_file(raw_dir: Path, pattern: str) -> Path:
    """Devuelve el único archivo que coincide con un patrón de entrada."""
    matches = sorted(raw_dir.glob(pattern))
    if len(matches) != 1:
        raise FileNotFoundError(
            f"Se esperaba un único archivo para {pattern!r}; encontrados: {matches}"
        )
    return matches[0]


def load_notes(raw_dir: Path) -> pd.DataFrame:
    """Carga las notas UPV y UV y las convierte de formato ancho a largo."""
    frames = []
    for university, filename in (
        ("UPV", "grados_upv_notas_corte_2022_2026.csv"),
        ("UV", "grados_uv_notas_corte_2022_2026.csv"),
    ):
        frame = pd.read_csv(raw_dir / filename, encoding="utf-8-sig")
        frame["Universidad"] = university
        frame[YEARS] = frame[YEARS].apply(pd.to_numeric, errors="coerce")
        frames.append(frame)

    notes = pd.concat(frames, ignore_index=True)
    notes = notes.melt(
        id_vars=["Universidad", "Grado", "Campus"],
        value_vars=YEARS,
        var_name="Anio_nota",
        value_name="Nota_corte",
    )
    notes["Anio_nota"] = notes["Anio_nota"].astype(int)
    return notes


def load_validated_salary_mapping(raw_dir: Path) -> pd.DataFrame:
    """Carga solo salarios detallados de 2024 y equivalencias sin duplicados."""
    mapping = pd.read_csv(raw_dir / "mapeo_carreras_cno11_final.csv")
    mapping = mapping[["Grado", "campo_estudio"]].drop_duplicates()

    salary_path = find_file(raw_dir, "bases_cotizacion_2024_*.csv")
    salary = pd.read_csv(salary_path, sep=";", encoding="utf-8-sig")
    detailed = salary[salary["nivel_desglose"].eq("campo_detallado")].copy()

    if detailed["campo_estudio"].duplicated().any():
        raise ValueError("El salario detallado de 2024 tiene campos duplicados")

    valid_mapping = mapping[mapping["campo_estudio"].isin(detailed["campo_estudio"])]
    if valid_mapping["Grado"].duplicated().any():
        raise ValueError("El mapeo contiene más de un campo salarial por grado")

    salary_columns = [
        "campo_estudio",
        "valor_eur_anual",
        "cohorte_egreso",
        "anos_despues_egreso",
        "ambito_geografico",
        "tipo_indicador",
        "poblacion",
        "fuente_url",
    ]
    return valid_mapping.merge(
        detailed[salary_columns],
        on="campo_estudio",
        how="inner",
        validate="many_to_one",
    ).rename(columns={"fuente_url": "fuente_salarial"})


def build_cross(raw_dir: Path) -> pd.DataFrame:
    """Genera el cruce y comprueba que las claves sean coherentes."""
    notes = load_notes(raw_dir)
    salary_mapping = load_validated_salary_mapping(raw_dir)
    cross = notes.merge(
        salary_mapping,
        on="Grado",
        how="inner",
        validate="many_to_one",
    )
    cross["equivalencia_validada"] = True
    return cross[OUTPUT_COLUMNS].sort_values(
        ["Anio_nota", "Universidad", "Grado", "Campus"]
    ).reset_index(drop=True)


def main() -> None:
    base_dir = Path(__file__).resolve().parents[1]
    raw_dir = base_dir / "data" / "raw"
    processed_dir = base_dir / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)

    cross = build_cross(raw_dir)
    all_years_path = processed_dir / "cruce_notas_salarios_uranking_2024.csv"
    aligned_path = processed_dir / "cruce_notas_2024_salarios_uranking_2024.csv"
    # Formato compatible con Excel en configuración regional española.
    cross.to_csv(
        all_years_path,
        index=False,
        encoding="utf-8-sig",
        sep=";",
        decimal=",",
    )
    cross[cross["Anio_nota"].eq(2024)].to_csv(
        aligned_path,
        index=False,
        encoding="utf-8-sig",
        sep=";",
        decimal=",",
    )

    print(f"Cruce completo: {len(cross)} filas -> {all_years_path}")
    print(
        f"Cruce temporalmente alineado (notas 2024): "
        f"{cross['Anio_nota'].eq(2024).sum()} filas -> {aligned_path}"
    )
    print(f"Grados con equivalencia validada: {cross['Grado'].nunique()}")
    print(f"Campos salariales utilizados: {cross['campo_estudio'].nunique()}")


if __name__ == "__main__":
    main()