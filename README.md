# Bravado_Health_Patient_Import
Bravado Health standalone eRX system.
The import system give zero fault codes on upload failures. 
Though trial and error was able to pinpoint where our data was failing and wrote a script to clean our SQL output for upload.

Even after perfect formatting, the .csv wouldn't upload. Converting to .json worked.

So here is a file to clean up your patient demographic export before uploading to Bravado Health standalone prescription portal.

### Steps

1.  Make sure you have a .csv (comma separated file) with these columns at a minimum :
```
firstName, lastName, dateOfBirth, street, city, state, zip
```

If you have any patients in the .csv that are under 12, you __must__ include their weight:
```
firstName, lastName, dateOfBirth, weight, street, city, state, zip
```

I added the email and mobile to make reaching patients more simple:
```
firstName, lastName, dateOfBirth, street, city, state, zip, email, mobileNumber
```
2.  Change filename to `Master_Export.csv` and save in same directory as the `convert_csv_to_json.py` file

3.  Run `convert_csv_to_json.py` and it will:
*  verify zipcode
*  verify email complete
*  remove apostrophe from first and-or last name
*  verify JSON format
*  saves output in files holding 2000 records each named `1_output_json.json, 2_output_json.json, etc` 
*  saves output as a single file named `single_file_patients_json.json`.

The 2,000 is a nice number to work with. If some batches upload and some fail, it is easier to identify the fault than one huge file that fails completely.

### Templates
The Bravado Health templates are 
*  template.csv 
*  template.json


https://www.bravadohealth.com/treat/

help file: https://support.bravadohealth.com/hc/en-us/articles/360044753974
