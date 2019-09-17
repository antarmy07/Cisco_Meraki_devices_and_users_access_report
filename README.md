# Meraki Devices and Users Report


This python script was made to create Google spreadsheet report of the devices and users that are connected to Meraki System Manager (MDM network).

This python script work well on Pyhton 3 and requires following:

- gspread
- sys, os
- requests
- json
- time
- datetime
- oauth2client
- boto3
- botocore
- gspread_formatting
- awscli

Please use pip install to install these modules before running the script.

**NOTE** 

This python runs bash script that download pre-encrypted S3 bucket files using awscli kms key and decrypts files using aws [default] profile that has the kms key to decrypt the files.




