import requests
from bs4 import BeautifulSoup
import re


url = 'please add URL'

# Headers to mimic a real browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

# Send a GET request to the URL
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    print("Successfully fetched the page.")
    soup = BeautifulSoup(response.content, 'html.parser')

    # Sets to store unique document codes
    personal_codes = set()
    business_codes = set()

   
    accordion_buttons = soup.find_all('button', class_='-oneX-panel-button')

    for button in accordion_buttons:
        section_name = button.get_text(strip=True).lower()
        aria_controls = button.get('aria-controls')

        # Find the corresponding panel using the aria-controls attribute
        panel = soup.find(id=aria_controls)
        if not panel:
            continue

        
        pdf_links = panel.find_all('a', href=re.compile(r'\.pdf$'))

        for link in pdf_links:
            href = link['href']
         
            match = re.search(r'/([^/]+)\.pdf$', href)
            if match:
                doc_code = match.group(1).strip()
               
                if 'business' in section_name:
                    business_codes.add(doc_code)
                else:
                    personal_codes.add(doc_code)

    
    with open('personal.txt', 'w') as personal_file:
        for code in sorted(personal_codes):
            personal_file.write(code + '\n')

    with open('business.txt', 'w') as business_file:
        for code in sorted(business_codes):
            business_file.write(code + '\n')
# below print statements added to just check in local Sys [optional]
    print("Document codes have been written to 'personal.txt' and 'business.txt'.")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
