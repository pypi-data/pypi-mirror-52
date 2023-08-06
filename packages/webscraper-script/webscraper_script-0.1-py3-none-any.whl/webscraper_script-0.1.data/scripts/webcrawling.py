'''Weather Application Web Crawling Task
Author: Akash Kundu
'''

import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
place=input("Enter Place Name: ")#The user should enter the place to get the weather information.
print("Please wait for a few seconds while the page loads.....")
browser = webdriver.Firefox(executable_path='C:/Users/geckodriver')#Place the geckodriver executable inside any local folder of your choice.
browser.get("https://weather.com/en-IN/")#Loading webpage source code.
time.sleep(8)#Waiting for some seconds for the webpage to load properly.
try:
        print("Selenium is now trying to Enter your location in the Webpage")
        browser.find_element_by_css_selector("#header-TwcHeader-144269fc-62bc-4d06-bc79-e158594b14ff > div > div > div > div.styles__content__1OMmY.styles__ready__2ZM2w.all-ready > div > div.styles__input__GVnwF.typeahead-wrapper > div > input").send_keys(place + Keys.ENTER)
        time.sleep(7) #hyperlink loading time relaxation given here.
        #the above line of code inserts user inputted data in the search tag and presses ENTER to submit
        sop = BeautifulSoup(browser.page_source, 'html.parser')
        all=sop.find("div",{"class":"search section-local-suite page"}).find("li").find('a')['href']  #Returns the first location hyperlink returned from search
        time.sleep(3)
        r = requests.get(all)#Loading webpage source code.
        c1 = r.content
        soup = BeautifulSoup(c1, "html.parser")
except:
        print("Selenium has failed to input location,Please Try again later!!") #please check your Geckodriver Installation
        print('Please find your default location information below: ')
        r = requests.get("https://weather.com/en-IN/")#Loading default webpage source code.
        c1 = r.content
        soup = BeautifulSoup(c1, "html.parser")


tod_mon_hourly = []  #This list contains all the hyperlinks to the tab-links:today,monthly,ten-day,hourly,etc
for ul in soup.find_all('div', class_='styles__root__2gUGa'):
    for li in ul.find_all('li'):
        a = li.find('a')
        tod_mon_hourly.append(a['href'])

print("Enter your choice to view weather details accordingly :")
choice=input("Enter as given: 1 for Today, 2 for Hourly, 3 for Monthly, 4 for Ten-days: ")
choic=int(choice)

if choic==1:
    r1_today = requests.get('https://weather.com' + tod_mon_hourly[0])#Getting the today hyper-link
    c2 = r1_today.content
    soup1 = BeautifulSoup(c2, "html.parser")
    d = {} #Empty dictionary to store the weather details of today
    d["region"] = soup1.find("div", {"class": "region region-hero-left"}).find("h1").text
    d["Temp"] = soup1.find("div", {"class": "today_nowcard-temp"}).text
    d["Phrase"] = soup1.find("div", {"class": "today_nowcard-phrase"}).text
    d["Feels"] = soup1.find("div", {"class": "today_nowcard-feels"}).text
    d["High-Low"] = soup1.find("div", {"class": "today_nowcard-hilo"}).text
    print("Today's Weather details: ")
    print(d) #Printing the weather details of today

elif choic==2:
    r3_hourly = requests.get('https://weather.com' + tod_mon_hourly[1])#hourly weather details hyper-link
    d3 = r3_hourly.content
    soup3 = BeautifulSoup(d3, "html.parser")
    Hourtitle1 = soup3.find("div", {"class": "hourly section-local-suite page"}).find("h1").text
    print("Hourly Weather details: ")
    print("Region name "+Hourtitle1)
    al = []
    table = soup3.find_all("table", {"class": "twc-table"})
    for items in table:
        for i in range(len(items.find_all("tr")) - 1):
            d_tmp = {}
            try:
                d_tmp["desc"] = items.find_all("td", {"class": "description"})[i].text
                d_tmp["temp"] = items.find_all("td", {"class": "temp"})[i].text
                d_tmp["precip"] = items.find_all("td", {"class": "precip"})[i].text
                d_tmp["wind"] = items.find_all("td", {"class": "wind"})[i].text
                d_tmp["humidity"] = items.find_all("td", {"class": "humidity"})[i].text
            except:
                d_tmp["desc"] = "None"
                d_tmp["temp"] = "None"
                d_tmp["precip"] = "None"
                d_tmp["wind"] = "None"
                d_tmp["humidity"] = "None"

        al.append(d_tmp)

    print(al)#printing the hourly weather details

elif choic==3:
    r4_monthly = requests.get('https://weather.com' + tod_mon_hourly[5])#monthly weather details hyper-link
    d4 = r4_monthly.content

    soup4 = BeautifulSoup(d4, "html.parser")

    alp = []
    divs = soup4.find_all("div", {"class": "monthly section-local-suite page"})
    for items in divs:
        for i in range(30):
            dv = {}
            try:
                dv["Place "] = soup4.find("div", {"class": "monthly section-local-suite page"}).find("h1").text
                dv["Time "] = soup4.find("div", {"class": "observation-timestamp"}).text
                dv["Day "] = soup4.find("div", {"class": "date"}).text
                dv["Temp H-L"] = soup4.find("div", {"class": "temps"}).text
            except:
                d["Place "] = "None"
                d["Time "] = "None"
                d["Day "] = "None"
                d["Temp H-L"] = "None"

        alp.append(dv)

    print("Monthly Weather details")
    print(alp)#printing monthly weather details


elif choic==4:

    r5_tendays = requests.get('https://weather.com' + tod_mon_hourly[3])#ten days Weather details hyper-link
    d5 = r5_tendays.content
    soup5 = BeautifulSoup(d5, "html.parser")
    ten_days = []
    ten = soup5.find("div", {"class": "locations-title ten-day-page-title"}).find("h1").text

    table=soup5.find_all("table",{"class":"twc-table"})
    for items in table:
        for i in range(len(items.find_all("tr"))-1):
            d = {}
            try:
                d["day"]=items.find_all("span",{"class":"date-time"})[i].text
                d["date"]=items.find_all("span",{"class":"day-detail"})[i].text
                d["desc"]=items.find_all("td",{"class":"description"})[i].text
                d["temp"]=items.find_all("td",{"class":"temp"})[i].text
                d["precip"]=items.find_all("td",{"class":"precip"})[i].text
                d["wind"]=items.find_all("td",{"class":"wind"})[i].text
                d["humidity"]=items.find_all("td",{"class":"humidity"})[i].text
            except:
                d["day"]="None"
                d["date"]="None"
                d["desc"]="None"
                d["temp"]="None"
                d["precip"]="None"
                d["wind"]="None"
                d["humidity"]="None"
            ten_days.append(d)
    print("Ten Days Weather Details: ")
    for i in range(len(ten_days)):
        print(ten_days[i])
