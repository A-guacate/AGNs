import pandas as pd
from typing import Iterable, Optional


def _find_column(df: pd.DataFrame, options: Iterable[str]) -> Optional[str]:
    for name in options:
        if name in df.columns:
            return name
    # case-insensitive search
    lowcols = {c.lower(): c for c in df.columns}
    for name in options:
        if name.lower() in lowcols:
            return lowcols[name.lower()]
    return None


def make_qso_latex_table(
    results: pd.DataFrame,
    top_n: int = 100,
    sort_by: Optional[str] = None,
    filename: Optional[str] = None,
) -> str:
    """Generate a LaTeX table (string) of the top-N QSOs from `results`.

    Behavior:
    - Attempts to build a QSO id from `plate` and `fiberid` if present.
    - Selects columns: id, z, T_e, N_e (tries several name variants).
    - Sorts by `sort_by` if given and present, otherwise by `chi2_red`/`chi2` if available.
    - Returns the LaTeX table as a string and optionally saves to `filename`.

    Parameters:
    - results: pandas DataFrame (e.g. `results_good` from the notebook).
    - top_n: number of rows to include (default 100).
    - sort_by: column name to sort by (ascending). If None, chooses best available.
    - filename: if provided, write the LaTeX to this file.
    """

    df = results.copy()

    # Build an ID column
    if "plate" in df.columns and "fiberid" in df.columns:
        df["qso_id"] = df["plate"].astype(str) + "-" + df["fiberid"].astype(str)
    elif "plate" in df.columns:
        df["qso_id"] = df["plate"].astype(str)
    elif "fiberid" in df.columns:
        df["qso_id"] = df["fiberid"].astype(str)
    else:
        # try case-insensitive
        plate_col = _find_column(df, ["plate"])
        fiber_col = _find_column(df, ["fiberid", "fiber_id"])
        if plate_col and fiber_col:
            df["qso_id"] = df[plate_col].astype(str) + "-" + df[fiber_col].astype(str)
        elif plate_col:
            df["qso_id"] = df[plate_col].astype(str)
        elif fiber_col:
            df["qso_id"] = df[fiber_col].astype(str)
        else:
            # fallback to the dataframe index
            df["qso_id"] = df.index.astype(str)

    # Find columns for z, T_e, N_e
    z_col = _find_column(df, ["z"])
    te_col = _find_column(df, ["T_e", "Te", "T_e[K]", "T_e_k"])
    ne_col = _find_column(df, ["N_e", "Ne"])

    cols = ["qso_id"]
    if z_col:
        cols.append(z_col)
    if te_col:
        cols.append(te_col)
    if ne_col:
        cols.append(ne_col)

    # Determine sort column
    sort_col = None
    if sort_by and sort_by in df.columns:
        sort_col = sort_by
    else:
        for cand in ["chi2_red", "chi2", "chi2_reduced"]:
            if cand in df.columns:
                sort_col = cand
                break

    if sort_col is not None:
        df_sorted = df.sort_values(by=sort_col, ascending=True)
    else:
        df_sorted = df

    df_top = df_sorted.loc[:, cols].head(top_n)

    # Nicely format numeric columns
    fmt = {}
    if z_col:
        fmt[z_col] = "{:.5f}".format
    if te_col:
        fmt[te_col] = "{:.1f}".format
    if ne_col:
        fmt[ne_col] = "{:.0f}".format

    # Rename columns for presentation
    display_names = {"qso_id": "ID", z_col: "z", te_col: "T_e", ne_col: "N_e"}
    df_print = df_top.rename(columns={k: v for k, v in display_names.items() if k})

    latex = df_print.to_latex(index=False, float_format=lambda x: ("{:.3f}".format(x) if isinstance(x, float) else str(x)))

    if filename:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(latex)

    return latex


if __name__ == "__main__":
    import sys
    import json

    msg = (
        "Usage: import this module and call make_qso_latex_table(results_good, top_n=100, filename=...)"
    )
    print(msg)
