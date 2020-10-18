from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

#setup chromedriver
driver = webdriver.Chrome(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("start-maximized");
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
df = pd.DataFrame(columns=["Title","Location","Company","Salary","Sponsored","Description"])
for i in range(0,45):

	#step 1: get the page
	driver.get("https://www.indeed.co.in/jobs?q=ui+ux+designer&l=India&start="+str(i))
	driver.implicitly_wait(4)

	all_jobs = driver.find_elements_by_class_name('result')

	for job in all_jobs:
		result_html = job.get_attribute('innerHTML')
		soup = BeautifulSoup(result_html,'html.parser')
		try:
			title = soup.find("a",class_="jobtitle").text.replace('\n','')	
		except:
			title = 'None'
		try:
			location = soup.find(class_="location").text	
		except:
			location = 'None'
		try:
			company = soup.find(class_="company").text.replace('\n','').strip()	
		except:
			company = 'None'
		try:
			salary = soup.find(class_="salary").text.replace('\n','').strip()	
		except:
			salary = "0"
		try:
			sponsored = soup.find(class_="sponsoredGray").text	
			sponsored = "Sponsored"
		except:
			sponsored = 'Organic'
		sum_div = job.find_element_by_xpath('./div[3]')
		try:
			sum_div.click()
		except:
			close_button = driver.find_elements_by_class_name('popover-x-button-close')[0]
			close_button.click()
			sum_div.click()
		try:	
			job_desc = driver.find_element_by_id('vjs-desc').text
		except:
			job_desc = 'None'
		df = df.append({
			'Title':title,
			'Location':location,
			'Company':company,
			'Salary' :salary,
			'Sponsored':sponsored,
			'Description':job_desc
			},ignore_index=True)
		print(df.shape," results received")	
df.to_csv("./data/indeed-ui-ux-designer-india.csv",index = False)

