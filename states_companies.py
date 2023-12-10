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

industry = "Business"
region = "California"

# Define the request body as a Python dictionary
request_body = {
    "filters": {
        "and": [
            {
                "attribute": "company_location",
                "relation": "equals",
                "value": {
                    "country": "United States",
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

states = "Alabama, Alaska, Arizona, Arkansas, California, Colorado, Connecticut, Delaware, Florida, Georgia, Hawaii, Idaho, Illinois, Indiana, Iowa, Kansas, Kentucky, Louisiana, Maine, Maryland, Massachusetts, Michigan, Minnesota, Mississippi, Missouri, Montana, Nebraska, Nevada, New Hampshire, New Jersey, New Mexico, New York, North Carolina, North Dakota, Ohio, Oklahoma, Oregon, Pennsylvania, Rhode Island, South Carolina, South Dakota, Tennessee, Texas, Utah, Vermont, Virginia, Washington, West Virginia, Wisconsin, Wyoming"
states = states.split(", ")


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



# count_revenues()


get_state_companies("IT")
# response = requests.post(url, headers=headers, json=request_body, params=params)
# print(response.json()["result"])
# print(len(response.json()['result']))