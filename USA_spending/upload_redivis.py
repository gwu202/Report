import os
import glob
import redivis
import redivis.classes.Table

# from pathlib import Path

os.environ["REDIVIS_API_TOKEN"] = 'AAACLh/rVCpoH0mc7jxfQjrmAHaWgdvV'

# filepaths = glob.glob('extracted content/*.csv')

names = {'FY2023P01-P09_All_FA_AccountBalances_2023-08-22_H08M13S10_1.csv': 'Federal Account: All Account Balances',
         'FY2023P01-P09_All_FA_AccountBreakdownByPA-OC_2023-08'
         '-22_H08M19S34_1.csv':
             'Federal Account: All Account Breakdown by Protection Agency',
         'FY2023P01-P09_All_FA_Assistance_AccountBreakdownByAward_2023'
         '-08-22_H08M14S25_1.csv': 'Federal Account: All Assistance Account Breakdown by Award',
         'FY2023P01-P09_All_FA_Contracts_AccountBreakdownByAward_2023-08-22_H08M13S12_1.csv':
             'Federal Account: All Contracts Account Breakdown by Award',
         'FY2023P01-P09_All_FA_Unlinked_AccountBreakdownByAward_2023-08-22_H08M15S13_1.csv':
             'Federal Account: All Unlinked Account Breakdown by Award'}


# dataset = redivis.user("user_name").dataset("dataset_name", version="next")


def create_dataset_upload(dataset_name, filename, organization_name='EIDC'):
    # Could also create a dataset under an organization:
    global table_name
    dataset = redivis.organization(organization_name).dataset(dataset_name)

    # public_access_level can be one of ('none', 'overview', 'metadata', 'sample', 'data')
    dataset.create(public_access_level="data")
    for name in names.values():
        # table_name = name

        # create table
        table = (
            dataset
            .table(name)
            .create(description="Some description")
        )

        # upload table
        upload = table.upload(filename)  # table_name
        with open(filename, "rb") as file:
            upload.create(
                file,
                type="delmited",
                remove_on_fail=True,  # Remove the upload if a failure occurs
                wait_for_finish=True,  # Wait for the upload to finish processing
                raise_on_fail=True  # Raise an error on failure
            )


# Create a table on the dataset. Datasets may have multiple tables

names.values()
# def create_table(dataset, table_name=names.values()):  # -> redivis.classes.Table.Table
# for name in names.values():
# table_name = name


# return table


# def upload_table(table, filename='C:/Users/bezal/PycharmProjects/report/USA_spending/extracted content'):


# Upload a file to the table.
# You can create multiple uploads per table, in which case they'll be appended together.
