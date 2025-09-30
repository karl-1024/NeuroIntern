import pandas as pd

CSV_PATH = "final_final_allsubj_personality_coded.xlsx"  # Path to your Excel file

df_sheets = pd.read_excel(CSV_PATH, sheet_name = None)
merged_df = None
for name, df in df_sheets.items():
    df = df.copy()
    if merged_df is None:
        merged_df = df
    else:
        # Merge on 'ID', keep all IDs (outer join)
        merged_df = pd.merge(merged_df, df, on="sub#", how="outer", suffixes=('', f'_{name}'))

CSV_PATH_2 = "allsubj_personality(2).xlsx"
worksheet = pd.read_excel(CSV_PATH_2, sheet_name= '工作表1')
opposing_update_one = worksheet.loc[0:44, '1stUpdated']
opposing_update_two = worksheet.loc[45:86, '2ndUpdate']
opposing_update = pd.concat([opposing_update_one, opposing_update_two], ignore_index=True)
supporting_update_one = worksheet.loc[0:44, '2ndUpdate']
supporting_update_two = worksheet.loc[45:86, '1stUpdated']
supporting_update = pd.concat([supporting_update_one, supporting_update_two], ignore_index=True)
opposing_update = pd.Series(opposing_update)
supporting_update = pd.Series(supporting_update)
merged_df['opposing_update'] = opposing_update
merged_df['supporting_update'] = supporting_update
merged_df.to_csv("final_final_allsubj_personality_coded.csv", index = False)
df_raw = pd.read_csv("final_final_allsubj_personality_coded.csv") #converts xlsx to csv