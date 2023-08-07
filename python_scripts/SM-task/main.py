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
    """
    Create a new survey on SurveyMonkey.
    Args:
        survey_title (str): The title of the survey
        pages (dict): A dictionary containing page titles as keys and questions as values.
    Returns:
        str: The ID of the created survey if successfull, None otherwise.
    """

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
    """
    Create a new collector for the survey.
    Args:
        survey_id (str): The ID of the survey.
    Returns:
        str: The ID of the created collector if successfull, None otherwise.
    """

    collector_data = {
        'type': 'email',
        'name': 'Email Collector',  # You can change the name of the collector as needed
        'thank_you_message': 'Thank you for taking the survey!'
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

def create_email(survey_id, collector_id):
    """
    Create an email message for the survey collector.
    Args:
        survey_id (str): The ID of the survey.
        collector_id (str): The ID of the collector.
    Returns:
        str: The ID of the created email message if successfull, None otherwise.
    """

    invitation_data = {
        'type': 'invite',
        'subject': 'Share your opinion about capybaras with me',
    }

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    response = requests.post(BASE_URL + f'surveys/{survey_id}/collectors/{collector_id}/messages', headers=headers, json=invitation_data)
    if response.status_code != 201:
        print(f"Failed to create email. Error: {response.text}")
        return None

    message_id = response.json()['id']
    return message_id

def add_recipients(survey_id, collector_id, message_id, email_list):
    """
    Add recipients to the survey email message.
    Args:
        survey_id (str): The ID of the survey.
        collector_id (str): The ID of the collector.
        message_id (str): The ID of the email message.
        email_list (list): A list of email addresses of recipients.
    Returns:
        dict: The recipient data if successfull, None otherwise.
    """

    recipients_data = {
        'contacts': [{'email': email} for email in email_list]
    }
    
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    response = requests.post(BASE_URL + f'surveys/{survey_id}/collectors/{collector_id}/messages/{message_id}/recipients/bulk', headers=headers, json=recipients_data)
    if response.status_code != 200:
        print(f"Failed to add recipients. Error {response.text}")
        return None

    return recipients_data

def send_email(survey_id, collector_id, message_id):
    """
    Send the survey email message to recipients.
    Args:
        survey_id (str): The ID of the survey.
        collector_id (str): The ID of the collector.
        message_id (str): The ID of the email message.
    """

    send_data = {}

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    response = requests.post(BASE_URL + f'surveys/{survey_id}/collectors/{collector_id}/messages/{message_id}/send', headers=headers, json=send_data)
    if response.status_code != 200:
        print(f"Failed to send email. Error {response.text}")
        return None

def main():
    """
    Main function to create and send a survey.
    """

    with open('survey_questions.json') as file:
        survey_data = json.load(file)
    survey_title = list(survey_data.keys())[0]
    pages = survey_data[survey_title]

    survey_id = create_survey(survey_title, pages)
    if survey_id:
        print(f"Survey '{survey_title}' with ID {survey_id} created successfully!")
        collector_id = create_collector(survey_id)
        if collector_id:
            message_id = create_email(survey_id, collector_id)
        
        with open('email_addresses.txt', 'r') as email_file:
            email_list = email_file.read().splitlines()
            add_recipients(survey_id, collector_id, message_id, email_list)
            send_email(survey_id, collector_id, message_id)

if __name__ == "__main__":
    main()

