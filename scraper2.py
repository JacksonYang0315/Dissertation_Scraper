import requests
from bs4 import BeautifulSoup
import pandas as pd

# List of company websites
companies = [
    {'name': 'Toptal', 'url': 'https://www.toptal.com/'},
    {'name': 'Elastic Search', 'url': 'http://www.elastic.co'},
    {'name': 'Crossover', 'url': 'http://www.crossover.com'},
    {'name': 'inVision', 'url': 'http://www.invisionapp.com'},
    {'name': 'Automattic', 'url': 'http://automattic.com'},
    {'name': 'Zapier', 'url': 'https://zapier.com'},
    {'name': 'GitLab', 'url': 'https://about.gitlab.com/'},
    {'name': 'Stack Overflow', 'url': 'http://www.stackoverflow.com'},
    {'name': 'Doist', 'url': 'https://doist.com'},
    {'name': 'GitHub', 'url': 'https://github.com/about'}
]

# Define a dictionary to store the scraped data
data = {
    "Company": [],
    "About Us": []
}

# Function to scrape the "About Us" page
def scrape_about_us(company_name, url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.content, 'html.parser')

        # Attempt to find the "About Us" section in various ways
        about_us_text = None
        
        # Check for common sections that might contain "About Us" information
        possible_sections = soup.find_all(['section', 'div', 'p'], text=lambda t: t and 'about' in t.lower())
        if possible_sections:
            about_us_text = ' '.join([section.get_text(strip=True) for section in possible_sections])

        # Default text if no section found
        if not about_us_text:
            about_us_text = "No specific 'About Us' section found"
        
        data["Company"].append(company_name)
        data["About Us"].append(about_us_text)

    except Exception as e:
        data["Company"].append(company_name)
        data["About Us"].append(f"Error occurred: {e}")

# Scrape each company's "About Us" page
for company in companies:
    scrape_about_us(company['name'], company['url'])

# Create a DataFrame from the dictionary
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
output_file = "fro_about_us.xlsx"
df.to_excel(output_file, index=False)

print(f"Data has been successfully scraped and saved to {output_file}")
