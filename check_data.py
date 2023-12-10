import json
import pandas as pd
import numpy as np
import requests
import urllib.request
import re
from bs4 import BeautifulSoup
from chat_interaction.get_request_criteria import get_request_criteria
from chat_interaction.ask_chat_gpt import ask_chat_gpt
import constants as const

# states = "Alabama, Alaska, Arizona, Arkansas, California, Colorado, Connecticut, Delaware, Florida, Georgia, Hawaii, Idaho, Illinois, Indiana, Iowa, Kansas, Kentucky, Louisiana, Maine, Maryland, Massachusetts, Michigan, Minnesota, Mississippi, Missouri, Montana, Nebraska, Nevada, New Hampshire, New Jersey, New Mexico, New York, North Carolina, North Dakota, Ohio, Oklahoma, Oregon, Pennsylvania, Rhode Island, South Carolina, South Dakota, Tennessee, Texas, Utah, Vermont, Virginia, Washington, West Virginia, Wisconsin, Wyoming"
states = "New York, Texas"
states = states.split(", ")

industries = "IT, Real Estate, Apparel, Media & Telecom, Construction, Business, Churches, Temples & Mosque, Entertainment & Hobbies, Community, Food & Beverage, Health & Medical, Home & Garden, Transportation & Shipping, Marketing & Sales, Travel & Tourism, Finance, Education, Agriculture & Farms, Manufacturing & Wholesale, Automotive, Petroleum Refining & Related Activities, Services, Beauty, Electrical & Electronic Stores, Sports, Legal, Retail, Industrial Production, Pets, Fashion Accessories Stores, Others, Textile Production, Boat Services, Funeral Services, Driving School, Wedding & Event Planning Services, Solar Energy Company, Gift & Boutique Shops, Utility Companies, Care Services, Food Production, Food Production & Distribution, Wood & Paper Manufacturing, Oil, Gas & Fuel Companies, General Stores & Hardware Stores"
industries = industries.split(", ")

def scrape_states_gdp(url):
    data = pd.read_html(requests.get(url).content)[0].to_csv()

    # Fortmat the data with only printables characters
    data = "".join([i for i in data if i.isprintable()])

    # Write the data to a csv file and add a \n after 10 commas
    with open("datasets/states_gdp.csv", "w") as f:
        f.write(data)
    return data

def prepare_industry_demand(path):
    with open(path, "r") as f:
        data = f.readlines()

    data = [x.strip() for x in data]

    # Remove all the empty lines
    data = list(filter(None, data))

    list_of_jobs = []
    state_jobs = []
    for i in range(len(data)):
        if "Largest Occupations" in data[i]:
            state = data[i].split(" ")[3] + " " + data[i].split(" ")[4]
            state = state.split(",")[0]
            print(state)
            if state_jobs:
                state_jobs.pop(1)
                list_of_jobs.append(state_jobs)
                state_jobs = []
        
        if "Largest Occupations" in data[i]:
            state_jobs.append(state)
        else:
            state_jobs.append("\"" + data[i] + "\"")

    # Append the last set of state_jobs after the loop
    if state_jobs:
        list_of_jobs.append(state_jobs)

    # write the data to a csv file
    with open("datasets/industry_demands.csv", "w") as f:
        for state_jobs in list_of_jobs:
            for job in state_jobs:
                f.write(job + ",")
            f.write("\n")

def scrape_disproprotionality(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        all_states = soup.find_all("div", class_="slide")

        line = ""

        for state_html in all_states:
            state = state_html.find("h2").text

            state = state.replace(": ", ': "')
            state = state.replace(": ", ",")
            state = state + '",'

            score = state_html.find("p").text

            number_of_jobs = score.split(" ")[1]
            number_of_jobs = re.findall(r"\d+", number_of_jobs)
            number_of_jobs = "".join(number_of_jobs)

            score_job = score.split(" ")[4]
            score_job = re.findall(r"\d+", score_job)
            score_job = ".".join(score_job)

            line += state + number_of_jobs + "," + score_job + "\n"

        # Write the data to a csv file
        with open("datasets/disproprotionality.csv", "w") as f:
            f.write(line)



def prepare_common_jobs_data(path):
    with open(path, "r") as f:
        data = f.readlines()

    data = [x.strip() for x in data]

    # Remove all the empty lines
    data = list(filter(None, data))

    list_of_jobs = []
    state_jobs = []
    for i in range(len(data)):
        if "Largest occupations" in data[i]:
            state = data[i].split(" ")[3] + " " + data[i].split(" ")[4]
            state = state.split(",")[0]

            if state_jobs:
                state_jobs.pop(1)
                list_of_jobs.append(state_jobs)
                state_jobs = []
        
        if "Largest occupations" in data[i]:
            state_jobs.append(state)
        else:
            state_jobs.append("\"" + data[i] + "\"")

    # Append the last set of state_jobs after the loop
    if state_jobs:
        list_of_jobs.append(state_jobs)

    # write the data to a csv file
    with open("datasets/common_jobs.csv", "w") as f:
        for state_jobs in list_of_jobs:
            for job in state_jobs:
                f.write(job + ",")
            f.write("\n")


def get_states_gdp(path):
    data = pd.read_csv(path)

    states = data.iloc[:, 0].values
    gdp = data.iloc[:, 2].values

    # Merge the two arrays into one
    states = np.column_stack((states, gdp))

    return states


def get_living_index(path):
    data = pd.read_csv(path)
    data = data.dropna()

    data = data.to_dict(orient="records")

    # Remove all rows that doesnt have a region United States
    data_us = []
    for row in data:
        if "United States" in row["City"]:
            data_us.append(row)

    # Multiply the Rent index by the average rent in New York
    for row in data_us:
        row["Rent Index"] = row["Rent Index"] * 4000

    return data

def get_disproprotionality(path):
    data = pd.read_csv(path)
    return data



def main():
    data_living = get_living_index("datasets/Cost_of_living_index_US.csv")
    data_gdp = get_states_gdp("datasets/states_gdp.csv")
    data_disproprotionality = get_disproprotionality("datasets/disproprotionality.csv")
    data_common_jobs = pd.read_csv("datasets/common_jobs.csv")
    data_industry_demand = pd.read_csv("datasets/industry_demands.csv")

    print(data_industry_demand)

    # request = get_request_criteria(states, const.industries)
    # anual_salaries = []
    # top_10_jobs = []
    # age_range = []
    # for i in range(len(request)):
    #     anual_salaries.append(request[i][0])
    #     top_10_jobs.append(request[i][1])
    #     age_range.append(request[i][2])

if __name__ == "__main__":
    main()
