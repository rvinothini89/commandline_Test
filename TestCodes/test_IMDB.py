import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from TestData.IMDBData import IMDB
from TestLocators.IMDBLocators import locators


class testIMDB:

    @pytest.fixture
    def booting_function(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 30)
        yield
        self.driver.close()

    def test_webPageAccess(self, booting_function):
        try:
            self.driver.get(IMDB.url)
            assert self.driver.title == IMDB.title
            print("Success, Able to retrieve web page title")
        except TimeoutException as e:
            print(e)

    def clickExpandAll(self,booting_function):
        try:
            # after loading need to scroll down the web page to enter details for fetching results
            self.driver.execute_script("window.scrollBy(0,500)", "")
            # Expanding all controls to enter data
            expand_button = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.expandAll)))
            expand_button.click()
        except TimeoutException as e:
            print(e)

    # Method to pass input for name field using explicit wait conditions
    def nameInput(self,booting_function):
        try:
            name = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.name_locator)))
            # Passing name value
            name.send_keys(IMDB.name)
        except TimeoutException as e:
            print(e)

    # Method to pass input for birthyear fields using explicit wait conditions
    def birthyear_range(self,booting_function):
        try:
            BdateFrom = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.birthdateFrom)))
            BdateTo = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.birthdateTo)))
            BdateFrom.send_keys(IMDB.birthyear_start)
            BdateTo.send_keys(IMDB.birthyear_end)
        except TimeoutException as e:
            print(e)

    # Method to pass input for birthday field using explicit wait conditions
    def birthday_input(self,booting_function):
        try:
            Bday = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.birthday)))
            Bday.send_keys(IMDB.birthday)
        except TimeoutException as e:
            print(e)

    # Method to select award options
    def awardOption_input(self,booting_function):
        try:
            # need to scroll down further to make the elements visible
            self.driver.execute_script("window.scrollBy(0,800)", "")
            # award options are not clickable with error "not scrolled as its not in view", so tried to execute javascript
            awardOptions = self.driver.find_element(By.XPATH, locators.awards)
            self.driver.execute_script("arguments[0].click();", awardOptions)
        except TimeoutException as e:
            print(e)

    # Method to select drop down option
    def topicOptionSelect(self,booting_function):
        try:
            # Tried with select class dint work, so used javascript to select the drop down value
            self.driver.execute_script("return document.getElementById('within-topic-dropdown-id').selectedIndex = '2'")
            # with javascript, it was changing to default option. so tried to trigger the change manually using dispatchEvent method
            self.driver.execute_script("""
                                   var select = document.getElementById('within-topic-dropdown-id');
                                   var event = new Event('change', { bubbles: true });
                                   select.dispatchEvent(event);
                               """)
        except TimeoutException as e:
            print(e)

    # Method for passing page topic values using explicit wait conditions
    def topicInputText(self,booting_function):
        try:
            tInput = self.wait.until(EC.presence_of_element_located((By.XPATH, locators.topic_input)))
            tInput.send_keys(IMDB.topic_input)
        except TimeoutException as e:
            print(e)

    # Method for fetching results by clicking on "See results button" using explicit wait condition
    def resultsClick(self,booting_function):
        try:
            resultsButton = self.wait.until(EC.element_to_be_clickable((By.XPATH, locators.results)))
            resultsButton.click()
            # Waiting for results to load and taking screenshot to verify the output
            self.wait.until(EC.presence_of_element_located((By.XPATH, locators.results_locator)))
            self.driver.save_screenshot("results.png")
        except TimeoutException as e:
            print(e)
