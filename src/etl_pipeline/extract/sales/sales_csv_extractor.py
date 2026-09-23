import csv
from pathlib import Path
import pandas as pd
from charset_normalizer import from_path
from ftfy.badness import sequence_weirdness

def extract_sales_data(file_path: str) -> pd.DataFrame:
    path = Path(file_path)

    if path.suffix.lower() != ".csv":
        raise ValueError(f"Expected a .csv file, got: {path.suffix or 'no extension'}")

    if not path.exists():
        raise FileNotFoundError(f"Sales CSV not found: {path}")

    # detect encoding
    result = from_path(path).best()
    if result is None:
        raise ValueError(f"Could not detect encoding for: {path}")
    encoding = result.encoding

    if result.chaos > 0:
        raise ValueError(
            f"Encoding detection for '{path.name}' was ambiguous (best guess: {encoding}). "
            f"Refusing to proceed automatically — verify the source encoding manually."
        )

    # general-purpose mojibake check
    with path.open(encoding=encoding) as f:
        sample_text = f.read(8192)

    weirdness = sequence_weirdness(sample_text)
    if weirdness > 0:
        raise ValueError(
            f"File '{path.name}' decoded as '{encoding}' but text weirdness score "
            f"is {weirdness} (expected 0 for clean text) — likely mis-decoded. "
            f"Verify the source encoding manually."
        )

    # detect delimiter
    with path.open(newline="", encoding=encoding) as f:
        sample = f.read(4096)
        dialect = csv.Sniffer().sniff(sample)
        delimiter = dialect.delimiter

    if delimiter != ",":
        print(f"Note: file uses '{delimiter}' as separator, not a comma.")

    return pd.read_csv(path, sep=delimiter, encoding=encoding)

if __name__ == "__main__":
    df = extract_sales_data(r"/raw_data/20260904_sales_data.csv")
    print(df.head())