import sqlite3
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
#create a database to store the data
conn=sqlite3.connect("ifb.db")
cur=conn.cursor()
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS ifb(
        COUPONNAME TEXT,
        COUPONRATE TEXT,
        DATE TEXT
    )
    """
)
# GET THE LINKS 
site = requests.get("https://www.ifb.ir/ytm.aspx")
soup = BeautifulSoup(site.content, "html.parser")
table_list = soup.find("table", {"class": "mGrid"})
a_list = table_list.findAll("a")
links = []
for a in a_list:
    super_link = "https://www.ifb.ir/" + a["href"]
    links.append(super_link)
    
# GET THE LINK FROM LINKS THEN GET ALL THE SPECIFIC TR
driver = webdriver.Chrome()
for link in links:
    driver.get(link)
    table_element = driver.find_element(By.XPATH, "//table[@class='mGrid']")
    tr_element = table_element.find_elements(By.XPATH,".//tr")
    for tr in tr_element:
        td_element = tr.find_elements(By.XPATH, "//tr[@class='alt']")
    data = [element.text for element in td_element if element.text]
    
#GET THE COPOUNNAME ANF COUPONRATE
    name=[]
    tables=driver.find_elements(By.XPATH,"//table[@class='insTable Info']")
    first_tr_elements = [table.find_element(By.TAG_NAME, 'tr') for table in tables]
    for row in first_tr_elements:
        cells=row.find_elements(By.TAG_NAME,"td")
        if len(cells)>1:
            second_cell_text=cells[1].text
            name.append(second_cell_text)
            finalnamelist=name[0]  
            # print(finalnamelist)  
    for i in data:
        if type(i)==str:
            data.remove(i)
    # print(data[1])
    
#SEPERATE DATA AND COUPONRATE FROM EACHOTHER
    try:    
        name1=finalnamelist
        date1=data[1][0:10]
        rate1=data[1][11:]
    except:
        print("-")    
    
#INSERT THE INFORMATION INTO THE IFB.DB TABLE AND AVOIDING DUPLICATES 
    cur.execute("""
        INSERT OR IGNORE INTO ifb (COUPONNAME, COUPONRATE, DATE) 
        VALUES (?,?,?)
    """, (name1,rate1, date1))
    conn.commit()
conn.close()