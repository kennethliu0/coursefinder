import json
import os
import re
from bs4 import BeautifulSoup

def normalize_whitespace(text):
    """Normalize whitespace: collapse multiple spaces/newlines into single spaces."""
    if text is None:
        return None
    # Replace newlines and multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def parse_courses(html):
    soup = BeautifulSoup(html, 'html.parser')
    extracted_data = []

    # Iterate through every container div with class 'courseInfo'
    for container in soup.find_all('div', class_='courseInfo'):
        course_data = {}

        # 1. Extract Course Number
        number_tag = container.find('span', class_='courseNumber')
        course_data['course_number'] = number_tag.get_text(strip=True).replace(':', '') if number_tag else None

        # 2. Extract Description
        # Logic: Find the div, then check if 'noDisplay' is NOT in its class list
        desc_tag = container.find('div', class_='courseDescription')

        description_text = None
        if desc_tag:
            classes = desc_tag.get('class', [])
            if 'noDisplay' not in classes:
                description_text = normalize_whitespace(desc_tag.get_text())

        course_data['course_description'] = description_text

        extracted_data.append(course_data)

    return extracted_data

if __name__ == "__main__":
    # Configuration: Change this to your actual file path
    INPUT_FILENAME = 'courses.html'
    OUTPUT_FILENAME = 'courses.json'

    # Check if file exists before trying to open
    if not os.path.exists(INPUT_FILENAME):
        print(f"Error: The file '{INPUT_FILENAME}' was not found in this directory.")
    else:
        try:
            # Open and read the HTML file
            with open(INPUT_FILENAME, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            print(f"Successfully read {len(html_content)} bytes from {INPUT_FILENAME}...")

            # Parse the data
            data = parse_courses(html_content)
            
            # Write to JSON file
            with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
                
            print(f"Success! Parsed {len(data)} courses. Output saved to '{OUTPUT_FILENAME}'.")
            
        except Exception as e:
            print(f"An error occurred: {e}")