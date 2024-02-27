# Expansion Advisor

## Description

The Expansion Advisor is a tool to help, relatively big, companies to find new areas to expand to in United States. Using the Expansion Advisor, companies can find new states and cities to expand to based on their current locations and the locations of their competitors. It uses the [Veridion Data](https://veridion.com/) API, Chat-GPT API and multiple others datasets to find the best locations for the company to expand to.

## Table of Contents

- [Description](#description)
- [Table of Contents](#table-of-contents)
- [Installation and Usage](#installation-and-usage)
- [Implementation](#implementation)
- [Story](#story)

## Installation and Usage

To install the Expansion Advisor, you need to clone this repository and install the dependencies using `pip install -r requirements.txt`. Then, you can run the `expansion_advisor.py` file to start the program. The program will prompt you with a series of questions. Once you answer all the questions, the program will return the best locations for the company to expand to.

> [Note: If the program doesn't work, you might need to change the API keys and urls present in the `constants.py` file.]

## Implementation

![Expansion Advisor](readme_imgs/diagram.png)

* In the first three steps, the programs filters the data from the Veridion Data API to get the locations of the company and its competitors. As Veridion Data API has a strict structure for the categories, the program uses the Chat-GPT API to recognize the category from your input. Then, it uses the recognized category to filter the data from the Veridion Data API.

* Using multiple datasets from trust-worthy and official government websites, the program calculates the weighted score for each state and city. The involvement of Chat-GPT in this process is to offer another layer of filtering by offering the 10 most common jobs in the state and the average wage beside the preexisting data. The weighted score is created by:
    * check_possible_openings(states, wages, rent, number_of_jobs, minimumLimit, my_revenue):
        ```
        This function checks if there are possible job openings in each state based on given criteria. It calculates the total cost (wages * number_of_jobs + rent) and compares it against a threshold (minimumLimit * my_revenue) to determine if the state meets the criteria for potential job openings.
        ```
         
    * create_industry_demand_weights(data_industry, selected_industry, data_common_jobs, data_disproportionality, data_gdp, chat_10_jobs=None):
        ```
        This function computes weights for each state based on industry demand. It considers factors like the number of jobs in the selected industry, disproportionality scores, and GDP to assign weights to each state.
        ```
    * calculate_mean_revenue(file_path):
        ```
        This function calculates the mean revenue for each state based on data provided in a JSON file. It computes the average revenue across different companies within each state.
        ```
* The final weighted score is filtered by checking the industry disproportionality in each state and how common is the industry in the state. Lastly, the list returned is sorted by the weighted score and if in any case the weighted score is the same, the list is sorted by the gdp of the state.

* In the output process, Chat-GPT offers multiple insights about the state, like the average wage, the average age, the most common jobs, and the average rent. This is done to offer a better understanding of the state and to help the company make a better decision.


> [Note: Momentarily, the Expansion Advisor only working regions in the United States.]

## Story

The Expansion Advisor was created as a part of the [HackITall](https://hack.lsacbucuresti.ro/) hackathon in Bucharest, Romania. The project was created in 24 hours.

The team is formed of 3 members: [Alexandru](https://github.com/alexandrutrifu), [Rares](https://github.com/rrsmart8) and [me](https://github.com/robertpaulp).