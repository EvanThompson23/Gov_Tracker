import xml.etree.ElementTree as ET 
from clerk import DataScrape as DS
from datetime import date as dtoday
from trade import Trade as Trade
import PyPDF2 #type:ignore
from io import BytesIO 

class File_Format:
    def check_new_trades(xml_file, tracked_names, date):
        root = ET.fromstring(xml_file.decode())
        reports = []
        for child in root:
            if child.find("FilingType").text == "P":
                last_name = child.find("Last").text
                date_filed = child.find("FilingDate").text
                for name in tracked_names:
                    if (date_filed == date or date == None) and (last_name == name or name == "All"): 
                        id = child.find("DocID").text
                        reports.append([last_name, date_filed[-4:], id])        
        return reports 
    
    def get_PDF_text(PDF_file):
        PDF_bytes = BytesIO(PDF_file)
        PDF = PyPDF2.PdfReader(PDF_bytes)
        PDF_text = ""
        for page in PDF.pages:
            PDF_text += page.extract_text()
        return PDF_text

class Breakdown:
    def text_breakdown(self, text, person):
        trades_text = self.get_trade_strings(text)
        trades = []
        for trade in trades_text:
            p_date = self.get_purchase_date(trade)           
            f_date = self.get_filing_date(trade)
            if stock := self.get_stock(trade) == None: continue
            action = self.get_action(trade)
            amount = self.get_amount(trade)
            trades.append(t := Trade(person, p_date, f_date, stock, action, amount))
            t.print_all()
        return trades   

    def remove_chars(self, text):
        text = text.replace('\x00', '')
        text = text.replace('/x00', '')
        text = text.replace('(partial)', '')
        return text

    def get_trade_strings(self, text):
        text = self.remove_chars(text)
        text = text.splitlines()
        #for te in text:
            #print(te)
        SP = False
        trade_string = ''
        trade_strings = []
        for line in text:
            print(line)
            if line[:4] == 'F S:':
                trade_strings.append(trade_string[4:])
                SP = False
                print("------> " + trade_string)
                trade_string = ''
            if line[:2] == 'SP' or SP: # "SP" is at the start of ever stock trade
                if line[:1] == "$":
                    trade_string += (" " + line[:9])
                    continue
                trade_string += (" " + line)
                SP = True
        return trade_strings

    def get_stock(self, trade):
        if len(t:= trade[(trade.find("(") +1):trade.find(")")]) <= 4  : return t; return None

    def get_action(self, trade):
                if trade.find("P ") != -1:
                    return "Purchased"
                elif trade.find("S ") != -1:
                    return "Sold"
                return None 

    def get_purchase_date(self, trade):
        if (placement := trade.find("/")) == -1:
            return None
        return trade[placement-2:placement+8]
    
    def get_filing_date(self, trade):
        if (placement := trade.rfind("/")) == -1:
            return None
        return trade[placement-5:placement+5]
    
    def get_amount(self, trade):
        return trade[trade.find("$"):trade.rfind("0")+1]
    

xml_file = DS.quick_xml_file() 
tracked_names = ["All"] # "All" used to track every congress man
date = None # dtoday.today().strftime("%-m/%-d/%Y") # Todays date used if any date wanted use None ("%-m/%-d/%y")
reports = File_Format.check_new_trades(xml_file, tracked_names, date)
trades = []
for report in reports:
    PDF_file = DS.quick_trade_PDF(report)
    PDF_text = File_Format.get_PDF_text(PDF_file)
    trades += Breakdown().text_breakdown(PDF_text, report[0])

for trade in trades:
    trade.print_all()