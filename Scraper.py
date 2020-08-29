import time
import xlwt
import os
import tkinter
from tkinter import *
from xlwt import Workbook
from selenium import webdriver
import mysql.connector

class Locater: 
    def search(self,job_title,desired_location,sort_key,save_option):
        #Opening chrome browser in icognito mode
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")
        driver=webdriver.Chrome(options=options)
        #Searching in linkedin for given job title and location
        driver.get("https://www.linkedin.com/jobs/search?keywords="+job_title+"&location="+desired_location)
        
        #Give time for the web page to load before scraping 
        time.sleep(2)
        try:
            #Scraping the web page for job offer, company name, date of offer and link to the offer using XPath of each variable wanted 
            job_offer=driver.find_elements_by_xpath('//h3[@class="result-card__title job-result-card__title"]')
            company_name=driver.find_elements_by_xpath('//h4[@class="result-card__subtitle job-result-card__subtitle"]')
            offer_date=driver.find_elements_by_xpath('//time[@class="job-result-card__listdate"]')
            offer_link=driver.find_elements_by_xpath('//a[@class="result-card__full-card-link"]')
        except:
            #In case no current offers appear on the web page
            print("No jobs available")
        i=0
        #Lists to store data of each job offer
        name=[]
        offer=[]
        date=[]
        link=[]
        #Adding data of each job offer
        for i in range(len(offer_date)):
            name.append(company_name[i].text)
            offer.append(job_offer[i].text)
            #Getting desired HTML attribute rather than the text referred to by the HTML tag
            date.append(offer_date[i].get_attribute('datetime'))
            link.append(offer_link[i].get_attribute('href'))
        
        if(save_option=="Excel"):   
            self.excel(driver,offer_date, name, offer, date, link, sort_key)
        else:
            self.mySQL(driver,offer_date, name, offer, date, link, sort_key)
            
    def mySQL(self,driver,offer_date,name,offer,date,link,sort_key):
        #Create a database in MySQL
        mydb=mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="mydatabase")
        #Create a cursor for the database
        mycursor=mydb.cursor(buffered=True)
        #To have a new empty table on every run of script
        sql = "DROP TABLE IF EXISTS companies"
        mycursor.execute(sql)
        #To create the new table on every run
        #VARCHAR is used as string length is unknown so CHAR can't be used 
        mycursor.execute("CREATE TABLE companies (Name VARCHAR(255), Offer VARCHAR(255), Date VARCHAR(255), Rating VARCHAR(255), Review_Count VARCHAR(255), Link VARCHAR(255))")
        val=[]
        #Scraping ranking of each company with a retrieved job offer
        for i in range(len(offer_date)):
            driver.get("https://eg.indeed.com/companies")
            #Input company name in search bar then click search button
            driver.find_element_by_id('search-by-company-input').send_keys(name[i])
            driver.find_element_by_xpath('//button[@type="submit"]').click()
            try:
                rating=driver.find_element_by_xpath('//span[@itemprop="ratingValue"]').text
                number_of_reviews=driver.find_element_by_xpath('//*[@id="cmp-curated"]/div[3]/div[1]/a[2]/p').text
            except:
                #In case company has no rating on the web page
                rating='0 (Not specified)'
                number_of_reviews='0'
            print("Reviews:",number_of_reviews)
            #The query used to insert new rows in database
            sql = "INSERT INTO companies (Name, Offer, Date, Rating, Review_Count, Link) VALUES (%s, %s, %s, %s, %s, %s)"
            #Creating a nested list where each index is a different job offer with its seperate data
            val.append([])
            val[i].append(name[i]) 
            val[i].append(offer[i]) 
            val[i].append(date[i]) 
            val[i].append(rating+" Stars")
            val[i].append(number_of_reviews) 
            val[i].append(link[i])
        mycursor.executemany(sql, val)
        print(mycursor.rowcount," row")
        #Used to print the job offers stored in the database
        mydb.commit()
        mycursor.execute("SHOW TABLES")
        mycursor.execute("SELECT * FROM companies ORDER BY "+sort_key+" DESC")
        results=mycursor.fetchall()
        for x in results:
            print(x)
            
    def excel(self,driver,offer_date,name,offer,date,link,sort_key):
        #Opening new excel sheet and adding titles of columns 
        wb=Workbook()
        sheet1=wb.add_sheet('Sheet1')
        sheet1.write(0,0,'Company name')
        sheet1.write(0,1,'Job Offer')
        sheet1.write(0,2,'Date')
        sheet1.write(0,3,'Rating')
        sheet1.write(0,4,'Review Count')
        sheet1.write(0,5,'Link')
        val=[]
        for i in range(len(offer_date)):
            driver.get("https://eg.indeed.com/companies")
            #Input company name in search bar then click search button
            driver.find_element_by_id('search-by-company-input').send_keys(name[i])
            driver.find_element_by_xpath('//button[@type="submit"]').click()
            try:
                rating=driver.find_element_by_xpath('//span[@itemprop="ratingValue"]').text+" Stars"
                number_of_reviews=driver.find_element_by_xpath('//*[@id="cmp-curated"]/div[3]/div[1]/a[2]/p').text
            except:
                #In case company has no rating on the web page
                rating='0 (Not specified)'
                number_of_reviews='0'
            #Creating a nested list where each index is a different job offer with its seperate data
            val.append([])
            val[i].append(name[i]) 
            val[i].append(offer[i]) 
            val[i].append(date[i]) 
            val[i].append(rating)
            val[i].append(number_of_reviews) 
            val[i].append(link[i])
        if(sort_key=="Date"):
            #Sort according to third element in tuple of nested list which is the date of offer
            val.sort(key=lambda x: x[2], reverse=True)
        else:
            #Sort according to the fourth element in tuple of nested list which is the rating of company
            val.sort(key=lambda x: x[3], reverse=True)
        for i in range(len(offer_date)):
            #Write the retrieved data in opened excel sheet, each piece of data under its specific column
            sheet1.write(i+1,0,val[i][0])
            sheet1.write(i+1,1,val[i][1])
            sheet1.write(i+1,2,val[i][2])
            sheet1.write(i+1,3,val[i][3])
            sheet1.write(i+1,4,val[i][4])
            sheet1.write(i+1,5,val[i][5])
        #Saving the excel sheet then opening it to view the results
        wb.save("jobs.xls")
        #Open the saved excel sheet by looking for the file in current working directory
        os.startfile(os.getcwd()+"\\jobs.xls")  
                 
