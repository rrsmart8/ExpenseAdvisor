import requests
import json
import constants as const
import pandas as pd

from chat_interaction.ask_chat_gpt import ask_chat_gpt
import check_data as check

def get_user_data():
    print("Hello, I am your startup advisor. I will help you to find the best industry for your startup.")

    data = {

        "Company Name": "Samsung",
        "Revenue": 5400000000,
        "Industry": "Business",
        "State": "New York",
        "Number of Employees": 1000,

    }

    return data

# TODO: Check big or small company
def check_company_size(company_name):
    # Define the API endpoint URL
    url = 'https://data.veridion.com/search/v2/companies'

    # Define the API key
    api_key = 'pXStedvXkA9pMcNK1tWvx_4DesmTsIZ47qfTa6WkqFxgrCvCqJA0mpALQ53J'

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
                    "attribute": "company_name",
                    "relation": "equals",
                    "value": company_name,
                }
            ]
        }
    }

    # Make the request
    response = requests.post(url, headers=headers, json=request_body)

    if response.status_code != 200 or response.json()["count"] == 0:
        print("Company not found")
        return False

    print("Company found")
    return True

# TODO: Correct industry from Search API using ChatGPT API
def correct_industry(industry):
    industries = const.industries
    answer = ask_chat_gpt("Find the best match for the industry " + industry + "in the following list: " + industries + ". Give me only one match")

    return answer

# TODO: Parse the United States company list and calculate the mean revenue

def calculate_mean_revenue(file_path):
    # Load the JSON data
    try:
        data = json.load(open(file_path, "r"))
    except json.JSONDecodeError:
        print("Error reading JSON file.")
        return None

    # Extracting revenue values
    states_revenue = []
    for state in data:
        sum = 0
        count = 0
        for company,revenue in data[state].items():
            if revenue is not None:
                sum += revenue
                count += 1
        states_revenue.append([state, sum / count])

    return states_revenue


def check_data(user, areas):

    # Revenue filter
    states_mean = calculate_mean_revenue("datasets/temp.json")

    for i in range(len(states_mean)):
        if states_mean[i][1] > user["Revenue"]:
            areas.remove(states_mean[i][0])

    # Industry demand filter

# TODO: Check the industry demand and sort them
def check_industry_demand(industry):
    data_gdp = check.get_states_gdp("datasets/states_gdp.csv")
    data_disproprotionality = check.get_disproprotionality("datasets/disproprotionality.csv")
    data_common_jobs = pd.read_csv("datasets/common_jobs.csv")
    data_industry_demand = pd.read_csv("datasets/industry_demands.csv")

    weight = check.create_industry_demand_weights(data_industry_demand, industry, data_common_jobs, data_disproprotionality, data_gdp)

    return weight

def main():

    data = get_user_data()
    check_company_size(data["Company Name"])
    industry = correct_industry(data["Industry"])
    data["Industry"] = industry

    states = const.states
    states = states.split(",")

    check_data(data, states)
    weight_array = check_industry_demand(data["Industry"])

    #TODO: Remove from weigth array the states where I cant affor to open with my revenue
    wages_chat = []
    #check.check_possible_openings(wages_array,wages_chat, data["Number of Employees"], 0.4, data["Revenue"])
    


if __name__ == "__main__":
    main()