from chat_interaction.ask_chat_gpt import ask_chat_gpt
import re

def prelucrate_wages(wages_response):
    # Extracting the average salary
    salary_match = re.search(r'\$(\d+,\d+)', wages_response)
    average_salary = salary_match.group(1) if salary_match else None
    return average_salary

def prelucrate_common_jobs(common_jobs_response):
    # Extracting the most common jobs
    jobs_text = common_jobs_response
    most_popular_jobs = [job.strip() for job in jobs_text.split('\n')]
    return most_popular_jobs

def prelucrate_age_range(age_range_response):
    age_range = age_range_response
    return age_range

def get_request_criteria(areas, industry):

    # Make an array of responses to the questions
    area_responses = []


    for area in areas:
        wages_question = f'What is the average salary for {industry} jobs in {area}?'

        common_jobs_question = f'What are the 10 most common jobs in {area} from the list {industry}?'

        age_range_question = f'Can you provide an estimate of the typical age range for jobs in {industry} within {area}?'

        # Create a tuple of the questions
        area_responses.append((ask_chat_gpt(wages_question), ask_chat_gpt(common_jobs_question), ask_chat_gpt(age_range_question)))

    # Prelucrate the responses
    for i in range(len(area_responses)):
        area_responses[i] = (prelucrate_wages(area_responses[i][0]), prelucrate_common_jobs(area_responses[i][1]), prelucrate_age_range(area_responses[i][2]))


    return area_responses

def main():
    areas = ['New York', 'Texas']
    industry = 'software engineering'


    print(get_request_criteria(areas, industry))


if __name__ == "__main__":
    main()