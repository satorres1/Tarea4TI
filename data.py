from gspread.models import Worksheet
import requests
import xml.etree.ElementTree as ET
import pandas as pd
import gspread
import df2gspread as d2g
from gspread_dataframe import get_as_dataframe, set_with_dataframe


albania='http://tarea-4.2021-1.tallerdeintegracion.cl/gho_ALB.xml'
nueva_zelanda='http://tarea-4.2021-1.tallerdeintegracion.cl/gho_NZL.xml'
canada='http://tarea-4.2021-1.tallerdeintegracion.cl/gho_CAN.xml'
australia='http://tarea-4.2021-1.tallerdeintegracion.cl/gho_AUS.xml'
japon='http://tarea-4.2021-1.tallerdeintegracion.cl/gho_JPN.xml'
españa='http://tarea-4.2021-1.tallerdeintegracion.cl/gho_ESP.xml'


r_albania = requests.get(albania)
r_nueva_zelanda = requests.get(nueva_zelanda)
r_canada = requests.get(canada)
r_australia = requests.get(australia)
r_japon = requests.get(japon)
r_españa = requests.get(españa)


albania_tree = ET.fromstring(r_albania.content)
nueva_zelanda_tree = ET.fromstring(r_nueva_zelanda.content)
canada_tree = ET.fromstring(r_canada.content)
australia_tree = ET.fromstring(r_australia.content)
japon_tree = ET.fromstring(r_japon.content)
españa_tree = ET.fromstring(r_españa.content)


all_trees = [albania_tree, nueva_zelanda_tree, canada_tree,
             australia_tree, japon_tree, españa_tree]

all_data = []

gho_index = ["Number of deaths", "Number of infant deaths",
             "Number of under-five deaths", "Mortality rate for 5-14 year-olds (probability of dying per 1000 children aged 5-14 years)",
             "Adult mortality rate (probability of dying between 15 and 60 years per 1000 population)",
             "Estimates of number of homicides", "Crude suicide rates (per 100 000 population)",
             "Mortality rate attributed to unintentional poisoning (per 100 000 population)",
             "Number of deaths attributed to non-communicable diseases, by type of disease and sex",
             "Estimated road traffic death rate (per 100 000 population)", "Estimated number of road traffic deaths",
             "Mean BMI (kg/m&#xb2;) (crude estimate)", "Mean BMI (kg/m&#xb2;) (age-standardized estimate)",
             "Prevalence of obesity among adults, BMI &GreaterEqual; 30 (age-standardized estimate) (%)",
             "Prevalence of obesity among children and adolescents, BMI > +2 standard deviations above the median (crude estimate) (%)",
             "Prevalence of overweight among adults, BMI &GreaterEqual; 25 (crude estimate) (%)",
             "Prevalence of overweight among children and adolescents, BMI > +1 standard deviations above the median (crude estimate) (%)",
             "Prevalence of underweight among adults, BMI < 18.5 (age-standardized estimate) (%)",
             "Prevalence of thinness among children and adolescents, BMI < -2 standard deviations below the median (crude estimate) (%)",
             "Alcohol, recorded per capita (15+) consumption (in litres of pure alcohol)",
             "Estimate of daily cigarette smoking prevalence (%)", "Estimate of daily tobacco smoking prevalence (%)",
             "Estimate of current cigarette smoking prevalence (%)", "Estimate of current tobacco smoking prevalence (%)",
             "Mean systolic blood pressure (crude estimate)", "Mean fasting blood glucose (mmol/l) (crude estimate)",
             "Mean Total Cholesterol (crude estimate)"]


for tree in all_trees:
    for row in tree.findall('Fact'):
        gho = row.find('GHO').text
        if gho in gho_index:
            try:
                country = row.find('COUNTRY').text
                sex = row.find('SEX').text
                year = row.find('YEAR').text
                ghecauses = row.find('GHECAUSES').text
                agegroup = row.find('AGEGROUP').text
                display = row.find('Display').text
                numeric = row.find('Numeric').text
                low = row.find('Low').text
                high = row.find('High').text
                result = {'GHO':gho, 'COUNTRY':country, 'SEX':sex, 'YEAR':year, 'GHECAUSES':ghecauses,
                          'AGEGROUP':agegroup, 'Display':display, 'Numeric':numeric, 'Low':low, 'High':high}

                all_data.append(result)

            except:
                pass

df = pd.DataFrame(data=all_data)
print(df)

spreadsheet_key = '1Yt0xRNR94tJf0TFak2oq-5KxK9d3JK-UsTMEZB6xRY8'


gc=gspread.service_account(filename='credentials.json')
sh=gc.open_by_key('1Yt0xRNR94tJf0TFak2oq-5KxK9d3JK-UsTMEZB6xRY8')
worksheet = sh.get_worksheet(0)
worksheet.clear()
set_with_dataframe(worksheet, df)



