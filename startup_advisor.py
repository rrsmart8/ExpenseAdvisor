import requests
import json
import constants as const

from chat_interaction.ask_chat_gpt import ask_chat_gpt

def get_user_data():
    print("Hello, I am your startup advisor. I will help you to find the best industry for your startup.")

    data = {

        "Company Name": "Samsung",
        "Revenue": 5400000000,
        "Industry": "Electronics",
        "State": "New York",

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

    print(answer)
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
    # Get the data from temp.json
    states_mean = calculate_mean_revenue("datasets/temp.json")

    for i in range(len(states_mean)):
        if states_mean[i][1] > user["Revenue"]:
            areas.remove(states_mean[i][0])

# TODO: Check the industry demand and sort them





# TODO: Check employee


def main():

    data = get_user_data()
    print(data["Company Name"])
    check_company_size(data["Company Name"])
    industry = correct_industry(data["Industry"])
    data["Industry"] = industry

    states = const.states
    states = states.split(",")

    check_data(data, states)


if __name__ == "__main__":
    main()