# Bravado_Health_Patient_Import
Bravado Health standalone eRX system.
The import system give zero fault codes.
Though trial and error was able to pinpoint where our data was failing. 

Eventually determined the data errors and that the CSV import non-functional.

Save .csv file in main directory and name it "Master_Export.csv"
Make sure you have the minimum columns:
```
firstName, lastName, dateOfBirth, street, city, state, zip
```
I added the email and mobile to make reaching patients more simple:
```
email, mobileNumber
```

Run convert_csv_to_json.py and it will:
*  verify zipcode
*  verify email complete
*  remove apostrophe from first and-or last name
*  verify JSON format
*  save in files with 2,000 records and a master file: single_file_patients_json.json

The 2,000 is a nice number that if successful, won't take too long but if an issue, you can use elimination to identify which files fail.

### Templates
The Bravado Health templates are 
*  template.csv 
*  template.json


https://www.bravadohealth.com/treat/

help file: https://support.bravadohealth.com/hc/en-us/articles/360044753974
