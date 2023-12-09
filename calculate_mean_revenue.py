import json

def calculate_mean_revenue(file_path):
    # Load the JSON data
    try:
        data = json.load(open(file_path, "r"))
    except json.JSONDecodeError:
        print("Error reading JSON file.")
        return None

    # Extracting revenue values
    revenues = []
    for state in data:
        for company, revenue in data[state].items():
            if revenue is not None:
                revenues.append(revenue)

    # Calculate the mean revenue
    if revenues:
        mean_revenue = sum(revenues) / len(revenues)
        return mean_revenue
    else:
        return None
