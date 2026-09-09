import pandas as pd

# ==========================
# Configuration
# ==========================
MASTER_FILE = "./data/prod_transactions.csv"
NEW_FILE = "./scripts/temp/temp_master_transactions.csv"
OUTPUT_FILE = "./data/prod_transactions.csv"

DATE_COLUMN = "Date"
KEY_COLUMNS = [
    "Date",
    "Description",
    "Amount"
]

# Date format examples:
# "%m/%d/%Y"
# "%Y-%m-%d"
# Leave as None to let pandas detect automatically.
DATE_FORMAT = "%m/%d/%Y"


def load_csv(filename):
    df = pd.read_csv(filename)

    if DATE_FORMAT:
        df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN], format=DATE_FORMAT)
    else:
        df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN])

    return df


def main():

    master = load_csv(MASTER_FILE)
    new = load_csv(NEW_FILE)

    # Preserve original column order
    columns = master.columns.tolist()

    master_keys = set(
        tuple(row) for row in master[KEY_COLUMNS].itertuples(index=False, name=None)
    )

    # Find latest date in master
    last_date = master[DATE_COLUMN].max()

    print(f"Last date in master: {last_date.date()}")

    # Everything after the last date
    future_rows = new[new[DATE_COLUMN] > last_date]

    # Rows on the last date
    master_last_day = master[master[DATE_COLUMN] == last_date]
    new_last_day = new[new[DATE_COLUMN] == last_date]

    # Compare full rows
    merged = new_last_day.merge(
        master_last_day,
        how="left",
        indicator=True
    )

    new_same_day_rows = merged[merged["_merge"] == "left_only"][columns]

    rows_to_add = new[
       ~new[KEY_COLUMNS]
            .apply(tuple, axis=1)
            .isin(master_keys)
    ]
    # rows_to_add = pd.concat(
    #     [new_same_day_rows, future_rows],
    #     ignore_index=True
    # )

    print(f"New rows found: {len(rows_to_add)}")
    if (len(rows_to_add) > 0): 
        updated_master = pd.concat(
            [master, rows_to_add],
            ignore_index=True
        )

        updated_master.sort_values(DATE_COLUMN, inplace=True)
        # Format dates for the output CSV
        updated_master[DATE_COLUMN] = updated_master[DATE_COLUMN].dt.strftime("%m/%d/%Y")
        updated_master.to_csv(OUTPUT_FILE, index=False)
    
        print(f"Saved updated master to {OUTPUT_FILE}")
    else:
        print("No updates made")

    

if __name__ == "__main__":
    main()