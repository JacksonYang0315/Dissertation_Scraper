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

# Initialize the current section
current_section = "General"

# Scrape data from various sections of the page
sections = soup.find_all(['h2', 'h3', 'p', 'li'])
for section in sections:
    section_title = section.get_text(strip=True)
    if section.name in ['h2', 'h3']:
        current_section = section_title
    else:
        data["Section"].append(current_section)
        data["Content"].append(section_title)

# Create a DataFrame from the dictionary
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
output_file = "gitlab_about_page.xlsx"
df.to_excel(output_file, index=False)

print(f"Data has been successfully scraped and saved to {output_file}")