STEPS TO RUN:
1. create virtualenv & install requirements by running:
pip install -r requirements.txt
2. run the flask application in an IDE or call "python app.py"
3. call the API using:

import requests

url = "http://127.0.0.1:5000/"

payload="{\n    \"fileName\": \"census_2009b\",\n    \"columnName\": \"7_2009\"\n}"
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

4. response will be something like:
{
    "followsBenfords": true,
    "saveTo": "graph136.png"
}



DESCRIPTION:
* the application will take in a fileName in the project directory and create a graph showing the 2 distributions
and respond back which file is stored under and also whether the provided file had data to follow Benford's
distribution.