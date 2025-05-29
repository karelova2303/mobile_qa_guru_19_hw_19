from allure_commons._allure import step
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have

from conftest import ios, mobile


@ios
def test_input_text_ios(mobile):
    text_to_input = 'Hello,world!'

    with step('Click on Text button'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Text Button")).click()

    with step(f'Type {text_to_input}'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Text Input")).send_keys(
            text_to_input + "\n")

    with step('Verify text'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Text Output")).should(
            have.exact_text(text_to_input)
        )
