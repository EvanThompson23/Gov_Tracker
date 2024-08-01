import xml.etree.ElementTree as ET 
from clerk import DataScrape as DS
from datetime import date as dtoday
import requests
import PyPDF2 #type:ignore
from io import BytesIO 

class trades:
    def __init__(self):
        self.tracked_name = "All"
        self.DS = DS()

    def check_new_trades(self):
        xml_file = self.DS.quick_xml_file() #move this later and pass in the xml file
        root = ET.fromstring(xml_file.decode())
        today = dtoday.today().strftime("%-m/%d/%Y")
        reports = []
        for child in root:
            if child.find("FilingType").text == "P":
                last_name = child.find("Last").text
                date = child.find("FilingDate").text
                any_date = True # For testing a larger set of results
                if (date == today or any_date) and (last_name == self.tracked_name or self.tracked_name == "All"):
                    id = child.find("DocID").text
                    reports.append([last_name,date[-4:],id])        
        return reports 
    
    def get_trades(self, reports):
        all_trades = []
        for info in reports:
            # pdf = self.DS.pull_trade_PDF(info[0])
            pdf = self.DS.quick_trade_PDF(info)
            pdf_file = BytesIO(pdf)
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            # all_trades.append([info[0],"Blank"]) # This is for testing and documentation
            all_trades += self.text_breakdown(text)
        return all_trades

    def text_breakdown(self,text):
        trades = []
        text = text.splitlines()
        SP_hold = ""
        SP_bool = False
        stock = ""
        action = ""
        for line in text:
            line.replace('\x00', '')
            if line[:2] == 'SP':
                SP_hold = line[-2:] # Necessary to not flag the purchased action 
                SP_bool = True
                continue
            if SP_bool:
                SP_bool = False
                SP_hold += line
                stock = SP_hold[(SP_hold.find("(") +1):SP_hold.find(")")]
                if len(stock) > 4 or len(stock) < 1: # Checks for Example NVAD instead of entire line
                    continue
                if SP_hold.find("P ") != -1:
                    print(SP_hold)
                    action = "Purchased"
                elif SP_hold.find("S ") != -1:
                    action = "Sold"
                else:
                    continue
                trades.append([stock, action])
        return trades

t = trades()
reports = t.check_new_trades()
trades = t.get_trades(reports)
for trade in trades:
    print(trade)