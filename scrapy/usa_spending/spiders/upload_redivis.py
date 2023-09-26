import os
import glob
import re

import pandas as pd
import redivis
import redivis.classes.Table

# from pathlib import Path
from redivis.classes.Dataset import Dataset
from dotenv import load_dotenv

load_dotenv()

# Retrieve the secret
os.environ["REDIVIS_API_TOKEN"] = os.getenv("TOKEN")


def filename_to_table_name(filename):
    patterns = [
        (r'Unlinked_AccountBreakdownByAward', 'Federal Account: All Unlinked Account Breakdown by Award'),
        (r'AccountBalances', 'Federal Account: All Account Balances'),
        (r'AccountBreakdownByPA', 'Federal Account: All Account Breakdown by Protection Agency'),
        (r'Assistance_AccountBreakdownByAward', 'Federal Account: Assistance Account Breakdown by Award'),
        (r'Contracts_AccountBreakdownByAward', 'Federal Account: All Contracts Account Breakdown by Award')
    ]

    # Create an empty dictionary to store the filename-description pairs
    filename_to_description = {}

    # Loop through filenames and patterns to populate the dictionary
    for pattern, description in patterns:
        if re.search(pattern, filename):
            return description


# dataset = redivis.user("user_name").dataset("dataset_name", version="next")
def create_dataset(dataset_name, organization_name='EIDC') -> Dataset:
    # dataset = redivis.organization(organization_name).dataset(dataset_name)
    dataset = redivis.user("khgha1").dataset(dataset_name)
    dataset.create(public_access_level="data")
    return dataset


def create_table(dataset, table_name, description="Some description"):
    table = (
        dataset
            .table(table_name)
            .create(description=description)
    )
    return table


def upload_file(table, filename, **kwargs):
    upload = table.upload(filename)  # table_name
    with open(filename, "rb") as file:
        upload.create(
            file,
            remove_on_fail=True,  # Remove the upload if a failure occurs
            wait_for_finish=True,  # Wait for the upload to finish processing
            raise_on_fail=True  # Raise an error on failure
        )


def upload_xlsx(excel_file_path, dataset_name):
    xls = pd.ExcelFile(excel_file_path)
    sheet_names = [sheet_name for sheet_name in xls.sheet_names if sheet_name not in ['Read Me', 'ReadMe']]
    dataset = create_dataset(dataset_name)
    for sheet_name in sheet_names:
        df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
        csv_file_name = f'{sheet_name}.csv'
        df.to_csv(csv_file_name, index=False)
        table = create_table(dataset, sheet_name)
        upload_file(table, f'{sheet_name}.csv')
        print(f'"{sheet_name}" has been converted to "{csv_file_name}".')
        os.remove(csv_file_name)
