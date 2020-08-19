import time
from selenium import webdriver

class Locater:
    def search(self,job_title,desired_location):
        looking_for=job_title
        location=desired_location
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")
        driver=webdriver.Chrome(options=options)
        driver.get("https://www.linkedin.com/jobs/search?keywords="+looking_for+"&location="+location)
        time.sleep(5)
        job_offer=driver.find_elements_by_xpath('//h3[@class="result-card__title job-result-card__title"]')
        company_name=driver.find_elements_by_xpath('//h4[@class="result-card__subtitle job-result-card__subtitle"]')
        offer_date=driver.find_elements_by_xpath('//time[@class="job-result-card__listdate"]')
        offer_link=driver.find_elements_by_xpath('//a[@class="result-card__full-card-link"]')
        i=0
        for i in range(len(offer_date)):
            name=company_name[i].text
            offer=job_offer[i].text
            date=offer_date[i].get_attribute('datetime')
            link=offer_link[i].get_attribute('href')
            print ('Company name:',name,'\nJob Offer:',offer,'\nDate of Offer:',date,'\nThe link:',link,'\n\n')
            i+=1
        print('All jobs have been displayed...')

job_title=input("Insert job title desired:")
desired_location=input("Insert location desired:")
Locater().search(job_title,desired_location)
            