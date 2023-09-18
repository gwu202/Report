import os
import re

from usa_spending.spiders.upload_redivis import create_dataset, csv_to_table_name, create_table, upload_file

csv_to_table_name = {
    'FY2023P01-P09_All_FA_AccountBalances_2023-08-22_H08M13S10_1.csv': 'Federal Account: All Account Balances',
    'FY2023P01-P09_All_FA_AccountBreakdownByPA-OC_2023-08-22_H08M19S34_1.csv':
        'Federal Account: All Account Breakdown by Protection Agency',
    'FY2023P01-P09_All_FA_Assistance_AccountBreakdownByAward_2023-08-22_H08M14S25_1.csv': 'Federal Account: All Assistance Account Breakdown by Award',
    'FY2023P01-P09_All_FA_Contracts_AccountBreakdownByAward_2023-08-22_H08M13S12_1.csv':
        'Federal Account: All Contracts Account Breakdown by Award',
    'FY2023P01-P09_All_FA_Unlinked_AccountBreakdownByAward_2023-08-22_H08M15S13_1.csv':
        'Federal Account: All Unlinked Account Breakdown by Award'}


filenames= ['FY2023P01-P09_All_FA_Unlinked_AccountBreakdownByAward_2023-08-22_H08M15S13_1.csv',
 'FY2023P01-P09_All_FA_AccountBreakdownByPA-OC_2023-08-23_H20M35S51_1.csv',
 'FY2023P01-P09_All_FA_Assistance_AccountBreakdownByAward_2023-08-23_H20M30S07_1.csv',
 'FY2023P01-P09_All_FA_Contracts_AccountBreakdownByAward_2023-08-29_H00M16S14_1.csv',
 'FY2023P01-P09_All_FA_Unlinked_AccountBreakdownByAward_2023-08-23_H20M31S09_1.csv',
 'FY2023P01-P09_All_FA_AccountBalances_2023-08-29_H00M16S12_1.csv',
 'FY2023P01-P09_All_FA_Unlinked_AccountBreakdownByAward_2023-08-29_H00M18S08_1.csv',
 'FY2023P01-P09_All_FA_Assistance_AccountBreakdownByAward_2023-08-22_H08M14S25_1.csv',
 'FY2023P01-P09_All_FA_Contracts_AccountBreakdownByAward_2023-08-23_H20M28S47_1.csv',
 'FY2023P01-P09_All_FA_Assistance_AccountBreakdownByAward_2023-08-29_H00M17S20_1.csv',
 'FY2023P01-P09_All_FA_AccountBreakdownByPA-OC_2023-08-29_H00M22S19_1.csv',
 'FY2023P01-P09_All_FA_AccountBalances_2023-08-22_H08M13S10_1.csv',
 'FY2023P01-P09_All_FA_AccountBalances_2023-08-23_H20M28S45_1.csv',
 'FY2023P01-P09_All_FA_Contracts_AccountBreakdownByAward_2023-08-22_H08M13S12_1.csv',
 'FY2023P01-P09_All_FA_AccountBreakdownByPA-OC_2023-08-22_H08M19S34_1.csv']
if __name__ == '__main__':
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
    for filename in filenames:
        for pattern, description in patterns:
            if re.search(pattern, filename):
                filename_to_description[filename] = description
                break  # Break once a pattern is matched

    # Print the resulting dictionary
    for filename, description in filename_to_description.items():
        print(f"'{filename}' maps to: '{description}'")