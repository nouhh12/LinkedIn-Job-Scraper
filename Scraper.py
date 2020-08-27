import time
import xlwt
import os
import tkinter
from tkinter import *
from xlwt import Workbook
from selenium import webdriver
import mysql.connector
from email.mime import image

#Change path according to your desired place to save the excel sheet
path="C:\\Users\\Nouh\\Desktop"
os.chdir(path)
class Locater:
    def search(self,job_title,desired_location):
        #Opening new excel sheet and adding titles of columns 
        wb=Workbook()
        sheet1=wb.add_sheet('Sheet1')
        sheet1.write(0,0,'Company name')
        sheet1.write(0,1,'Job Offer')
        sheet1.write(0,2,'Date')
        sheet1.write(0,3,'Rating')
        sheet1.write(0,4,'Link')

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
        val=[]
        #Adding data of each job offer
        for i in range(len(offer_date)):
            name.append(company_name[i].text)
            offer.append(job_offer[i].text)
            #Getting desired HTML attribute rather than the text referred to by the HTML tag
            date.append(offer_date[i].get_attribute('datetime'))
            link.append(offer_link[i].get_attribute('href'))
        i=0
        #Create a database in MySQL
        mydb=mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="mydatabase")
        #Create a cursor for the database
        mycursor=mydb.cursor(buffered=True)
        #Scraping ranking of each company with a retrieved job offer
        for i in range(len(offer_date)):
            driver.get("https://eg.indeed.com/companies")
            #Input company name in search bar then click search button
            driver.find_element_by_id('search-by-company-input').send_keys(name[i])
            driver.find_element_by_xpath('//button[@type="submit"]').click()
            try:
                rating=driver.find_element_by_xpath('//span[@itemprop="ratingValue"]').text
            except:
                #In case company has no rating on the web page
                rating='Not specified'
            print ('Index:',i,'\nCompany name:',name[i],'\nJob Offer:',offer[i],'\nDate of Offer:',date[i],'\nThe link:',link[i],'\nCompany Rating:',rating,'\n')
            #The query used to insert new rows in database
            sql = "INSERT INTO companies (Name, Offer, Date, Rating, Link ) VALUES (%s, %s, %s, %s, %s)"
            #Creating a nested list where each index is a different job offer with its seperate data
            val.append([])
            val[i].append(name[i]) 
            val[i].append(offer[i]) 
            val[i].append(date[i]) 
            val[i].append(rating) 
            val[i].append(link[i])
            #Write the retrieved data in opened excel sheet, each piece of data under its specific column
            sheet1.write(i+1,0,name[i])
            sheet1.write(i+1,1,offer[i])
            sheet1.write(i+1,2,date[i])
            sheet1.write(i+1,3,rating)
            sheet1.write(i+1,4,link[i])
        print('All jobs have been displayed...')
        #Writing the nested list in rows in the database
        mycursor.executemany(sql, val)
        #print(mycursor.rowcount," row")
        #Used to print the job offers stored in the database
        mydb.commit()
        mycursor.execute("SHOW TABLES")
        mycursor.execute("SELECT * FROM companies")
        results=mycursor.fetchall()
        for x in results:
            print(x)
        #Saving the excel sheet then opening it to view the results
        wb.save("jobs.xls")
        os.startfile(path+"\\jobs.xls")

#Design of GUI window
#Path of images used in place of labels and button    
search_path="C:\\Users\\Nouh\\Desktop\\images\\search_button.png"    
job_path="C:\\Users\\Nouh\\Desktop\\images\\job_button.png"    
location_path="C:\\Users\\Nouh\\Desktop\\images\\location_button.png"    
window=tkinter.Tk()
window.title('Job Scraper')
#Linking tkinter with the images
search_image=tkinter.PhotoImage(file=search_path)
job_image=tkinter.PhotoImage(file=job_path)
location_image=tkinter.PhotoImage(file=location_path)
#Adding the images to labels
Label(window,image=job_image).grid(row=0)
Label(window,image=location_image).grid(row=1)
the_job=Entry(window)
the_job.grid(row=0,column=1)
the_location=Entry(window)
the_location.grid(row=1,column=1)
#Instantiating new Locater object
locate=Locater()
#Search button to use the inserted job and location to run the search method in Locater object
b=Button(window,image=search_image,width=search_image.width(),border=0,command=(lambda:locate.search(the_job.get(), the_location.get())))
b.grid(row=3,column=1)
#To run the GUI
window.mainloop()

            