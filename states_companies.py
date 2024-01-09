import requests
import json
import constants as const
from industry_request import get_industries

# Get the constants
url = const.url_1
api_key = const.api_key
states = const.states
states = states.split(",")

# Test data
country = "United States"
industry = "Business"
region = "California"


# Define the request headers
headers = {
    'x-api-key': api_key,
    'Content-Type': 'application/json'
}

# Define the request body as a Python dictionary
request_body = {
    "filters": {
        "and": [
            {
                "attribute": "company_location",
                "relation": "equals",
                "value": {
                    "country": country,
                    "region": region
                },
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

def get_state_companies(industry):
    companies = {}

    with open("temp.json", "r") as f:
        try:
            companies = json.load(f)
        except json.decoder.JSONDecodeError:
            companies = {}

    with open("state_companies.json", "w") as f:
        json.dump(companies, f, indent=4)

    with open("state_companies.json", "r") as f:
        try:
            companies = json.load(f)
        except json.decoder.JSONDecodeError:
            companies = {}

        request_body["filters"]["and"][1]["value"] = industry

        for state in states:
            request_body["filters"]["and"][0]["value"]["region"] = state
            company_counter = 0

            if state in companies.keys() and companies[state] != {}:
                continue

            companies[state] = {}

            company_list = {}

            # Update params
            params["pagination_token"] = None

            print("Listing companies for state: " + state)

            # Make the request
            response = requests.post(url, headers=headers, json=request_body, params=params)
            print(len(response.json()['result']))
            # Print the response status content
            # text = json.dumps(response.json(), sort_keys=True, indent=4)
            # print(response.text)

            # Add to list
            if "next" in response.json()["pagination"].keys():
                while response.json()["pagination"]["next"] is not None and company_counter < 600:

                    request_results = response.json()['result']
                    print(len(request_results))
                    company_counter += len(request_results)

                    for company in request_results:
                        if 'estimated_revenue' in company.keys() and company['estimated_revenue'] is not None:
                            company_list[company['company_name']] = company['estimated_revenue']

                    next_page = response.json()["pagination"]["next"]
                    params["pagination_token"] = next_page

                    response = requests.post(url, headers=headers, json=request_body, params=params)

                companies[state] = company_list

                with open("temp.json", "w") as res:
                    json.dump(companies, res, indent=4, sort_keys=True)

def count_revenues():
    with open("state_companies.json", "r") as f:
        companies = json.load(f)
        good = []
        for state in companies.keys():
            total = len(companies[state])
            res = list(filter(lambda x: companies[state][x] is not None, companies[state]))
            # print(state, total, len(res) / total)
            if len(res) / total > 0.5:
                good.append(state)
        print(len(states))
        print(len(good))