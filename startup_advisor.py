import requests
import json

from ask_chat_gpt import ask_chat_gpt

# TODO: Getting input from user and storing it to an array
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
    industries = "IT, Real Estate, Apparel, Media & Telecom, Construction, Business, Churches, Temples & Mosque, Entertainment & Hobbies, Community, Food & Beverage, Health & Medical, Home & Garden, Transportation & Shipping, Marketing & Sales, Travel & Tourism, Finance, Education, Agriculture & Farms, Manufacturing & Wholesale, Automotive, Petroleum Refining & Related Activities, Services, Beauty, Electrical & Electronic Stores, Sports, Legal, Retail, Industrial Production, Pets, Fashion Accessories Stores, Others, Textile Production, Boat Services, Funeral Services, Driving School, Wedding & Event Planning Services, Solar Energy Company, Gift & Boutique Shops, Utility Companies, Care Services, Food Production, Food Production & Distribution, Wood & Paper Manufacturing, Oil, Gas & Fuel Companies, General Stores & Hardware Stores"
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
    states_mean = calculate_mean_revenue("temp.json")

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

    states = "Alabama, Alaska, Arizona, Arkansas, California, Colorado, Connecticut, Delaware, Florida, Georgia, Hawaii, Idaho, Illinois, Indiana, Iowa, Kansas, Kentucky, Louisiana, Maine, Maryland, Massachusetts, Michigan, Minnesota, Mississippi, Missouri, Montana, Nebraska, Nevada, New Hampshire, New Jersey, New Mexico, New York, North Carolina, North Dakota, Ohio, Oklahoma, Oregon, Pennsylvania, Rhode Island, South Carolina, South Dakota, Tennessee, Texas, Utah, Vermont, Virginia, Washington, West Virginia, Wisconsin, Wyoming"
    states = states.split(", ")

    check_data(data, states)

    print(states)

if __name__ == "__main__":
    main()