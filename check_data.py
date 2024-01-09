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
    data.iloc[:, 0] = data.iloc[:, 0].str.replace("*", "")

    states = data.iloc[:, 0].values
    gdp = data.iloc[:, 2].values

    # Merge the two arrays into one
    states = np.column_stack((states, gdp))

    return states
def create_chat_criterias(states, industry):
        request = get_request_criteria(states, industry)
        anual_salaries = []
        age_ranges = []
        for i in range(len(request)):
            anual_salaries.append(request[i][0])
            age_ranges.append(request[i][1])

        # Save the chat criteria to a JSON file
        with open("datasets/chat_criterias.json", "w") as f:
            json.dump({"anual_salaries": anual_salaries, "age_range": age_ranges}, f)


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


def check_possible_openings(states, wages, rent, number_of_jobs, minimumLimit, my_revenue):
    possible_states = []  # List to hold states that meet the criteria

    for i in range(len(states)):
        if wages[i] is not None and number_of_jobs is not None:
            if wages[i] * number_of_jobs + rent < minimumLimit * my_revenue:
                # Add states that meet the criteria to the new list
                possible_states.append(states[i])

    return possible_states
        


def create_industry_demand_weights(data_industry, industries, data_common_jobs, data_disproprotionality, data_gdp, chat_10_jobs=None):
    matching = data_industry[data_industry.iloc[:, 0] == industries]
    if matching.empty:
        return None
    matching = matching.iloc[:, 2].values[0]
    matching = matching.replace(",", "")

    # Convert to a number
    matching = float(matching)

    areas = const.states
    areas = areas.split(",")
    weigth_list = []

    for area in areas:
        # Get the number of jobs in the area
        matching_area = data_common_jobs[data_common_jobs.iloc[:, 0] == area]
        if matching_area.empty:
            continue
        
        intustry_common = False
        idx = 0
        for i in range(1, 11):
            if matching_area.iloc[:, i].values[0] == industries:
                intustry_common = True
                idx = i
                break
        
        if chat_10_jobs is not None:
            for chat_job in chat_10_jobs:
                if chat_job == matching_area.iloc[:, idx].values[0]:
                    intustry_common = True
                    break

        # Get the disproportionality score
        matching_disproprotionality = data_disproprotionality[data_disproprotionality.iloc[:, 1] == area.upper()]
        industry_disproprotionality = False

        if matching_disproprotionality.iloc[:, 2].values[0] == industries:
            industry_disproprotionality = True
            weigth = matching_disproprotionality.iloc[:, 4].values[0]
            weigth_list.append([area, weigth])

        if not industry_disproprotionality and not intustry_common:
            weigth = 0.01
            weigth_list.append([area, weigth])
        elif intustry_common:
            matching_area_value = matching_area.iloc[:, idx + 1].values[0]
            matching_area_value = matching_area_value.replace(",", "")
            matching_area_value = float(matching_area_value)
            weigth = matching_area_value / matching * 10
            weigth = round(weigth, 2)
            weigth_list.append([area, weigth])

    # Sort the list and if the value is the same, sort by the gdp
    weigth_list.sort(key=lambda x: x[1], reverse=True)

    for i in range(len(weigth_list)):
        for j in range(i+1,len(weigth_list)):
            if weigth_list[i][1] == weigth_list[j][1]:
                data_i = data_gdp[data_gdp[:, 0] == weigth_list[i][0]]
                data_j = data_gdp[data_gdp[:, 0] == weigth_list[j][0]]
                if data_i[0][1] < data_j[0][1]:
                    weigth_list[i], weigth_list[j] = weigth_list[j], weigth_list[i]

    return weigth_list

def main():
    data_living = get_living_index("datasets/Cost_of_living_index_US.csv")
    data_gdp = get_states_gdp("datasets/states_gdp.csv")
    data_disproprotionality = get_disproprotionality("datasets/disproprotionality.csv")
    data_common_jobs = pd.read_csv("datasets/common_jobs.csv")
    data_industry_demand = pd.read_csv("datasets/industry_demands.csv")

    # request = get_request_criteria(states, const.industries)
    # anual_salaries = []
    # top_10_jobs = []
    # age_range = []
    # for i in range(len(request)):
    #     anual_salaries.append(request[i][0])
    #     top_10_jobs.append(request[i][1])
    #     age_range.append(request[i][2])

    weight = create_industry_demand_weights(data_industry_demand, "Business", data_common_jobs, data_disproprotionality, data_gdp)

    print(weight)


if __name__ == "__main__":
    main()
