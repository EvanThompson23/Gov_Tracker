import xml.etree.ElementTree as ET 
from clerk import DataScrape as DS
from datetime import date as dtoday
import requests
import PyPDF2 #type:ignore
from io import BytesIO 

class trades:
    def __init__(self):
        self.tracked_name = "Pelosi"
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
                any_date = True
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
            all_trades.append([info[0],"Blank"])
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
                SP_hold = line
                SP_bool = True
                continue
            if SP_bool:
                SP_bool = False
                SP_hold += line
                first_bracket = SP_hold.find("(")
                second_bracket = SP_hold.find(")")
                stock = SP_hold[first_bracket+1:second_bracket]
                p_location = SP_hold.find("P ")
                if p_location != -1:
                    action = "Purchased"
                s_location = SP_hold.find("S ")
                if s_location != -1:
                    action = "Sold"
                trades.append([stock, action])
        return trades
t = trades()
reports = t.check_new_trades()
trades = t.get_trades(reports)