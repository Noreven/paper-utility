import os
from pathlib import Path
import pandas as pd

DATA_PATH = Path(os.path.dirname(__file__)) / "data"


def load_csv(filename: str) -> pd.DataFrame:
    path = DATA_PATH / filename
    df = pd.read_csv(path)
    return df


def parse_text_new_line(text: str):
    n = 100
    text = text.replace("\n", " ")
    parts = [text[i : i + n] for i in range(0, len(text), n)]
    return "\n".join(parts)


def parse_csv_for_edit(filename: str) -> pd.DataFrame:
    df = load_csv(filename)
    df["fulltext"] = df["fulltext"].apply(parse_text_new_line)
    return df[["fulltext", "label"]]


def save_labels(labels: list, df_name: str):
    df = load_csv(df_name)
    df["label"] = labels
    df.to_csv(DATA_PATH / df_name, index=False)
