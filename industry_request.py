import requests
import json

industry_url = "https://data.veridion.com/industries/v0"

# Define the API key
api_key = 'pXStedvXkA9pMcNK1tWvx_4DesmTsIZ47qfTa6WkqFxgrCvCqJA0mpALQ53J'

# Define the request headers
headers = {
    'x-api-key': api_key,
    'Content-Type': 'application/json'
}

industry_request_body = {
    "filters": {
        "and": [
            {
                "attribute": "industry_name",
                "relation": "equals",
                "value": "IT",
            }
        ]
    }
}


def get_industries():
    industry_response = requests.get(industry_url, headers=headers)
    industries = []

    for industry in industry_response.json():
        industries.append(industry['name'])

    return industries
