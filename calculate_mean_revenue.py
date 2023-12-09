import json

def calculate_mean_revenue(file_path):
    # Load the JSON data
    with open(file_path, "r") as f:
        data = json.load(f)

    # Extracting revenue values
    print(data)
    # revenues = []
    # for state in data:
    #     for company, revenue in data[state].items():
    #         if revenue is not None:
    #             revenues.append(revenue)
    #
    # # Calculate the mean revenue
    # if revenues:
    #     mean_revenue = sum(revenues) / len(revenues)
    #     return mean_revenue
    # else:
    #     return None
