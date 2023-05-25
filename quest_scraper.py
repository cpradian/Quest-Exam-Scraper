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
    options = EdgeOptions()
    options.use_chromium = True

    # provide the path to the installed webdriver here:
    webdriver_path = r"C:\Users\calvi\OneDrive\Documents\OnRamps\Report Download Script\OnRamps-Submission-Report-Automation\msedgedriver.exe"
    driver = webdriver.Edge(executable_path=webdriver_path)

    # read csv file to get list of quest links
    # provide path to csv file w/ links here:
    quest_links_path = r"C:\Users\calvi\OneDrive\Documents\OnRamps\Quest-Exam-Scraper\quest_links.csv"
    dataset = pd.read_csv(quest_links_path)

    # Create array of text to search by to grab links of exams
    exams = ['1A', '1B', '2A', '2B', '3A', '3B', '4A', '4B', '5A', '5B', '6A', '6B', '7A', '7B',
             'Final A (Part 1)', 'Final A (Part 2)', 'Final B (Part 1)', 'Final B (Part 2)',
             'Final A 22-23', 'Final B 22-23']

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

    # Loop through each instructor and url
    for i in range(4):
        print(instructors[i])

        # Go to the target page
        driver.get(urls[i])

        # Wait for 3 seconds to fully load
        time.sleep(15)

        # Extract links for each of the exams
        exam_links = scraper.gather_exam_links(exams)
        time.sleep(15)

        # Loop through each of the exam links and grab the question_id for slide 3 (Q1)
        for exam in exam_links.keys():
            question_id = scraper.get_question_id(exam_links[exam])
            dataset.at[i, exam] = question_id
            print(question_id)
            

    # Close the driver
    driver.close()

    dataset.to_csv('new_output.csv', index=False)


if __name__ == "__main__":
    main()
