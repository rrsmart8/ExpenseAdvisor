import json

from flask import Flask, render_template, request
import os

app = Flask(__name__, template_folder=os.path.abspath('templates'))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form)
        industry = request.form.get('industry', '')
        location = request.form.get('location', '')
        revenue = request.form.get('revenue', '')
        employees = request.form.get('employees', '')

        input = {}
        input['industry'] = industry
        input['location'] = location
        input['revenue'] = revenue
        input['employees'] = employees

        with open('input.json', 'w') as f:
            json.dump(input, f, indent=4)

        return f'Industry: {industry}, Location: {location}'
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)