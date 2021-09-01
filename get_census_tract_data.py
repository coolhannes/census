from census import Census
import numpy as np
import os
import pandas as pd
from us import states

# Defining the census_response_df tool which takes API response dictionaries and transforms them into dataframes
def census_response_df(response_dict,col_names,new_names):
    data = []
    for d in response_dict:
        items = [float(d[i]) for i in col_names]
        items.append(d['state']+d['county']+d['tract'])
        data.append(items)
    df = pd.DataFrame(data,columns=new_names)
    return df

# Save your Census API Key in a text file in the same directory as this script
# https://api.census.gov/data/key_signup.html
ckey = open('census_key.txt').readline().rstrip()

# Set variables for the census function (api key and vintage)
c = Census(ckey, year=2019)

# Dictionary of census columns and user-chosen accessible names
# Columns will be named these accessble names at the end in the data frame and CSV
# Census API Ref: https://api.census.gov/data/2019/acs/acs5/groups.html

acs_items = {
    'B19013_001E': 'median_household_income',
    'B19083_001E': 'gini_estimate',
    'B01002_001E': 'median_age',
    'B01003_001E': 'pop_total',
    'B02001_002E': 'pop_white',
    'B02001_003E': 'pop_black',
    'B03001_003E': 'pop_hispanic',
    'B03001_008E': 'hispanic_central_american',
    'B03001_006E': 'hispanic_cuban',
    'B03001_004E': 'hispanic_mexican',
    'B03001_025E': 'hispanic_venezuelan',
    'B05002_013E': 'pop_foreign_born',
    'B25007_001E': 'units_total',
    'B25007_002E': 'units_owner_occupied',
    'B25007_012E': 'units_renter_occupied',
    'B15003_001E': 'edu_eligible_pop',
    'B15003_002E': 'edu_no_school',
    'B15003_017E': 'edu_high_school',
    'B15003_018E': 'edu_ged',
    'B15003_020E': 'edu_some_college',
    'B15003_022E': 'edu_bachelors',
    'B15003_023E': 'edu_masters',
    'B15003_024E': 'edu_professional',
    'B15003_025E': 'edu_doctorate',
    'B17001_002E': 'pop_poverty_last_year',
    'B19052_001E': 'hh_total',
    'B19052_002E': 'hh_salary_income',
    'B19053_002E': 'hh_self_employed',
    'B19054_002E': 'hh_passive_income',
    'B19055_002E': 'hh_social_security_income',
    'C17002_001E': 'income_to_poverty_total',
    'C17002_002E': 'income_to_pov_ratio_under_50',
    'C17002_003E': 'income_to_pov_ratio_50_to_99',
    'C17002_004E': 'income_to_pov_ratio_100_to_124',
    'C17002_005E': 'income_to_pov_ratio_125_to_149',
    'C17002_006E': 'income_to_pov_ratio_150_to_184',
    'C17002_007E': 'income_to_pov_ratio_185_to_199',
    'C17002_008E': 'income_to_pov_ratio_2_plus',
    'B19052_001E': 'hh_with_wage_or_salary_income_total',
    'B19052_002E': 'hh_with_wage_or_salary_income',
    'B19057_001E': 'hh_with_public_assistance_income_total',
    'B19057_002E': 'hh_with_public_assistance_income',
    'B09002_001E': 'own_children',
    'B09002_002E': 'own_children_married',
    'B09002_009E': 'own_children_male_only_hoh',
    'B09002_015E': 'own_children_female_only_hoh',
    'B21002_002E': 'veteran_gulf_war_2001',
    'B21002_003E': 'veteran_gulf_war_2001_1990',
    'B21002_004E': 'veteran_gulf_war_2001_1990_vietnam',
    'B21002_005E': 'veteran_gulf_war_1990',
    'B21002_006E': 'veteran_gulf_war_1990_vietnam',
    'B21002_007E': 'veteran_vietnam',
    'B21002_008E': 'veteran_vietnam_korea',
    'B21002_009E': 'veteran_vietnam_korea_wwii',
    'B21002_010E': 'veteran_korea',
    'B21002_011E': 'veteran_korea_wwii',
    'B21002_012E': 'veteran_wwii',
    'B21002_013E': 'veteran_between_gulf_war_vietnam',
    'B21002_014E': 'veteran_between_vietnam_korea',
    'B21002_015E': 'veteran_between_korea_wwii',
    'B21002_016E': 'veteran_before_wwii',
    'B11001_001E': 'hh_family_type_total',
    'B11001_003E': 'hh_family_type_married',
    'B11001_005E': 'hh_family_type_male_householder_no_spouse',
    'B11001_006E': 'hh_family_type_female_householder_no_spouse',
    'B11001_008E': 'hh_family_type_householder_living_alone',
    'B25081_001E': 'housing_units_total',
    'B25081_002E': 'housing_units_with_mortgage',
    'B14002_001E': 'school_population_over_three',
    'B14002_032E': 'school_female_kindergarten_public',
    'B14002_008E': 'school_male_kindergarten_public',
    'B14002_035E': 'school_female_elementary_public',
    'B14002_011E': 'school_male_elementary_public',
    'B14002_038E': 'school_female_middle_public',
    'B14002_014E': 'school_male_middle_public',
    'B14002_041E': 'school_female_high_public',
    'B14002_017E': 'school_male_high_public',
    'B14002_033E': 'school_female_kindergarten_private',
    'B14002_009E': 'school_male_kindergarten_private',
    'B14002_036E': 'school_female_elementary_private',
    'B14002_012E': 'school_male_elementary_private',
    'B14002_039E': 'school_female_middle_private',
    'B14002_015E': 'school_male_middle_private',
    'B14002_042E': 'school_female_high_private',
    'B14002_018E': 'school_male_high_private',
    'B27010_001E': 'insurance_total',
    'B27010_017E': 'insurance_under_19_no_coverage',
    'B27010_033E': 'insurance_under_35_no_coverage',
    'B27010_050E': 'insurance_under_66_no_coverage',
    'B27010_066E': 'insurance_over_65_no_coverage',
    'B25087_002E': 'mortgage_monthly_total',
    'B25087_003E': 'mortage_monthly_owner_costs_under_200',
    'B25087_004E': 'mortage_monthly_owner_costs_200_to_299',
    'B25087_005E': 'mortage_monthly_owner_costs_300_to_399',
    'B25087_006E': 'mortage_monthly_owner_costs_400_to_499',
    'B25087_007E': 'mortage_monthly_owner_costs_500_to_599',
    'B25087_008E': 'mortage_monthly_owner_costs_600_to_699',
    'B25087_009E': 'mortage_monthly_owner_costs_700_to_799',
    'B25087_010E': 'mortage_monthly_owner_costs_800_to_899',
    'B25087_011E': 'mortage_monthly_owner_costs_900_to_999',
    'B25087_012E': 'mortage_monthly_owner_costs_1000_to_1249',
    'B25087_013E': 'mortage_monthly_owner_costs_1250_to_1499',
    'B25087_014E': 'mortage_monthly_owner_costs_1500_to_1999',
    'B25087_015E': 'mortage_monthly_owner_costs_2000_to_2499',
    'B25087_016E': 'mortage_monthly_owner_costs_2500_to_2999',
    'B25087_017E': 'mortage_monthly_owner_costs_3000_to_3499',
    'B25087_018E': 'mortage_monthly_owner_costs_3500_to_3999',
    'B25087_019E': 'mortage_monthly_owner_costs_over_4000',
    'C24050_001E': 'occupation_total',
    'C24050_002E': 'occupation_agriculture_hunting_mining',
    'C24050_003E': 'occupation_construction',
    'C24050_004E': 'occupation_manufacturing',
    'C24050_005E': 'occupation_wholesale_trade',
    'C24050_006E': 'occupation_retail_trade',
    'C24050_007E': 'occupation_transportation_warehousing',
    'C24050_008E': 'occupation_information',
    'C24050_009E': 'occupation_finance_realestate',
    'C24050_010E': 'occupation_pmc',
    'C24050_011E': 'occupation_education_health',
    'C24050_012E': 'occupation_arts_entertainment_food',
    'C24050_013E': 'occupation_other_services',
    'C24050_014E': 'occupation_public_admin',
    'C16002_001E': 'hh_lang_total',
    'C16002_003E': 'hh_lang_spanish',
    'C16002_006E': 'hh_lang_other_indoeuro',
    'C16002_009E': 'hh_lang_aapi',
    'C16002_012E': 'hh_lang_other',
    'B28001_001E': 'computer_hh_total',
    'B28001_002E': 'computer_hh_devices_any',
    'B28001_003E': 'computer_hh_devices_computer',
    'B28001_005E': 'computer_hh_devices_smartphone',
    'B28001_011E': 'computer_hh_devices_none',
    'B28002_001E': 'internet_hh_total',
    'B28002_002E': 'internet_subscription',
    'B28002_012E': 'internet_no_subscription',
    'B28002_003E': 'internet_dialup_subscription',
    'B28002_004E': 'internet_broadband',
    'B28002_013E': 'internet_none',
}

# Turn the dictionary into two lists that are easily processed. Adding the census_tract_id column name
col_names = list(acs_items.keys())
names = list(acs_items.values())
new_names = names + ['census_tract_id']

# Bind each state together into a big dataframe
df = pd.concat([census_response_df(c.acs5.state_county_tract(col_names, state.fips, Census.ALL, Census.ALL),col_names,new_names) for state in states.STATES],ignore_index=True)

# Make sure numbers are numbers
for name in names:
    df[name] = df[name].astype(float)

# Make sure missing values are missing
df = df.replace(-666666666.,np.nan)

# Write dataframe to CSV
df.to_csv("census_tract_acs_2019.csv",index=False)
