# The following libraries are required to run this program. They provide the tools we need to interact with webpages and analyze data.
# Selenium is a powerful tool for controlling a web browser through the program. 
# It's used here to automate browser actions such as clicking buttons and navigating pages.
# Pandas is a data analysis library, and we're using it here to read a csv file.
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# This is a class definition for a "QuestScraper". A class is a blueprint for creating objects. 
# In this case, QuestScraper objects are capable of gathering exam links and retrieving question IDs from those links.
class QuestScraper:
    def __init__(self, driver):
        self.driver = driver

    # This method is used to gather links to exams. It searches for links that contain the specified exam names.
    def gather_exam_links(self, exams):
        exam_links = {}

        for exam in exams:
            try:
                # Find a link that contains the name of the exam and get its URL.
                element = self.driver.find_element("xpath", f"//a[contains(text(), '{exam}')]")
                exam_link = element.get_attribute('href')
                exam_links[exam] = exam_link
            except: 
                print("did not have " + exam)
        return exam_links

    # This method is used to retrieve the ID of a question from an exam link.
    def get_question_id(self, exam_link):
        try:
            self.driver.get(exam_link)
            time.sleep(15)  # Wait for the page to load.
            # Find the question ID on the page and get its text.
            question_id = self.driver.find_element("xpath", '/html/body/main/div/div[4]/div/div[2]/div[2]/div[2]/div/table/tbody/tr[3]/td[6]').text
            return question_id
        except:
            # If something goes wrong, wait 5 seconds and try again.
            time.sleep(5)
            self.get_question_id(exam_link)

# This is the main part of the program. It's where the high-level logic resides.
def main():
    # Set up Chrome options. These options can be used to customize the browser behavior.
    options = ChromeOptions()
    options.use_chromium = True

    # This is where you specify the location of the Chrome driver on your computer (only for Windows). 
    # The Chrome driver is a separate component that Selenium uses to control Chrome.
    webdriver_path = r"chromedriver"
    driver = webdriver.Chrome()

    # Specify the location of the csv file that contains quest links.
    quest_links_path = r"/Users/cbp847/Documents/GitHub/Quest-Exam-Scraper/phy1_quest_links.csv"
    # Read the csv file into a pandas DataFrame.
    dataset = pd.read_csv(quest_links_path)

    # These are the names of the exams to search for.
    exams = ['1M', '2M', '3M', '4M', '5M', '6M', '7M']

    # Add new columns to the DataFrame for each exam.
    for new_col in exams:
        dataset[new_col] = ''

    # Get the list of instructor names and urls from the DataFrame.
    instructors = dataset["Instructor"]
    urls = dataset["Links"]

    # Create a new QuestScraper object.
    scraper = QuestScraper(driver)

    # Navigate to the first URL and pause for 30 seconds to allow for manual login.
    driver.get(urls[0])
    time.sleep(30)
    
    # Loop over each instructor and URL.
    for i in range(len(instructors)):
        print(instructors[i])

        # Go to the URL for this instructor.
        driver.get(urls[i])

        # Wait for the page to load.
        time.sleep(15)

        # Gather the links for each exam.
        exam_links = scraper.gather_exam_links(exams)
        time.sleep(15)

        # Loop over each exam link and retrieve the question ID.
        for exam in exam_links.keys():
            question_id = scraper.get_question_id(exam_links[exam])
            dataset.at[i, exam] = question_id
            print(question_id)

        # Save the DataFrame to a csv file after each question ID is retrieved.
        # ** Specify the name of the CSV file here **
        dataset.to_csv('phy1_final_m3.csv', index=False)

    # Close the browser window.
    driver.close()


# This line checks if this script is being run directly (as opposed to being imported as a module).
# If the script is being run directly, it calls the main() function to start the program.
if __name__ == "__main__":
    main()
