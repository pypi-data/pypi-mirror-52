import pandas
from tkinter import messagebox
from tkinter import *
window=Tk()
window.wm_title("WebCrawler_Weather")
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys


window.configure(background='gray91')#setting window color

def enter_place():
    if place_text.get()=="":
        list1.delete(0,END)
        list1.insert(END,"Please enter valid name and then click on 'Enter Place' button")
    else:
        global place
        list1.delete(0,END)
        list1.insert(END,("You have entered: "+place_text.get().title()+" as your location"))
        list1.insert(END,"Now click on Run Button to get " +place_text.get().title()+"'s"+ " weather details")
        place=place_text.get()

def web_run():
    browser = webdriver.Firefox(executable_path='C:/Users/geckodriver')#Place the geckodriver executable inside any local folder of your choice.
    browser.get("https://weather.com/en-IN/")#Loading webpage source code.
    window.update()
    time.sleep(7)#Waiting for some seconds for the webpage to load properly.
    #window.after(8000)
    try:
            #print("Selenium is now trying to Enter your location in the Webpage")
            browser.find_element_by_css_selector("#header-TwcHeader-144269fc-62bc-4d06-bc79-e158594b14ff > div > div > div > div.styles__content__1OMmY.styles__ready__2ZM2w.all-ready > div > div.styles__input__GVnwF.typeahead-wrapper > div > input").send_keys(place + Keys.ENTER)
            window.update()
            time.sleep(6) #hyperlink loading time relaxation given here.
            #the above line of code inserts user inputted data in the search tag and presses ENTER to submit
            #window.after(7000)
            sop = BeautifulSoup(browser.page_source, 'html.parser')
            all=sop.find("div",{"class":"search section-local-suite page"}).find("li").find('a')['href']  #Returns the first location hyperlink returned from search
            #window.after(3000)
            r = requests.get(all)#Loading webpage source code.
            c1 = r.content
            soup = BeautifulSoup(c1, "html.parser")
            list1.delete(0,END)
            list1.insert(END, "Your results are now ready! Please click on respective buttons to view weather details.")
            list1.insert(END, "Press Today: To view today's weather details")
            list1.insert(END, "Press Hourly: To view hourly weather details")
            list1.insert(END, "Press Monthly: To view monthly weather details")
            list1.insert(END, "Press Ten-days: To view ten day's weather details")
    except:
            messagebox.showerror("Try again!","Geckodriver/Network issue, please try again")
            list1.delete(0,END)
            list1.insert(END,"Program has failed to input location,Please Try again by clicking Run button!!")
            list1.insert(END,"Or you can find your default location informations by clicking respective buttons")
            #print("Selenium has failed to input location,Please Try again later!!") #please check your Geckodriver Installation
            #print('Please find your default location information below: ')
            r = requests.get("https://weather.com/en-IN/")#Loading default webpage source code.
            c1 = r.content
            soup = BeautifulSoup(c1, "html.parser")

    global tod_mon_hourly
    tod_mon_hourly = []  #This list contains all the hyperlinks to the tab-links:today,monthly,ten-day,hourly,etc
    for ul in soup.find_all('div', class_='styles__root__2gUGa'):
        for li in ul.find_all('li'):
            a = li.find('a')
            tod_mon_hourly.append(a['href'])
    browser.quit()#Exiting the web-browser as information has been extracted

def choice_1():
        r1_today = requests.get('https://weather.com' + tod_mon_hourly[0])#Getting the today hyper-link
        c2 = r1_today.content
        soup1 = BeautifulSoup(c2, "html.parser")
        d = {} #Empty dictionary to store the weather details of today
        d["region"] = soup1.find("div", {"class": "region region-hero-left"}).find("h1").text
        d["Temp"] = soup1.find("div", {"class": "today_nowcard-temp"}).text
        d["Phrase"] = soup1.find("div", {"class": "today_nowcard-phrase"}).text
        d["Feels"] = soup1.find("div", {"class": "today_nowcard-feels"}).text
        d["High-Low"] = soup1.find("div", {"class": "today_nowcard-hilo"}).text
        return d

def choice_2():
        r3_hourly = requests.get('https://weather.com' + tod_mon_hourly[1])#hourly weather details hyper-link
        d3 = r3_hourly.content
        soup3 = BeautifulSoup(d3, "html.parser")
        Hourtitle1 = soup3.find("div", {"class": "hourly section-local-suite page"}).find("h1").text
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
        return al


def choice_3():
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
            return alp


def choice_4():
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
        return ten_days


