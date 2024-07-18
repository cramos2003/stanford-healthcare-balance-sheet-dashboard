# For scraping dynamic website content with static content links
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import requests

# For scraping pdfs
from pypdf import PdfReader
import requests
import io

# For parsing through pdf data using regular expressions (regex)
import re

# For adding dictionary frames to database
from pipeline import PostgresPipeline

# For access to google gemini model for text summarization
import google.generativeai as genai

url = 'https://stanfordhealthcare.org/about-us/bondholder-general-financial-information/audited-financial-statements.html'

class PdfScraper:
    def __init__(self):
        try:
            self.driver = webdriver.Edge()
        except:
            print("Could not open webdriver Edge")

    def open_link(self, link):
        try:
            self.driver.get(link)
        except:
            print("error, could not open link")

    def get_pdf_links(self, parent_tag, parent_class):
        try:
            links = self.driver.find_element(By.CLASS_NAME, parent_class)
            link_list = links.find_elements(By.TAG_NAME, 'a')
        except:
            print("Could not get pdf links or paths")
        return link_list

    def get_pdf_content(self, pdf):
        r = requests.get(pdf)
        text = ""
        if r.status_code == 200:
            with io.BytesIO(r.content) as f:
                pdf = PdfReader(f)
                num_pages = pdf.get_num_pages()
                for page in range(num_pages):
                    p = pdf.pages[page]
                    rotation_deg = p.get('/Rotate')
                    if rotation_deg != 0:
                        text += "\n" + p.extract_text()
        else:
            print(f"Error downloading pdf: {r.status_code}")
        return text
    
    def stop(self):
        self.driver.quit()

def grab_all_integers(item : str):
    result = []
    large_int = ''
    for i in item:
        if i.isdigit():
      # Append digit to current number
            large_int += i
        elif i == '-':
            large_int = '0'
        elif large_int and not i.isdigit():
        # Add smaller number or non-digit character as-is
            result.append(large_int)
            large_int = ""
          # Add the last number if it exists
    if large_int:
        result.append(large_int)

    return result

def grab_all_labels(data : str):
    result = ''
    for d in data:
        if d.isdigit():
            result += ' '
            continue
        else:
            result += d

    result = result.strip()
    result = result.split(sep='  ')
    temp = []
    for r in result:
        if len(r) > 1:
            temp.append(r)
    result = temp
    return result

def parse_for_table_data(text : str):
    cleaned_numbers = []
    stop_characters = ['', ' ', '  ', '   ', '    ']
    text = text.split(sep='\n')
    for t in text:
        t = t.replace(',', '')
        t = t.replace('$', '')
        t = t.strip()
        t = t.split(sep=' ')
        try:
            t.remove('')
        except:
            pass
        try:
            t.remove(' ')
        except:
            pass
        if len(t) == 0:
            continue
        t = ' '.join(map(str, t))
        temp = grab_all_integers(t)
        if len(temp) == 0:
            continue
        cleaned_numbers.append(temp)
    financial_data = []
    for i in cleaned_numbers:
        if len(i) < 10:
            continue
        financial_data.append(i)
    return financial_data

def create_frame(financials : list):
    sections = ['TotalCurrentAssets', 'TotalAssets', 'TotalCurrentLiabilities',
                'TotalLiabilities', 'TotalWithoutDonorRestrictions', 'TotalNetAssets',
                'TotalLiabilitiesAndAssets']
    financial_dictionary = dict()
    section_total = 0
    prev_total = 0
    counter = 0
    
    for f in financials:
        sec = sections[counter]
        carry_total = section_total + prev_total
        if carry_total == int(f[-1]):
            prev_total = carry_total
            financial_dictionary[sec] = carry_total
            counter += 1
            continue

        elif section_total == int(f[-1]):
            financial_dictionary[sec] = section_total
            prev_total = section_total
            section_total = 0
            counter += 1
            continue
        
        section_total += int(f[-1])
        
    return financial_dictionary

def scraper():
    S = PdfScraper()
    S.open_link(url)
    pdf_links = S.get_pdf_links('table', 'shc-table-zebra')
    scraped_frames = []
    for pdf in pdf_links:
        try:
            pdf_text = S.get_pdf_content(pdf.get_attribute('href'))
            financials = parse_for_table_data(pdf_text)
            frame = create_frame(financials)
            frame['PdfLink'] = pdf.get_attribute('href')
            frame['NetAssets'] = int(frame['TotalAssets']) - int(frame['TotalLiabilities'])
            frame['NetWorth'] = int(frame['TotalAssets']) + int(frame['TotalLiabilities'])
            frame['WorkingCapital'] = int (frame['TotalCurrentAssets']) - int(frame['TotalCurrentLiabilities'])
            frame['CapitalEmployed'] = int(frame['TotalAssets']) - int(frame['TotalCurrentLiabilities'])
            frame['DebtRatio'] = int(frame['TotalLiabilities']) / int(frame['TotalAssets'])
            frame['DebtRatioShortTerm'] = int(frame['TotalCurrentLiabilities']) / int(frame['TotalCurrentAssets'])
            frame['DebtToEquityRatio'] = int(frame['TotalLiabilities']) / int(frame['NetAssets'])
            scraped_frames.append(frame)
        except:
            print(f"Could not get info for: {pdf.get_attribute('href')}")
    S.stop()
    pipeline = PostgresPipeline()
    for frame in scraped_frames:
        pipeline.open()
        print("loading frame to database...")
        pipeline.process_item(frame)
        print("Successfully loaded frame!")
    pipeline.close()
scraper()