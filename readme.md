## Family Tree Generator From Voter Details in India

This is a simple real-time API to fetch family details of a person using a few fields like name, dob, fathersName, state, gender.

This currently supports only Karnataka and will be expanded soon.

> Do note that this is a real-time API so the response will be super slow (Up to 30 seconds). 

> If you are thinking of using this for production, A better way is to Schedule a Job every 6 months and store all the voter's Details in your Local DB and query it in milli seconds( If it's legal)

## Tech used
- Google Cloud Vision API
- Google Cloud Document AI

## Steps to run this locally

- Signup for a Google Cloud Account
- Enable Document AI and Cloud Vision API in your GCP Account
- Download the Project Keys and store it in the base directory as ```keys.json```
- Run ```pip install requirements.txt```
- Run ```flask run```