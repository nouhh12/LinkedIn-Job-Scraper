                                        LinkedIn Job Scraper
User Manual:

Upon running the app a small GUI will open where the user will be prompted to insert the job title in the first text field and the desired location in the second text field. After typing in both fields the user should click on the 'Next' button displayed at the bottom of the GUI to proceed to next window.

In the next window, the user is given the option to choose by which type of data the information gathered should be sorted, either by Rating of Company or Date of Offer. The information will be sorted descendingly i.e: Highest Rating/Latest Offer first. After choosing the desired sorting type, user should click on the 'Next' button displayed at the bottom of the GUI to proceed to next window.

In this final window, the user is given the option to choose in which type of database the information should be stored in, either in MySQL or Microsoft Excel. Information will be stored in a sorted manner according to the previously chosen type. After deciding where the information should be saved, the user should click on 'Search' button to run the bot and start searching for job offers.

Logic:

Selenium Webdriver is used to search through LinkedIn job offers. First the driver opens google chrome and searches LinkedIn for the job title and location the user had typed in.

Once the page loads with all the available job offers, the driver is used again to retrieve the job_offer, company_name, offer_date and offer_link. All the information is looked for in the webpage by searching using relative XPath.

In the case that no offers are available for the user’s query then a text is displayed to inform the user. However, if the search returns back job offers then the information of these offers are stored in 4 lists, each piece of information under its specific list.

Proceeding from there, the Selenium driver is used yet again to open the website Indeed, where the company name of each offer we retrieved is sent to. This step is done to scrape the rating of the companies and number of reviews given to each company, which we then add with the rest of the data initially retrieved.

Finally, all gathered information is written and saved in either a MySQL table or a Microsoft Excel sheet consisting of 6 columns – Company name, Job Offer, Date of Offer, Rating, Number of Reviews, Link – while the rows depend on the number of jobs we found at the time of searching. If the user decides to save in Microsoft Excel the Excel sheet is saved and opened as the last step in the app.

Disclaimer: Total commits to project are much more, but due to an error while pushing the commit number decreased, so to check all the commits please take a look at the activity page found on project overview. Link: https://gitlab.com/nouh12/linkedin-job-scraper/activity
