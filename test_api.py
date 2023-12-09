import requests
import json

# Define the API endpoint URL
url = 'https://data.veridion.com/search/v2/companies'

# Define the API key
api_key = 'pXStedvXkA9pMcNK1tWvx_4DesmTsIZ47qfTa6WkqFxgrCvCqJA0mpALQ53J'

# Define the request headers
headers = {
    'x-api-key': api_key,
    'Content-Type': 'application/json',
}

# Define the request body as a Python dictionary
request_body = {
    "filters": {
        "and": [
            {
                "attribute": "company_location",
                "relation": "in",
                "value": [
                    {
                        "country": "US"
                    }
                ],
                "strictness": 1
            },
            {
                "attribute": "company_products",
                "relation": "match_expression",
                "value": {
                    "match": {
                        "operator": "OR",
                        "operands": [
                            "biopharma",
                            "biopharmaceutical",
                            "biopharmaceuticals"
                        ]
                    }
                },
                "strictness": 2,
                "supplier_types": [
                    "manufacturer",
                    "distributor"
                ]
            }
        ]
    }
}

# Make the request

response = requests.post(url, headers=headers, json=request_body)

# Print the response status content

print(json.loads(response.text))

