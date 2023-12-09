import requests
import json
from industry_request import get_industries


input_dict = {
    "company_country": "United States",
    "main_industry": "Software",
}

# Define the API endpoint URL
url = 'https://data.veridion.com/search/v2/companies'

# Define the API key
api_key = 'pXStedvXkA9pMcNK1tWvx_4DesmTsIZ47qfTa6WkqFxgrCvCqJA0mpALQ53J'

# Define the request headers
headers = {
    'x-api-key': api_key,
    'Content-Type': 'application/json'
}

industry = None

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
                    },
                    {
                        "country": "United States"
                    }
                ],
                "strictness": 3
            },
            {
                "attribute": "company_industry",
                "relation": "equals",
                "value": industry,
            }
        ]
    }
}

next_page = None

params = {
    "page_size": 200,
    "pagination_token": next_page
}


def get_companies():
    companies = {}
    industries = get_industries()

    with open("companies.json", "r") as f:
        if f.read() != "":
            companies = json.load(f)
        else:
            companies = {}

        for found_industry in industries:
            request_body["filters"]["and"][1]["value"] = found_industry
            company_counter = 0

            if found_industry in companies.keys() and companies[found_industry] != {}:
                continue

            companies[found_industry] = {}

            company_list = {}

            # Update params
            params["pagination_token"] = None

            print("Listing companies for industry: " + found_industry)

            # Make the request
            response = requests.post(url, headers=headers, json=request_body, params=params)

            # Print the response status content
            # text = json.dumps(response.json(), sort_keys=True, indent=4)
            # print(response.text)

            # Add to list
            while response.json()["pagination"]["next"] is not None and company_counter < 600:

                request_results = response.json()['result']
                print(len(request_results))
                company_counter += len(request_results)

                for company in request_results:
                    if 'estimated_revenue' in company.keys():
                        company_list[company['company_name']] = company['estimated_revenue']
                    else:
                        company_list[company['company_name']] = None

                next_page = response.json()["pagination"]["next"]
                params["pagination_token"] = next_page

                response = requests.post(url, headers=headers, json=request_body, params=params)

            companies[found_industry] = company_list

            with open("companies_res.json", "w") as res:
                json.dump(companies, res, indent=4)


get_companies()

