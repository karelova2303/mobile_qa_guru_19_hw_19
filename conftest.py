import os

import allure
import allure_commons
import pytest

from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from appium import webdriver

from selene import browser, support

import config
from mobile_hw_19 import utils


@pytest.fixture(scope='function', params=['android', 'ios'])
def mobile(request):
    if request.param == 'android':
        options = UiAutomator2Options().load_capabilities({
            # Specify device and os_version for testing
            "platformName": 'android',
            "platformVersion": '13.0',
            "deviceName": 'Google Pixel 7 Pro',

            # Set URL of the application under test
            "app": "bs://sample.app",

            # Set other BrowserStack capabilities
            'bstack:options': {
                "projectName": "Android tests",
                "buildName": "browserstack-build-1",

                # Set your access credentials
                "userName": config.user_name,
                "accessKey": config.access_key
            }
        }
        )

    if request.param == 'ios':
        options = XCUITestOptions().load_capabilities({
            # Specify device and os_version for testing
            "platformName": "ios",
            "platformVersion": "17",
            "deviceName": "iPhone 15 Pro Max",

            # Set URL of the application under test
            "app": "bs://sample.app",

            # Set other BrowserStack capabilities
            'bstack:options': {
                "projectName": "IOS tests",
                "buildName": "browserstack-build-1",

                # Set your access credentials
                "userName": config.user_name,
                "accessKey": config.access_key
            }
        }
        )
    with allure.step('init app session'):
        browser.config.driver = webdriver.Remote(
            config.driver_remote_url,
            options=options)

    browser.config.timeout = float(os.getenv('timeout', '10.0'))

    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )

    yield

    utils.allure.attach_bstack_screenshot()
    utils.allure.attach_bstack_page_source()

    session_id = browser.driver.session_id

    with allure.step('tear down app session'):
        browser.quit()

    utils.allure.attach_bstack_video(session_id)


ios = pytest.mark.parametrize('mobile', ['ios'], indirect=True)
android = pytest.mark.parametrize('mobile', ['android'], indirect=True)
