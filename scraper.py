import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the page to scrape
url = "https://about.gitlab.com/company/"

# Send a GET request to the webpage
response = requests.get(url)
response.raise_for_status()  # Check if the request was successful

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Define a dictionary to store the scraped data
data = {
    "Section": [],
    "Content": []
}

# Function to add data to the dictionary
def add_data(section, content):
    data["Section"].append(section)
    data["Content"].append(content)

# Scrape data from various sections of the page
sections = soup.find_all(['h2', 'h3', 'p', 'li', 'strong', 'span'])
current_section = "General"

for section in sections:
    section_title = section.get_text(strip=True)
    if section.name in ['h2', 'h3']:
        current_section = section_title
    elif section.name in ['p', 'li', 'strong', 'span']:
        add_data(current_section, section_title)

# Handle specific sections such as "GitLab by the numbers" separately
numbers_section = soup.find_all('div', class_='gl-mt-6')
if numbers_section:
    for div in numbers_section:
        heading = div.find('h2', string="GitLab by the numbers")
        if heading:
            stats = div.find_next_sibling('div').find_all('div', recursive=False)
            for stat in stats:
                key = stat.find('p').get_text(strip=True)
                value = stat.find('span').get_text(strip=True)
                add_data("GitLab by the numbers", f"{key}: {value}")

# Create a DataFrame from the dictionary
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
output_file = "gitlab_about_page.xlsx"
df.to_excel(output_file, index=False)

print(f"Data has been successfully scraped and saved to {output_file}")
