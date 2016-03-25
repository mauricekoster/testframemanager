#!/bin/env python3

import json
import gspread
from oauth2client.client import GoogleCredentials

# json_key = json.load(open('~/Downloads/client_secret_845885166827-uftdiljedsskcvumrpq7fp8lt4iciu7a.apps.googleusercontent.com.json'))
scope = ['https://spreadsheets.google.com/feeds']

credentials = GoogleCredentials.get_application_default()

# credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)

gc = gspread.authorize(credentials)