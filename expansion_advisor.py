import requests
import json
import constants as const
import pandas as pd

from chat_interaction.ask_chat_gpt import ask_chat_gpt
import check_data as check

# Getting the constants
URL = const.url_1
API_KEY = const.api_key

## Region: User data && data validation
def get_user_data():
    print("Hello, I am your expansion advisor. I will help you to find the best industry for your business.")

    # Read the user data
    Company_Name = input("What is the name of your company? ")
    Revenue = input("What is your revenue? ")
    Industry = input("What is your industry? ")
    State = input("What is your state? ")
    Number_of_Employees = input("How many employees do you want to have at the new location? ")

    # Create a dictionary with the user data
    data = {
            "Company Name": Company_Name,
            "Revenue": int(Revenue),
            "Industry": Industry,
            "State": State,
            "Number of Employees": int(Number_of_Employees),

        }

    # Test data
    # data = {
    #
    #     "Company Name": "McDonald's",
    #     "Revenue": 550000000,
    #     "Industry": "Food & Beverage",
    #     "State": "New York",
    #     "Number of Employees": 1000,
    #
    # }
    return data

def check_company_in_database(company_name):
    # Define the request URL and API key
    url = URL
    api_key = API_KEY

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
        print("Company not found in the database")
        return False

    print("Company found in the database")
    return True

# Replace the given industry with the best match from the Veridion industry list
def correct_industry(industry):
    industries = const.industries
    answer = ask_chat_gpt("Find the best match for the industry " + industry + "in the following list: " + industries + ". Give me only one match")

    return answer

## End region

def main():

    data = get_user_data()
    if check_company_in_database(data["Company Name"]) == False:
        return
    industry = correct_industry(data["Industry"])
    data["Industry"] = industry

    states = const.states
    states = states.split(",")

    check.remove_higher_revenue_states(data, states)
    weight_array = check.check_industry_demand(data["Industry"])

    try:
        chat_criterias = json.load(open("datasets/chat_criterias.json", "r"))
    except json.JSONDecodeError:
        print("Error reading JSON file.")
        return None

    # Extracting the anual wages
    wages_chat = []
    for i in range(len(chat_criterias["anual_salaries"])):
        wages_chat.append(chat_criterias["anual_salaries"][i].replace(",", ""))

    wages_chat = [int(i) for i in wages_chat]
    num_of_employees = data["Number of Employees"]
    meet_criteria_states = check.check_possible_openings(weight_array,wages_chat, 3000,num_of_employees, 0.5, data["Revenue"])

    if meet_criteria_states == []:
        print("You don't have sufficient revenue to open a new location in the United States.")
        return
    
    print("The best states for your business are: " + str(meet_criteria_states))

    # Get the industry index from the industries list
    industry_index = -1
    ind_array = const.industries.split(", ")

    for i in range(len(ind_array)):
        if ind_array[i] == industry:
            industry_index = i
            break

    if industry_index == -1:
        print("Industry not found")
        return

    # Get the age range from the chat_criterias.json file
    age_range = chat_criterias["age_range"][industry_index]

    print("----------------------------------------------------------------------------------------\n")

    saturated_nieches = []
    best_choice = ""

    for i in range(len(meet_criteria_states)):
        if meet_criteria_states[i][1] > 2:
            saturated_nieches.append(meet_criteria_states[i][0])
        else:
            best_choice = meet_criteria_states[i][0]
            break

    if saturated_nieches == []:
        print("There are no saturated nieches")
    else:
        print("The saturated nieches are: \n" + str(saturated_nieches))
    print()

    print("Best choice:")
    print(" -> Open new location " + data["Company Name"] + " in " + best_choice + ".")
    print(" -> In the industry " + industry +  " and the age range is " + age_range + ".")
    print("\nThank you for using our service. We hope you will have a scalable business.")

if __name__ == "__main__":
    main()