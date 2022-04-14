from icecream import ic
import json
import csv
from pathlib import Path
from email_validator import validate_email, EmailNotValidError


def get_approved_zipcodes():
    """using the USPS get approved zipcodes"""
    zip_list_approved = []
    zipcode_path = Path.cwd() / "zipcode_list.txt"
    zipcode_list = Path.open(zipcode_path, "r")
    zipcode_as_list = csv.reader(zipcode_list)
    # convert to list
    for zipcode in zipcode_list:
        zip_1 = zipcode.strip()
        zip_list_approved.append(zip_1)
    return zip_list_approved


one_big_list = []
one_file_output = {}
output = {}
patients = []


def convert_csv_to_json(zipcode_check):
    quick_check = 0
    file_number = 1
    with open('Master_Export.csv') as csvf:
        csv_reader = csv.DictReader(csvf)
        for rows in csv_reader:
            ic(rows)

            # check if zip code exists, if not, skip record
            if rows['zip'] not in zipcode_check:
                continue

            # remove any hyphens in names
            rows["lastName"] = rows["lastName"].replace("'", "")
            rows["firstName"] = rows["firstName"].replace("'", "")

            # check for email format, delete faulty emails
            if "email" in rows:
                try:
                    valid = validate_email(rows["email"])
                    email_normalize = valid.email
                    if email_normalize:
                        print('looks good', email_normalize)
                        rows["email"] = email_normalize
                    else:
                        print('it was invalid, dont user')
                        rows["email"] = ""
                except EmailNotValidError as e:
                    print(str(e))
                    print("This is the error email: ", rows["email"])
                    rows["email"] = ""

            # after checking for zip, cleaning names and email, add to dict.
            # todo may need additional data screening?  'pydantic'?

            patients.append(rows)
            one_big_list.append(rows)
            quick_check += 1
            if quick_check == 2000:
                output["patients"] = patients
                break_list_into_2000_patients(file_number, output)
                file_number += 1
                output["patients"] = {}
                quick_check = 0
                patients.clear()

    one_file_output["patients"] = one_big_list
    return one_file_output


def break_list_into_2000_patients(list_number, file_json):
    """making files of 2000 records makes the import manageable if something goes wrong"""
    write_2000_patients = Path.cwd() / f"{list_number}_output_json.json"
    convert_to_json_before_writing = json.dumps(file_json, indent=4)
    # validate quickly
    if validate_json(convert_to_json_before_writing):
        write_2000_patients.write_text(convert_to_json_before_writing)


def validate_json(jsonData):
    """validate json before saving it to the file"""
    try:
        json.loads(jsonData)
    except ValueError as err:
        print("BIG JSON ISSUE", err)
        return False
    return True


if __name__ == '__main__':
    zipcodes = get_approved_zipcodes()
    prep_file_to_upload = convert_csv_to_json(zipcodes)
    convert_to_json = json.dumps(prep_file_to_upload, indent=4)
    if validate_json(convert_to_json):
        patient_json_file = Path.cwd() / "single_file_patients_json.json"
        patient_json_file.write_text(convert_to_json)
