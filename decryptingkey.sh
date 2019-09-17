#!/usr/bin/env bash
aws s3 cp s3://touchsurgery-gdrive-app-credentials/MerakiApiKey ./key/MerakiApiKey
aws s3 cp s3://touchsurgery-gdrive-app-credentials/TechOps-GSuite-ApiKey ./key/TechOps-GSuite-ApiKey

aws kms decrypt --ciphertext-blob fileb://key/MerakiApiKey --output text --query Plaintext | base64 --decode > ./key/Meraki_apikey.txt 
aws kms decrypt --ciphertext-blob fileb://key/TechOps-GSuite-ApiKey --output text --query Plaintext | base64 --decode > ./key/TechOps-gspread-apikey.json 