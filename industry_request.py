import requests
import json
import constants as const

# Get the constants
industry_url = const.url_2
api_key = const.api_key

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
