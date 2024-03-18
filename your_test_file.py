from appium import webdriver
from selenium.webdriver.common.by import By

def test_example():
    # Your test steps go here
    desired_caps = {
        'platformName': 'iOS',
        'platformVersion': '16.5',
        'udid': '00008101-00162DC22684001E',
        'bundleId': 'com.apple.mobiletimer',
        'automationName': 'XCUITest',
    }

    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps, options=None)

    element = driver.find_element(By.XPATH, "//XCUIElementTypePickerWheel[@value='10 minutes']")
    element.click()
