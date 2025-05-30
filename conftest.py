import os

import allure
import allure_commons
import pytest

from appium.options.android import UiAutomator2Options
from appium import webdriver

from selene import browser, support

import config
from mobile_hw_19 import utils


@pytest.fixture(scope='function')
def mobile():
    options = UiAutomator2Options().load_capabilities({
        # Specify device and os_version for testing
        "platformName": 'Android',
        "deviceName": 'Pixel_8',
        "appWaitActivity": 'org.wikipedia.*',

        # Set URL of the application under test
        "app": 'D:/Mobile/wikipedia/app-alpha-universal-release.apk',
    }
    )

    with allure.step('init app session'):
        browser.config.driver = webdriver.Remote(
            'http://127.0.0.1:4723',
            options=options)

    browser.config.timeout = float(os.getenv('timeout', '10.0'))

    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )

    yield

    utils.allure.attach_bstack_screenshot()
    utils.allure.attach_bstack_page_source()

    # session_id = browser.driver.session_id

    with allure.step('tear down app session'):
        browser.quit()


