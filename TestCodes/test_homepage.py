from TestData.HomePageData import HomePage
from TestLocators.HomePageLocators import Locators
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pytest


class Test_Suman:

    @pytest.fixture
    # Booting function for running all the Python tests
    def booting_function(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        yield
        self.driver.close()

    def test_get_title(self):
        self.driver.get(HomePage().url)
        assert self.driver.title == HomePage().title
        print("SUCCESS : Web Page title is verified")

    def test_verify_url(self, booting_function):
        self.driver.get(HomePage().url)
        assert self.driver.current_url == HomePage().url
        print("SUCCESS : Home page URL verified")

    def test_login(self, booting_function):
        try:
            self.driver.get(HomePage().url)
            self.driver.find_element(by=By.NAME, value=Locators().username_input_box).send_keys(HomePage().username)
            self.driver.find_element(by=By.NAME, value=Locators().password_input_box).send_keys(HomePage().password)
            self.driver.find_element(by=By.NAME, value=Locators().submit_button).click()
            assert self.driver.current_url == HomePage().dashboard_url
            print("SUCCESS : Logged in with Username {a} and Password {b}".format(a=HomePage().username,
                                                                                  b=HomePage().password))
        except NoSuchElementException as e:
            print(e)
