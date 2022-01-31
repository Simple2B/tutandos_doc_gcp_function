from typing import List
import csv
import pandas as pd
import dateutil.parser as parser

# converts a decimal to a pc
def to_percentage(x: float):
    return "{:.0%}".format(x)


def write_to_csv(filepath: str, row: List[str]):
    # Appends row to csv file
    # row = ['4', ' Danny', ' New York']

    try:
        with open(filepath, 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)

        csvFile.close()
    except:
        print(f"An exception occurred whilst writing logs ({row}) to {filepath}")


def read_csv(filepath: str):
    df = pd.read_csv(filepath)
    return df
