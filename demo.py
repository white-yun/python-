import requests
from bs4 import BeautifulSoup
import time

# Define the main URL
main_url = "https://shenzhen.anjuke.com/ask/?from=esf_list"

# Send a GET request to the main URL
response = requests.get(main_url)
response.encoding = 'utf-8'

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all question links
    question_links = soup.find_all('a', attrs={"_soj": "wd_rmwd_ask"})
    question_urls = [link['href'] + "?wd_rmwd_ask" for link in question_links if link.has_attr('href')]
    print(question_urls)
    # Create a list to store the data
    data = []

    # Iterate through each question URL
    for question_url in question_urls:
        # Visit each question page
        question_response = requests.get(question_url)
        question_response.encoding = 'utf-8'

        if question_response.status_code == 200:
            question_soup = BeautifulSoup(question_response.text, 'html.parser')

            # Extract the question
            question_text = question_soup.find('div', class_='question no-content-question').get_text(strip=True)

            # Extract all answers
            answer_items = question_soup.find_all('p', class_='answer-doc no-select')
            print(answer_items)
            answers = [answer.get_text(strip=True) for answer in answer_items]

            # Store the question and its answers in the data list
            data.append({'question': question_text, 'answers': answers})

            # Print the data
            print(f"Question: {question_text}")
            for answer in answers:
                print(f"Answer: {answer}\n")

            # Pause to avoid overwhelming the server
            time.sleep(1)
        else:
            print(f"Failed to retrieve the question page. Status code: {question_response.status_code}")
else:
    print(f"Failed to retrieve the main page. Status code: {response.status_code}")
