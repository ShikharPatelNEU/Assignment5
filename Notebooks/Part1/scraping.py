import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import re
from dotenv import load_dotenv
load_dotenv()
import boto3
from botocore.exceptions import NoCredentialsError

# Function to setup Chrome WebDriver
def setup_driver():
   chrome_options = Options()
   chrome_options.add_argument("--headless")  # Ensures Chrome runs in headless mode
   chrome_options.add_argument("--no-sandbox")
   chrome_options.add_argument("--disable-dev-shm-usage")
   driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
   return driver


# Function to scrape content from each reading link
def scrape_reading_content(driver, url):
    readings = []
    driver.get(url)
    time.sleep(2)  # Wait for the page to load
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # Extract relevant information from the page
    title = soup.find('h1').text.strip() if soup.find('h1') else 'Title Not Found'
    topic = soup.find("span", class_="content-utility-topics").text.strip() if soup.find("span", class_="content-utility-topics") else "Topic Not Found"
    # Extract the topic from the page
    topic = soup.find("span", class_="content-utility-topics").text.strip() if soup.find("span", class_="content-utility-topics") else "Topic Not Found"
    
    # Find and extract the required publication year
    year_text = soup.find("span", class_="content-utility-curriculum").text.strip() if soup.find("span", class_="content-utility-curriculum") else "Year Not Found"
    # Use regular expression to find all numbers in the extracted text
    year_match = re.search(r'\d{4}', year_text)
    # If a year is found, use the first match, otherwise default to "Year Not Found"
    year = year_match[0] if year_match else "Year Not Found"
        # Function to extract text based on header texts
    def extract_text_by_header(soup, header_texts):
        content = ""
        # Normalize header_texts to lowercase for case-insensitive comparison
        header_texts = [text.lower() for text in header_texts]
        headers = soup.find_all('h2', class_='article-section')
        for header in headers:
            if header.text.strip().lower() in header_texts:
                current_element = header.find_next_sibling()
                while current_element and current_element.name != 'h2':
                    if current_element.name in ['p', 'div', 'ol']:
                        content += '\n' + ' '.join(current_element.stripped_strings)
                    current_element = current_element.find_next_sibling()
                if content:  # Break if content has been found
                    break
        return content.strip()

        # Function to extract learning outcomes
    def extract_learning_outcomes(soup):
        content = ""
        header = soup.find('h2', text=lambda t: "Learning Outcomes" in t, class_='article-section')
        if header:
            section = header.find_next_sibling('section')
            if section:
                content = ' '.join(section.stripped_strings)
        return content.strip()


    # Extracts the introduction section from the page using predefined headers.
    introduction = extract_text_by_header(soup, ['Introduction', 'Overview', 'INTRODUCTION'])
    # Extracts the learning outcomes section from the page.
    learning_outcomes = extract_learning_outcomes(soup)
    # Extracts the summary section from the page using the 'Summary' header.
    summary = extract_text_by_header(soup, ['Summary','Conclusions and Summary'])

    # Find and extract the required publication year, level, links to the pdf
    level = soup.find("span", class_="content-utility-topic").text.strip() if soup.find("span", class_="content-utility-topic") else "Level Not Found"
    link_to_full_pdf = soup.find("a", class_="locked-content")["href"].strip() if soup.find("a", class_="locked-content") else "Link Not Found"

    # Appends the extracted information as a dictionary to the readings list.
    readings.append({
        'Article': title,
        'Topic': topic,
        'Year': year,
        'Level' : level,
        'Introduction': introduction,
        'Learning Outcomes': learning_outcomes,
        'Summary': summary,
        'Link to the Summary Page': url,
        'Link to the PDF File': link_to_full_pdf
    })

    return readings

# Function to save the scraped data into a CSV file.
def save_to_csv(readings, filename="Team05.csv"):
    keys = readings[0].keys() # Extracts the keys from the first dictionary to use as column headers.
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader() # Writes the column headers.
        dict_writer.writerows(readings) # Writes the rows of data.

# Function to save the scraped data into a CSV file and upload it to S3.
def save_to_csv_and_upload_to_s3(readings, filename="Team05.csv", bucket_name="your-bucket-name"):
    keys = readings[0].keys()  # Extracts the keys from the first dictionary to use as column headers.
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()  # Writes the column headers.
        dict_writer.writerows(readings)  # Writes the rows of data.
    
    # Upload the file to S3
    s3 = boto3.client('s3')
    try:
        s3.upload_file(filename, bucket_name, filename)
        print(f"File {filename} uploaded to S3 bucket {bucket_name}")
    except NoCredentialsError:
        print("Credentials not available")

# Imports for handling specific exceptions from Selenium.
from selenium.common.exceptions import NoSuchElementException, JavascriptException


def main():
    driver = setup_driver() # Initializes the WebDriver.
    # List of URLs to scrape.
    
    urls = ['https://www.cfainstitute.org/membership/professional-development/refresher-readings/overview-equity-portfolio-management',
            'https://www.cfainstitute.org/membership/professional-development/refresher-readings/industry-company-analysis',
            'https://www.cfainstitute.org/membership/professional-development/refresher-readings/2018/discounted-dividend-valuation']
    all_readings = []

    try:
        for url in urls:
            #links = get_reading_links(driver, url)
            readings = scrape_reading_content(driver, url)
            all_readings.extend(readings)
        save_to_csv(all_readings)
        save_to_csv_and_upload_to_s3(all_readings, 'Team05.csv', 'assignment-5-7245')

    finally:
        driver.quit()

if __name__ == '__main__':
    main()

 