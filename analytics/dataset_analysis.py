import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "processed" / "papers_clean.csv"

def load_dataset():
    print("Loading dataset...")
    df = pd.read_csv(INPUT_FILE)
    df = pd.read_csv(INPUT_FILE)
    return df

def basic_info(df):
    print("-----Basic Info-----")
    print(f"Number of papers: {len(df)}")
    print("Columns: ")
    print(df.columns.tolist())
    print("-----")

def missing_values(df):
    print("-----Missing Values-----")
    print(df.isnull().sum())
    print("-----")

def year_distribution(df):
    print("-----Year Distribution-----")
    print(df.groupby(["year"]).size())
    print("-----")

def abstract_length(df):
    print("-----Abstract Length-----")
    df["abstract_length"] = df["abstract"].str.split().str.len()

    print(f"Average length: {df['abstract_length'].mean():.2f}")
    print(f"Min length: {df['abstract_length'].min()}")
    print(f"Max length: {df['abstract_length'].max()}")
    print("-----")

def category_distribution(df):
    print("-----Category Distribution-----")
    print(df["category"].value_counts())

if __name__ =="__main__":
    df = load_dataset()
    basic_info(df)
    missing_values(df)
    year_distribution(df)
    abstract_length(df)
    category_distribution(df)

    print("Dataset validation complete")