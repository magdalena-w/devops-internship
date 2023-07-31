#!/usr/bin/env python3

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# SurveyMonkey API credentials
ACCESS_TOKEN = os.getenv('SM_ACCESS_TOKEN')
BASE_URL = 'https://api.surveymonkey.com/v3/'

def create_survey(survey_title, pages):
    # Create a new survey
    survey_data = {
        'title': survey_title
    }
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    survey_response = requests.post(BASE_URL + 'surveys', headers=headers, json=survey_data)
    if survey_response.status_code != 201:
        print(f"Failed to create survey. Error: {survey_response.text}")
        return None

    survey_id = survey_response.json()['id']

    # Add pages and questions to the survey
    for page_title, questions in pages.items():
        page_data = {
            'title': page_title,
            'position': len(pages)  # Set the position of the page
        }
        page_response = requests.post(BASE_URL + f'surveys/{survey_id}/pages', headers=headers, json=page_data)
        if page_response.status_code != 201:
            print(f"Failed to create page. Error: {page_response.text}")
            return None

        page_id = page_response.json()['id']

        for question_id, question_info in questions.items():
            question_data = {
                'headings': [{'heading': question_info['Description']}],
                'family': 'single_choice',  # You can change this to 'multiple_choice' for multiple-choice questions
                'subtype': 'vertical',      # You can change this to 'horizontal' for horizontal layout
                'answers': {"choices": [{'text': answer} for answer in question_info['Answers']]},
                'position': len(questions)  # Set the position of the question on the page
            }
            question_response = requests.post(BASE_URL + f'surveys/{survey_id}/pages/{page_id}/questions', headers=headers, json=question_data)
            if question_response.status_code != 201:
                print(f"Failed to create question. Error: {question_response.text}")
                return None

    return survey_id

def create_collector(survey_id):
    collector_data = {
        'type': 'email',
        'name': 'Email Collector',  # You can change the name of the collector as needed
        'thank_you_message': 'Thank you for taking the survey!',
        'close_date': None  # You can set a close date for the collector if desired
    }
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    response = requests.post(BASE_URL + f'surveys/{survey_id}/collectors', headers=headers, json=collector_data)
    if response.status_code != 201:
        print(f"Failed to create collector. Error: {response.text}")
        return None

    collector_id = response.json()['id']
    return collector_id

def send_email_invitations(collector_id, email_list):
    for email in email_list:
        invitation_data = {
            'recipients': {
                'type': 'email',
                'email': email,
            }
        }
        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        response = requests.post(BASE_URL + f'collectors/{collector_id}/messages', headers=headers, json=invitation_data)
        if response.status_code != 201:
            print(f"Failed to send email invitation to {email}. Error: {response.text}")

def main():
    with open('survey_questions.json') as file:
        survey_data = json.load(file)

    survey_title = list(survey_data.keys())[0]
    pages = survey_data[survey_title]

    survey_id = create_survey(survey_title, pages)
    if survey_id:
        print(f"Survey '{survey_title}' with ID {survey_id} created successfully!")

        with open('email_addresses.txt', 'r') as email_file:
            email_list = email_file.read().splitlines()

        collector_id = create_collector(survey_id)
        if collector_id:
            send_email_invitations(collector_id, email_list)
            print(f"Email invitations sent to {len(email_list)} recipients!")

if __name__ == "__main__":
    main()

