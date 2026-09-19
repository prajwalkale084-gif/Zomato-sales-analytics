import pandas as pd

# Load the CSV file
df = pd.read_csv(r"C:\Users\sus\Desktop\zomato.pi\zomato_master_cleaned.csv")

# Drop unnecessary columns
columns_to_drop = [
    "orderitemid",
    "fooditemid",
    "foodname",
    "food_category",
    "quantity",
    "unitprice",
]
df = df.drop(columns=columns_to_drop, errors="ignore")

# Drop exact duplicate rows
df = df.drop_duplicates()

# Filter for fulfilled orders
df_fulfilled = df[
    ~df["orderstatus"].isin(["Cancelled", "Food Not Delivered"])
].copy()

# Save output files directly to your project folder
df.to_csv(
    r"C:\Users\sus\Desktop\zomato.pi\zomato_cleaned_all_orders.csv", index=False
)
df_fulfilled.to_csv(
    r"C:\Users\sus\Desktop\zomato.pi\zomato_cleaned_fulfilled_orders.csv",
    index=False,
)

print("SUCCESS: Cleaning complete!")