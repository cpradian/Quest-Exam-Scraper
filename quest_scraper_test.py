# import necessary libraries 
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

def gather_exam_links(driver, exams):
    exam_links = {}

    # Extract each exam link
    for exam in exams:
        element = driver.find_element("xpath", f"//a[contains(text(), '{exam}')]")
        exam_link = element.get_attribute('href')
        exam_links[exam] = exam_link

    return exam_links

# specify  options
options = EdgeOptions()
options.use_chromium = True

# provide the path to the installed webdriver here:
webdriver_path = r"C:\Users\calvi\OneDrive\Documents\OnRamps\Report Download Script\OnRamps-Submission-Report-Automation\msedgedriver.exe"
driver = webdriver.Edge(executable_path=webdriver_path)


# read csv file to get list of quest links
# provide path to csv file w/ links here:
quest_links_path = r"C:\Users\calvi\OneDrive\Documents\OnRamps\Quest-Exam-Scraper\quest_links.csv"
dataset = pd.read_csv(quest_links_path)

# create array of text to search by to grab links of exams
exams = ['1A', '1B', '2A', '2B']

# create new columns based on exams
for new_col in exams:
    dataset[new_col] = ''

# Grab the course instructor names and urls and put them into arrays
instructors = dataset["Instructor"]
urls = dataset["Links"]


# do log in process
driver.get(urls[0])
# allow 30 seconds to complete login process
time.sleep(30) 
for i in range(2):
    print(instructors[i])
    # Go to target page
    driver.get(urls[i])
    # Wait for 3 seconds to fully load
    time.sleep(10)

    # Extract links for each of the exams 
    exam_links = gather_exam_links(driver, exams)
    print(exam_links)
    time.sleep(10)

    # Loop through each of the exam links and grab the question_id for slide 3
    for exam in exams:
        driver.get(exam_links[exam])
        time.sleep(10)
        question_id = driver.find_element("xpath", '/html/body/main/div/div[4]/div/div[2]/div[2]/div[2]/div/table/tbody/tr[3]/td[6]').text
        print(question_id)
        dataset.at[i, exam] = question_id
        time.sleep(10)

    print(dataset['1A'])
# Close the driver
driver.close()