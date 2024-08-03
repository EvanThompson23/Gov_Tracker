import io
import requests
import zipfile
from datetime import date as dtoday

class DataScrape:
    def quick_trade_PDF(info):
        link = f"https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{info[1]}/{info[2]}.pdf"
        return requests.get(link).content

    def quick_xml_file():
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



   