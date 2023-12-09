import json
import pandas as pd
import numpy as np
import requests
import urllib.request
import re
from bs4 import BeautifulSoup

def get_living_index(path):
    data = pd.read_csv(path)
    data = data.dropna()

    data = data.to_dict(orient='records')

    # Remove all rows that doesnt have a region United States
    data_us = []
    for row in data:
        if "United States" in row['City']:
            data_us.append(row)
    
    # Multiply the Rent index by the average rent in New York
    for row in data_us:
        row['Rent Index'] = row['Rent Index'] * 4000
    
    return data_us

def scrape_states_gdp(url):

    data = pd.read_html(requests.get(url).content)[0].to_csv()
    
    # Fortmat the data with only printables characters
    data = ''.join([i for i in data if i.isprintable()])

    # Write the data to a csv file and add a \n after 10 commas
    with open('datasets/states_gdp.csv', 'w') as f:
        f.write(data)
    return data

def scrape_disproprotionality(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        all_states = soup.find_all('div', class_='slide')

        line = ""

        for state_html in all_states:

            state = state_html.find('h2').text

            state = state.replace(': ',': "')
            state = state.replace(': ',',')
            state = state + '",'

            score = state_html.find('p').text
            
            number_of_jobs = score.split(' ')[1]
            number_of_jobs = re.findall(r'\d+', number_of_jobs)
            number_of_jobs = ''.join(number_of_jobs)

            score_job = score.split(' ')[4]
            score_job = re.findall(r'\d+', score_job)
            score_job = '.'.join(score_job)

            line += state + number_of_jobs + ',' + score_job + '\n'

        # Write the data to a csv file
        with open('datasets/disproprotionality.csv', 'w') as f:
            f.write(line)

def get_states_gdp(path):

    data = pd.read_csv(path)

    states = data.iloc[:, 0].values
    gdp = data.iloc[:, 2].values

    # Merge the two arrays into one
    states = np.column_stack((states, gdp))

    return states


def check_data(data):
    pass

def main():
    
    data_living = get_living_index('datasets/Cost_of_living_index_US.csv')
    data_gdp = get_states_gdp('datasets/states_gdp.csv')

    scrape_disproprotionality('https://www.businessinsider.com/popular-jobs-in-every-state-2018-4')

if __name__ == '__main__':
    main()
    