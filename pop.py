import pandas as pd

# Load original dataset
df = pd.read_csv("zomato_master_cleaned.csv")

# Drop completely empty columns (N through S)
columns_to_drop = [
    "orderitemid",
    "fooditemid",
    "foodname",
    "food_category",
    "quantity",
    "unitprice",
]
df = df.drop(columns=columns_to_drop, errors="ignore")

# Remove duplicate rows
df = df.drop_duplicates()

# Filter out non-fulfilled orders
df_fulfilled = df[
    ~df["orderstatus"].isin(["Cancelled", "Food Not Delivered"])
].copy()

# Save output files
df.to_csv("zomato_cleaned_all_orders.csv", index=False)
df_fulfilled.to_csv("zomato_cleaned_fulfilled_orders.csv", index=False)

print("Data cleaning complete! Check your folder for the new CSV files.")