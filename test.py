import pandas as pd
import time
from datetime import datetime as dt

class Utility:
    # Placeholder for utility functions
    def excel_to_df(self, filename):
        return pd.read_excel(filename)  # Assuming this function reads an Excel file into a DataFrame

# Example Utility class instantiation
utility_obj = Utility()

# Initialize the DataFrame
df = pd.DataFrame()

while True:
    if df.empty:
        df_init = utility_obj.excel_to_df('active_calls_2024-12-03_012529.xlsx')
        df = df_init.copy()
        print(f'{df}\n')
    else:
        datetime = dt.now().strftime('%Y-%m-%d %H:%M:%S')
        df_compare = utility_obj.excel_to_df('active_calls_2024-12-03_012535.xlsx')
        
        # Merge data to find new and updated records
        merged = pd.merge(df, df_compare, on='ID', suffixes=('_init', '_compare'), how='outer', indicator=True)
        print(merged)

        # Identify new and updated records
        new_records = merged[merged['_merge'] == 'right_only']
        updated_records = merged[(merged['_merge'] == 'both') & (merged['Call Status_init'] != merged['Call Status_compare'])]

        if not new_records.empty:
            print('rows added')
            new_records['Previous Call Status'] = None
            new_records['Call Status Indicator'] = datetime
            df = pd.concat([df, new_records[df.columns]], ignore_index=True)
        
        if not updated_records.empty:
            print('updating statuses')
            for index, row in updated_records.iterrows():
                df.loc[df['ID'] == row['ID'], 'Previous Call Status'] = row['Call Status_init']
                df.loc[df['ID'] == row['ID'], 'Call Status'] = row['Call Status_compare']
                df.loc[df['ID'] == row['ID'], 'Call Status Indicator'] = datetime

        print(df)
        
        # Update df_init for the next iteration
        df_init = df_compare.copy()

        # Sleep for a while before the next iteration
        time.sleep(5)
