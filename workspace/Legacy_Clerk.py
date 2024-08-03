import time
import io
import requests
import zipfile
from datetime import date as dtoday
from selenium import webdriver # type:ignore
from selenium.webdriver.chrome.service import Service # type:ignore
from webdriver_manager.chrome import ChromeDriverManager # type:ignore
from selenium.webdriver.chrome.options import Options # type:ignore
from selenium.webdriver.common.keys import Keys # type:ignore

class DataScrape:
    def __init__(self):
        # Options chosen specifically for use in a docker container
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)        

    def pull_trade_PDFs(self, last_name):
        
        pull_driver = self.driver
        pull_driver.get("https://disclosures-clerk.house.gov/PublicDisclosure/FinancialDisclosure")
        search_reports = pull_driver.find_element("xpath",'//*[@id="main-content"]/div/div[1]/ul/li[7]/a')
        search_reports.click()

        time.sleep(2)

        search_box = pull_driver.find_element("xpath",'//input[@name="LastName"]')
        search_box.clear()
        search_box.send_keys(last_name) # Non Object needs to become file stored or user inputted
        search_box.send_keys(Keys.RETURN)

        time.sleep(2)

        filing_year_column = pull_driver.find_element("xpath",'//*[@id="DataTables_Table_0"]/thead/tr/th[3]')
        filing_year_column.click()
        time.sleep(1)
        filing_year_column.click()

        time.sleep(2)

        body = pull_driver.find_element("xpath",'//*[@id="DataTables_Table_0"]/tbody')
        reports = body.find_elements("css selector", '[role="row"]')
        trade_PDFs = []
        
        for report in reports:
            link = report.find_element("tag name",'a').get_attribute("href") # pulls links to all recent trades
            trade_PDFs.append([link, requests.get(link).content]) # add this to an array in init.

        trade_PDFs.sort(reverse=True, key=lambda x: x[0])

        return trade_PDFs
    
    def pull_trade_PDF(self, last_name):
        return self.pull_trade_PDFs(last_name)[0][1]
    def quick_trade_PDF(self, info):
        link = f"https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{info[1]}/{info[2]}.pdf"
        return requests.get(link).content
        
    def pull_xml_file(self):
        
        check_driver = self.driver
        check_driver.get("https://disclosures-clerk.house.gov/PublicDisclosure/FinancialDisclosure")

        time.sleep(1)

        content = check_driver.find_element("xpath", '//*[@id="Report"]')
        list = check_driver.find_element("xpath", '/html/body/section/div/div[2]/div[1]/section/div[2]')
        years = list.find_elements("tag name", 'tag')
        link = years[len(years)-1].find_element("tag name",'a').get_attribute("href")
        fd_zip = io.BytesIO(requests.get(link).content)
        
        xmlfile = None
        with zipfile.ZipFile(fd_zip, 'r') as z:
            files = z.namelist()
            for file in files:
                if file.__contains__(".xml"):
                    xmlfile = z.read(file)

        return xmlfile

    def quick_xml_file(self):
        year = dtoday.today().strftime("%Y")
        link = f"https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{year}FD.zip"
        fd_zip = io.BytesIO(requests.get(link).content)
        
        xmlfile = None
        with zipfile.ZipFile(fd_zip, 'r') as z:
            files = z.namelist()
            for file in files:
                if file.__contains__(".xml"):
                    xmlfile = z.read(file)

        return xmlfile

    def get_driver(self):
        return self.driver

    def set_trade_PDFs(self, trade_PDFs):
        self.trade_PDFs = trade_PDFs


   