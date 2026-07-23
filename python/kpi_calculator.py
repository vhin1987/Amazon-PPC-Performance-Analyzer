import pandas as pd


def calculate_kpis(dataset):
    """
    Calculate Amazon PPC KPIs.

    Parameters
    ----------
    dataset : pandas.DataFrame

    Returns
    -------
    pandas.DataFrame
        Dataset with calculated KPIs.
    """

    dataset = dataset.copy()

    # -----------------------------
    # Click Through Rate
    # -----------------------------
    dataset["CTR"] = (
        dataset["Clicks"] /
        dataset["Impressions"]
    ).fillna(0)

    # -----------------------------
    # Cost Per Click
    # -----------------------------
    dataset["CPC"] = (
        dataset["Spend"] /
        dataset["Clicks"]
    ).fillna(0)

    # -----------------------------
    # Conversion Rate
    # -----------------------------
    dataset["CVR"] = (
        dataset["Orders"] /
        dataset["Clicks"]
    ).fillna(0)

    # -----------------------------
    # Advertising Cost of Sales
    # -----------------------------
    dataset["ACoS"] = (
        dataset["Spend"] /
        dataset["Sales"]
    ).fillna(0)

    # -----------------------------
    # Return on Ad Spend
    # -----------------------------
    dataset["RoAS"] = (
        dataset["Sales"] /
        dataset["Spend"]
    ).fillna(0)

    # -----------------------------
    # Round Values
    # -----------------------------
    dataset[["CTR", "CVR", "ACoS"]] = (
        dataset[["CTR", "CVR", "ACoS"]]
        .round(4)
    )

    dataset[["Spend", "Sales", "CPC", "RoAS"]] = (
        dataset[["Spend", "Sales", "CPC", "RoAS"]]
        .round(2)
    )

    return dataset
