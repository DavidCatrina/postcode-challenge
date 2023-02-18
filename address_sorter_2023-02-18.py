import pandas as pd
import numpy as np

# Read the csv files into dataframes
users_address_df = pd.read_csv('example_input_data.csv')
post_office_address_df = pd.read_csv('example_abp_data.csv')

# Create a dictionary mapping postcodes to sets of streets at that postcode
streets_by_postcode = {}
for _, row in post_office_address_df.iterrows():
    postcode = row['POSTCODE']
    if pd.notna(postcode):
        if postcode not in streets_by_postcode:
            streets_by_postcode[postcode] = set()
        streets_by_postcode[postcode].add(row['STREET_NAME'])

# Create a list to hold the new column values
street_in_postcode = []

# clean users_address_df dataframe from numbers and special characters
for col in ["Address_Line_1", "Address_Line_2", "Address_Line_3", "Address_Line_4", "Address_Line_5"]:
    #set dtype as str to all row values
    users_address_df[col] = users_address_df[col].astype('str')

    # Create new address lines columns that are cleaned
    # Remove all numerical values and characters in between from street address columns - keep just the street name
    users_address_df[col+"_new"] = users_address_df[col].str.replace(r'\d+[^a-zA-Z]*', '')

    #fill empty row values
    users_address_df[col+"_new"] = np.where(users_address_df[col].empty, 'NaN',users_address_df[col])


# Loop over the users_address_df dataframe and check whether each address's street is in the
# set of streets at that postcode
for _, row in users_address_df.iterrows():
    postcode = row['Postcode']

    # loop over each Address line new columns
    streets = np.array(['Address_Line_1_new','Address_Line_2_new','Address_Line_3_new','Address_Line_4_new','Address_Line_5_new'])

    for street_columns in streets:

        found_street = False
        street = row[street_columns]
        if pd.notna(postcode):
            # check if any of the values from address line new columns is in the post office streets set for that specific postcode
            if postcode in streets_by_postcode and street in streets_by_postcode[postcode]:
                street_in_postcode.append('Yes')
                found_street = True
                break
            else:
                found_street = False
                pass
        else:
            found_street = False
            pass

    if found_street == False:
        street_in_postcode.append('No')
    else:
        pass

# Add the new column to the input data
users_address_df['Street_In_Postcode'] = street_in_postcode

users_address_df = users_address_df.drop(['Address_Line_1_new','Address_Line_2_new','Address_Line_3_new','Address_Line_4_new','Address_Line_5_new'], axis=1)

# Write the output data to a CSV file
users_address_df.to_csv('output_data.csv', index=False)