# import necessary libraries 
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

class QuestScraper:
    def __init__(self, driver):
        self.driver = driver

    def gather_exam_links(self, exams):
        exam_links = {}

        for exam in exams:
            try:
                element = self.driver.find_element("xpath", f"//a[contains(text(), '{exam}')]")
                exam_link = element.get_attribute('href')
                exam_links[exam] = exam_link
            except: 
                print("did not have " + exam)
        return exam_links

    def get_question_id(self, exam_link):
        try:
            self.driver.get(exam_link)
            time.sleep(15)
            question_id = self.driver.find_element("xpath", '/html/body/main/div/div[4]/div/div[2]/div[2]/div[2]/div/table/tbody/tr[3]/td[6]').text

            return question_id
        except:
            time.sleep(5)
            self.get_question_id(exam_link)


def main():
    # specify options
    options = ChromeOptions()
    options.use_chromium = True

    # provide the path to the installed webdriver here:
    webdriver_path = r"chromedriver"
    driver = webdriver.Chrome()

    # read csv file to get list of quest links
    # provide path to csv file w/ links here:
    quest_links_path = r"/Users/cbp847/Documents/GitHub/Quest-Exam-Scraper/phy1_quest_links.csv"
    dataset = pd.read_csv(quest_links_path)

    # Create array of text to search by to grab links of exams
    exams = ['1M', '2M', '3M', '4M', '5M', '6M', '7M']

    # Create new columns based on exams array
    for new_col in exams:
        dataset[new_col] = ''

    # Grab the course instructor names and urls and put them into arrays
    instructors = dataset["Instructor"]
    urls = dataset["Links"]

    # Create a scraper object
    scraper = QuestScraper(driver)

    # Do log in process
    driver.get(urls[0])
    # Allow 30 seconds to complete login process
    time.sleep(30)
    
    # Open the CSV file for writing
    with open('phy1_final_m.csv', 'w') as file:
        # Write the header row
        file.write(','.join(dataset.columns) + '\n')

        # Loop through each instructor and url
        for i in range(len(instructors)):
            print(instructors[i])

            # Go to the target page
            driver.get(urls[i])

            # Wait for 15 seconds to fully load
            time.sleep(15)

            # Extract links for each of the exams
            exam_links = scraper.gather_exam_links(exams)
            time.sleep(15)

            # Loop through each of the exam links and grab the question_id for slide 3 (Q1)
            for exam in exam_links.keys():
                question_id = scraper.get_question_id(exam_links[exam])
                dataset.at[i, exam] = question_id
                print(question_id)

            # Write the row to the CSV file
            file.write(','.join(dataset.loc[i].astype(str)) + '\n') 

    # Close the driver
    driver.close()

    # dataset.to_csv('phy1_final_m.csv', index=False)


if __name__ == "__main__":
    main()