class GUI:
    def init(self):
        #Design of GUI        
        #Path of images used in place of labels and button        
        job_path=os.getcwd()+"\\job_button.png"  
        location_path=os.getcwd()+"\\location_button.png"  
        nextbutton_path=os.getcwd()+"\\next_button.png"  
        window=tkinter.Tk()
        #Position and size of window
        window.geometry("280x110+300+300")
        window.title('Job Scraper')
        #Linking tkinter with the images
        job_image=tkinter.PhotoImage(file=job_path)
        location_image=tkinter.PhotoImage(file=location_path)
        nextbutton_image=tkinter.PhotoImage(file=nextbutton_path)
        #Adding the images to labels
        Label(window,image=job_image).grid(row=0)
        Label(window,image=location_image).grid(row=1)
        the_job=Entry(window)
        the_job.grid(row=0,column=1)
        the_location=Entry(window)
        the_location.grid(row=1,column=1)
        #The button 'Next' that calls sort method upon clicking
        actual_button=Button(window,image=nextbutton_image,width=nextbutton_image.width(),border=0,command=(lambda:self.sort(window,the_job,the_location))).grid(row=2,column=0,columnspan=2)
        #To run the GUI
        window.mainloop()
        
    def sort(self,window,the_job,the_location):
        #Opening new window
        window1=tkinter.Toplevel(window)
        #Position of window
        window1.geometry("+300+300")
        window1.title('Job Scraper')
        #Frame to place radio buttons used in displaying sorting options
        radio_var=StringVar(window1)
        radio_var.set("Rating")
        sortbutton_path=os.getcwd()+"\\sort_button.png"
        ratingbutton_path=os.getcwd()+"\\rating_button.png"
        datebutton_path=os.getcwd()+"\\date_button.png"
        nextbutton_path=os.getcwd()+"\\next_button.png" 
        #Linking images to tkinter to be used on radio buttons
        sortbutton_image=tkinter.PhotoImage(file=sortbutton_path)
        ratingbutton_image=tkinter.PhotoImage(file=ratingbutton_path)
        datebutton_image=tkinter.PhotoImage(file=datebutton_path)
        nextbutton_image=tkinter.PhotoImage(file=nextbutton_path)
        #Creating radio buttons and label
        date_radiobutton=Radiobutton(window1,image=datebutton_image,variable=radio_var,value="Date").grid(row=1,column=1)
        rating_radiobutton=Radiobutton(window1,image=ratingbutton_image,variable=radio_var,value="Rating").grid(row=1,column=0)
        Label(window1,image=sortbutton_image).grid(row=0,columnspan=2)
        #The button 'Next' that calls save_place method upon clicking
        actual_button=Button(window1,image=nextbutton_image,width=nextbutton_image.width(),border=0,command=(lambda:self.save_place(window,radio_var,the_job,the_location))).grid(row=2,columnspan=2)
        window.mainloop()
        
    def save_place(self,window,radio_var,the_job,the_location):
        #Opening new window
        window2=tkinter.Toplevel(window)
        #Position of window
        window2.geometry("+300+300")
        window2.title('Job Scraper')
        #Frame to place radio buttons used in displaying saving options
        saving_var=StringVar(window2)
        saving_var.set("MySQL")
        search_path=os.getcwd()+"\\search_button.png"
        savebutton_path=os.getcwd()+"\\save_button.png"
        mysqlbutton_path=os.getcwd()+"\\mySQL_button.png"
        excelbutton_path=os.getcwd()+"\\excel_button.png"
        #Linking images to tkinter to be used on radio buttons
        search_image=tkinter.PhotoImage(file=search_path)
        savebutton_image=tkinter.PhotoImage(file=savebutton_path)
        mysqlbutton_image=tkinter.PhotoImage(file=mysqlbutton_path)
        excelbutton_image=tkinter.PhotoImage(file=excelbutton_path)
        #Creating radio buttons and label
        excel_radiobutton=Radiobutton(window2,image=excelbutton_image,variable=saving_var,value="Excel").grid(row=1,column=1)
        mySQL_radiobutton=Radiobutton(window2,image=mysqlbutton_image,variable=saving_var,value="MySQL").grid(row=1,column=0)
        Label(window2,image=savebutton_image).grid(row=0,columnspan=2)
        #Instantiating new Locater object
        locate=Locater()
        #Search button to use the inserted job,location,sorting type and saving type to run the search method in Locater object
        b=Button(window2,image=search_image,width=search_image.width(),border=0,command=(lambda:locate.search(the_job.get(), the_location.get(),radio_var.get(),saving_var.get())))
        b.grid(row=3,column=0,columnspan=2)
        window.mainloop()
        
#Instantiating new Gui object to start the bot
gui_window=GUI()
gui_window.init()
