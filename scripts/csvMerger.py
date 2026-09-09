import pandas as pd

# ==========================
# Configuration
# ==========================

MASTER_FILE = "./data/prod_transactions.csv"
NEW_FILE = "./scripts/temp/temp_master_transactions.csv"
OUTPUT_FILE = "./data/prod_transactions.csv"

DATE_COLUMN = "Date"

# Same-day transactions are compared using these columns.
MATCH_COLUMNS = [
    "Description",
    "Amount"
]

# Date format examples:
# "%m/%d/%Y"
# "%Y-%m-%d"
# Leave as None to let pandas detect automatically.
DATE_FORMAT = "%m/%d/%Y"

# Set this to your ID column name.
# Set to None if your files do not have an ID column.
ID_COLUMN = "ID"


# ==========================
# Load CSV
# ==========================

def load_csv(filename):
    df = pd.read_csv(filename)

    # Convert dates
    if DATE_FORMAT:
        df[DATE_COLUMN] = pd.to_datetime(
            df[DATE_COLUMN],
            format=DATE_FORMAT,
            errors="coerce"
        )
    else:
        df[DATE_COLUMN] = pd.to_datetime(
            df[DATE_COLUMN],
            errors="coerce"
        )

    # Convert amounts to numeric
    if "Amount" in df.columns:
        df["Amount"] = pd.to_numeric(
            df["Amount"],
            errors="coerce"
        )

    # Remove rows with invalid dates
    invalid_dates = df[DATE_COLUMN].isna().sum()

    if invalid_dates > 0:
        print(
            f"Warning: {invalid_dates} rows in {filename} "
            f"have invalid dates and will be ignored."
        )

        df = df.dropna(subset=[DATE_COLUMN])

    return df


# ==========================
# Main
# ==========================

def main():

    # ==========================
    # Load files
    # ==========================

    master = load_csv(MASTER_FILE)
    new = load_csv(NEW_FILE)

    # Preserve original master column order
    columns = master.columns.tolist()

    # Make sure the new file contains all
    # columns that exist in the master.
    missing_columns = [
        column
        for column in columns
        if column not in new.columns
    ]

    if missing_columns:
        raise ValueError(
            f"New file is missing columns: {missing_columns}"
        )

    # Only use columns that exist in the master.
    new = new[columns]


    # ==========================
    # Find latest master date
    # ==========================

    if master.empty:
        raise ValueError("Master file is empty.")

    last_date = master[DATE_COLUMN].max()

    print(
        f"Last date in master: "
        f"{last_date.strftime('%m/%d/%Y')}"
    )


    # ==========================
    # Find future transactions
    # ==========================

    # ALL transactions after the latest master date
    # are new transactions and should be added.
    #
    # Duplicates are intentionally allowed here because
    # two identical transactions can both be legitimate.

    future_rows = new[
        new[DATE_COLUMN] > last_date
    ].copy()

    print(
        f"Transactions after last date: "
        f"{len(future_rows)}"
    )


    # ==========================
    # Find same-day transactions
    # ==========================

    master_last_day = master[
        master[DATE_COLUMN] == last_date
    ].copy()

    new_last_day = new[
        new[DATE_COLUMN] == last_date
    ].copy()


    # ==========================
    # Count existing same-day
    # transactions in master
    # ==========================

    # Normalize descriptions for comparison while
    # preserving the original description in the output.

    master_last_day["_description_key"] = (
        master_last_day["Description"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    master_same_day_counts = (
        master_last_day
        .groupby(
            ["_description_key", "Amount"],
            dropna=False
        )
        .size()
        .to_dict()
    )


    # ==========================
    # Compare incoming same-day
    # transactions
    # ==========================

    same_day_rows_to_add = []

    # Track how many copies of each transaction
    # we've encountered in the NEW file.
    new_same_day_counts = {}

    for _, row in new_last_day.iterrows():

        description_key = (
            str(row["Description"])
            .strip()
            .lower()
        )

        key = (
            description_key,
            row["Amount"]
        )

        # Number of identical transactions already
        # represented in the master.
        existing_count = master_same_day_counts.get(
            key,
            0
        )

        # Number of identical transactions we've already
        # encountered in the new file.
        new_count = new_same_day_counts.get(
            key,
            0
        )

        new_same_day_counts[key] = new_count + 1

        # Only skip the number of transactions that are
        # already represented in the master.
        #
        # Example:
        #
        # Master: 2 identical transactions
        # New:    3 identical transactions
        #
        # Result: add 1 transaction.
        #
        # Master: 2
        # New:    2
        #
        # Result: add 0.
        #
        # Master: 0
        # New:    3
        #
        # Result: add all 3.

        if new_count >= existing_count:
            same_day_rows_to_add.append(row)


    same_day_rows_to_add = pd.DataFrame(
        same_day_rows_to_add,
        columns=columns
    )

    print(
        f"New same-day transactions: "
        f"{len(same_day_rows_to_add)}"
    )


    # ==========================
    # Combine rows to add
    # ==========================

    rows_to_add = pd.concat(
        [
            same_day_rows_to_add,
            future_rows
        ],
        ignore_index=True
    )


    print(
        f"Total new rows to add: "
        f"{len(rows_to_add)}"
    )


    # ==========================
    # No updates
    # ==========================

    if rows_to_add.empty:
        print("No updates made")
        return


    # ==========================
    # Combine with master
    # ==========================

    updated_master = pd.concat(
        [
            master,
            rows_to_add
        ],
        ignore_index=True
    )


    # ==========================
    # Sort by date
    # ==========================

    updated_master.sort_values(
        by=DATE_COLUMN,
        inplace=True,
        kind="stable"
    )

    updated_master.reset_index(
        drop=True,
        inplace=True
    )


    # ==========================
    # Rebuild IDs
    # ==========================

    if ID_COLUMN is not None and ID_COLUMN in updated_master.columns:

        updated_master[ID_COLUMN] = range(
            1,
            len(updated_master) + 1
        )

        # Put ID first
        id_column = updated_master.pop(ID_COLUMN)

        updated_master.insert(
            0,
            ID_COLUMN,
            id_column
        )


    # ==========================
    # Format dates for output
    # ==========================

    updated_master[DATE_COLUMN] = (
        updated_master[DATE_COLUMN]
        .dt.strftime("%m/%d/%Y")
    )


    # ==========================
    # Save output
    # ==========================

    updated_master.to_csv(
        OUTPUT_FILE,
        index=False
    )


    print(
        f"Saved updated master to {OUTPUT_FILE}"
    )

    print(
        f"Total transactions: "
        f"{len(updated_master)}"
    )

    if ID_COLUMN is not None and ID_COLUMN in updated_master.columns:
        print(
            f"IDs: 1 through {len(updated_master)}"
        )


# ==========================
# Run
# ==========================

if __name__ == "__main__":
    main()