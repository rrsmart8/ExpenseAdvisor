import json

largest_occupation_in_each_state = {
    "STATE": []
}

while True:
    state_name = input("Enter state name (or 'done' to finish): ").strip()
    if state_name.lower() == 'done':
        break

    jobs = input("Enter jobs for {}: ".format(state_name)).strip()
    employees = input("Enter employees for {}: ".format(state_name)).strip()

    state_data = {
        state_name: [
            {
                "JOBS": jobs,
                "EMPLOYEES": employees
            }
        ]
    }

    largest_occupation_in_each_state["STATE"].append(state_data)

# Convert the Python dictionary to JSON
json_data = json.dumps(largest_occupation_in_each_state, indent=4)

# Save the JSON data to a file
with open('data.json', 'w') as json_file:
    json_file.write(json_data)

print("JSON data saved to 'data.json'.")
