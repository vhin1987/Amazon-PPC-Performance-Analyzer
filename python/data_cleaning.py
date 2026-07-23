import pandas as pd


def find_matching_column(raw_columns, candidates, fallback_name):
    """
    Finds the first column that partially matches one of the candidate names.
    """

    for candidate in candidates:
        for col in raw_columns:
            if candidate.lower() in col.lower():
                return col

    return fallback_name


def clean_data(path):
    """
    Reads and standardizes an Amazon Sponsored Products Search Term Report.

    Returns:
        df_raw
        df_clean_keywords
        df_asin_placements
    """

    # --------------------------------------------------
    # Read Excel
    # --------------------------------------------------

    df_raw = pd.read_excel(path)

    df = df_raw.copy()

    raw_columns = [str(c).strip() for c in df.columns]

    # --------------------------------------------------
    # Dynamic column detection
    # --------------------------------------------------

    portfolio_col = find_matching_column(
        raw_columns,
        ["portfolio name", "portfolio"],
        "Portfolio Name"
    )

    campaign_col = find_matching_column(
        raw_columns,
        ["campaign name", "campaign"],
        "Campaign Name"
    )

    search_col = find_matching_column(
        raw_columns,
        ["customer search term", "search term"],
        "Customer Search Term"
    )

    impressions_col = find_matching_column(
        raw_columns,
        ["impressions"],
        "Impressions"
    )

    clicks_col = find_matching_column(
        raw_columns,
        ["clicks"],
        "Clicks"
    )

    spend_col = find_matching_column(
        raw_columns,
        ["spend"],
        "Spend"
    )

    orders_col = find_matching_column(
        raw_columns,
        ["orders", "conversions", "purchases"],
        "7-Day Total Orders (#)"
    )

    sales_col = find_matching_column(
        raw_columns,
        ["sales", "revenue"],
        "7-Day Total Sales ($)"
    )

    # --------------------------------------------------
    # Rename columns
    # --------------------------------------------------

    column_map = {

        portfolio_col: "Portfolio_Name",

        campaign_col: "Campaign_Name",

        search_col: "Search_Term",

        impressions_col: "Impressions",

        clicks_col: "Clicks",

        spend_col: "Spend",

        orders_col: "Orders",

        sales_col: "Sales"

    }

    df = df.rename(columns=column_map)

    # --------------------------------------------------
    # Ensure required columns exist
    # --------------------------------------------------

    required_columns = [

        "Portfolio_Name",
        "Campaign_Name",
        "Search_Term",
        "Impressions",
        "Clicks",
        "Spend",
        "Orders",
        "Sales"

    ]

    for col in required_columns:

        if col not in df.columns:

            if col in ["Portfolio_Name", "Campaign_Name"]:

                df[col] = "Not Specified"

            else:

                df[col] = 0

    # --------------------------------------------------
    # Keep only required columns
    # --------------------------------------------------

    df = df[required_columns]

    # --------------------------------------------------
    # Handle missing values
    # --------------------------------------------------

    df = df.dropna(subset=["Search_Term"])

    df["Search_Term"] = (
        df["Search_Term"]
        .astype(str)
        .str.strip()
    )

    df["Portfolio_Name"] = (
        df["Portfolio_Name"]
        .fillna("Not Specified")
        .astype(str)
        .str.strip()
    )

    df["Campaign_Name"] = (
        df["Campaign_Name"]
        .fillna("Not Specified")
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------
    # Convert numeric columns
    # --------------------------------------------------

    numeric_columns = [

        "Impressions",
        "Clicks",
        "Spend",
        "Orders",
        "Sales"

    ]

    for col in numeric_columns:

        df[col] = (
            pd.to_numeric(df[col], errors="coerce")
            .fillna(0)
        )

    # --------------------------------------------------
    # Aggregate duplicate keywords
    # --------------------------------------------------

    df_grouped = (

        df.groupby(

            [

                "Portfolio_Name",
                "Campaign_Name",
                "Search_Term"

            ],

            as_index=False

        )

        .agg({

            "Impressions": "sum",

            "Clicks": "sum",

            "Spend": "sum",

            "Orders": "sum",

            "Sales": "sum"

        })

    )

    # --------------------------------------------------
    # Separate ASINs from keywords
    # --------------------------------------------------

    is_asin = df_grouped["Search_Term"].str.startswith(

        ("b0", "B0"),

        na=False

    )

    df_asin_placements = df_grouped[is_asin].copy()

    df_clean_keywords = df_grouped[~is_asin].copy()

    return (

        df_raw,

        df_clean_keywords,

        df_asin_placements

    )