def jsonf():
    try:
        list1.delete(0,END)
        list1.insert(0,"Saving JSON files as given below:")
        list1.insert(1,"Today's weather: output_today.json")
        list1.insert(2,"Hourly weather: output_Hourly.json")
        list1.insert(3,"Monthly weather: output_Monthly.json")
        list1.insert(4,"Ten-days weather: output_Tendays.json")
        a=choice_1()
        df=pandas.Series(a).to_frame()
        df.to_json("output_today.json")
        a=choice_2()
        df=pandas.Series(a).to_frame()
        df.to_json("output_Hourly.json")
        df=pandas.Series(a).to_frame()
        df.to_json("output_Monthly.json")
        a=choice_4()
        df=pandas.Series(a).to_frame()
        df.to_json("output_Tendays.json")
        list1.insert(5,"Saved Successfully!")
    except:
        list1.delete(0,END)
        list1.insert(0,"Please run the program first!")

l1=Label(window, text="Place Name: ")
l1.grid(row=0,column=0)

place_text=StringVar()
e1=Entry(window,textvariable=place_text)
e1.grid(row=0,column=1)
e1.focus()

#Defining the button coomands below
def run_com():
    list1.delete(0,END)
    web_run()

def choice_1a():
    try:
        list1.delete(0,END)#deletes or clear textbox so that row appending can be avoided when we click view button multiple times
        list1.insert(0,"Today Weather details")
        a=choice_1()
        list1.insert(END,a)#inserts row at the end of textbox
    except:
        list1.delete(0,END)
        list1.insert(0,"Please run the program first!")

def choice_2a():
    try:
        list1.delete(0,END)
        list1.insert(0,"Hourly Weather details")
        a=choice_2()
        list1.insert(END, a)
    except:
        list1.delete(0,END)
        list1.insert(0,"Please run the program first!")

def choice_3a():
    try:
        list1.delete(0,END)
        list1.insert(0,"Monthly Weather details")
        a=choice_3()
        list1.insert(END, a)
    except:
        list1.delete(0,END)
        list1.insert(0,"Please run the program first!")

def choice_4a():
    try:
        list1.delete(0,END)
        list1.insert(0,"Ten-days Weather details")
        for row in choice_4():
            list1.insert(END, row)
    except:
        list1.delete(0,END)
        list1.insert(0,"Please run the program first!")




#Defining tkinter GUI layouts
list1=Listbox(window,height=15,width=75,font=("Helvetica", 10))
list1.grid(row=1,column=0,rowspan=6,columnspan=2)

list1.delete(0,END)
list1.insert(END,"Welcome to the webcrawler app")
list1.insert(END,"Please enter place name in the above textbox and click on 'Enter Place' button")

sb1=Scrollbar(window)
sb1.grid(row=2,column=2,rowspan=4)

list1.configure(yscrollcommand=sb1.set)#defining vertcal scrollbar
sb1.configure(command=list1.yview)

sb2=Scrollbar(window,orient=HORIZONTAL)
sb2.grid(row=7,column=0,columnspan=2)

list1.configure(xscrollcommand=sb2.set)#defining horizontal scrollbar
sb2.configure(command=list1.xview)


b1=Button(window,text="Enter place",width=14,height=2,command=enter_place,bd=4,bg='#D3D3D3')
b1.grid(row=1,column=3)

b1=Button(window,text="Run",width=14,height=2,command=run_com,fg="green",activeforeground="blue",bd=4,bg='#D3D3D3')
b1.grid(row=2,column=3)

b1=Button(window,text="Today",width=14,height=2,command=choice_1a,activeforeground="blue",bd=4,bg='#D3D3D3')
b1.grid(row=3,column=3)

b1=Button(window,text="Hourly",width=14,height=2,command=choice_2a,activeforeground="blue",bd=4,bg='#D3D3D3')
b1.grid(row=4,column=3)

b1=Button(window,text="Monthly",width=14,height=2,command=choice_3a,activeforeground="blue",bd=4,bg='#D3D3D3')
b1.grid(row=5,column=3)

b1=Button(window,text="Ten-days",width=14,height=2,command=choice_4a,activeforeground="blue",bd=4,bg='#D3D3D3')
b1.grid(row=6,column=3)

b1=Button(window,text="Save JSON",width=14,height=2,command=jsonf,activebackground="blue",bd=4,bg='#D3D3D3')
b1.grid(row=7,column=3)

b1=Button(window,text="Close",width=14,height=2,command=window.destroy,activebackground="red",bd=4,bg='#D3D3D3')
b1.grid(row=8,column=3)

window.mainloop()
