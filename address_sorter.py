import numpy as np
import pandas as pd
import re

# Read the csv files into dataframes
users_address_df = pd.read_csv('example_input_data.csv')
post_office_address_df = pd.read_csv('example_abp_data.csv')

## post_office_address_df modelling
#Extract unique postcodes and street names from 'example_abp_data.csv'
unique_postcode_and_street = post_office_address_df[['POSTCODE', 'STREET_NAME']].drop_duplicates()

#Create a new dataframe with of those unique values
post_office_address_unique_df = pd.DataFrame(unique_postcode_and_street)

#Drop the rows that have no street name or postcode
post_office_address_unique_df = post_office_address_unique_df.dropna(subset=['STREET_NAME','POSTCODE'])

#Rename postcode column
users_address_df = users_address_df.rename(columns={'Postcode': 'POSTCODE'})

#Merge users_address_df and post_office_address_unique_df on POSTCODE column
merged_df = pd.merge(users_address_df, post_office_address_unique_df, on='POSTCODE', how='inner')

## merged_df modelling
for col in ["Address_Line_1", "Address_Line_2", "Address_Line_3", "Address_Line_4", "Address_Line_5"]:
    #set dtype as str to all row values
    merged_df[col] = merged_df[col].astype('str')

    # Create new address lines columns that are cleaned
    # Remove all numerical values and characters in between from street address columns - keep just the street name
    merged_df[col+"_new"] = merged_df[col].str.replace(r'\d+[^a-zA-Z]*', '')
    # merged_df[col+"_new"] = merged_df[col].str.replace('[0-9]+[^a-zA-Z]*', '')

    
    #fill empty row values
    merged_df[col+"_new"] = np.where(merged_df[col].empty, 'NaN',merged_df[col])


# check if any of the Address Lines are in STREET_NAME column
merged_df['Street_In_Postcode'] = merged_df.apply(lambda row: 'Yes' if 
    (row['Address_Line_1_new'] in row['STREET_NAME']) or 
    (row['Address_Line_2_new'] in row['STREET_NAME']) or
    (row['Address_Line_3_new'] in row['STREET_NAME']) or
    (row['Address_Line_4_new'] in row['STREET_NAME']) or
    (row['Address_Line_5_new'] in row['STREET_NAME']) else 'No', axis=1)

#drop additional columns created for data modelling
merged_df = merged_df.drop(['Address_Line_1_new','Address_Line_2_new','Address_Line_3_new','Address_Line_4_new','Address_Line_5_new','STREET_NAME'], axis=1)

#export the dataframe to a csv
merged_df.to_csv('output.csv', index=False)

print(merged_df)
