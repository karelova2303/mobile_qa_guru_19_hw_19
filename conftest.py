import os

import allure
import allure_commons
import pytest

from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from appium import webdriver

from selene import browser, support

import config


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

    allure.attach(
        browser.driver.get_screenshot_as_png(),
        name='screenshot',
        attachment_type=allure.attachment_type.PNG,
    )

    allure.attach(
        browser.driver.page_source,
        name='screen xml dump',
        attachment_type=allure.attachment_type.XML,
    )

    session_id = browser.driver.session_id

    with allure.step('tear down app session'):
        browser.quit()

    import requests
    bstack_session = requests.get(
        f'https://api.browserstack.com/app-automate/sessions/{session_id}.json',
        auth=(config.user_name, config.access_key),
    ).json()
    video_url = bstack_session['automation_session']['video_url']

    allure.attach(
        '<html><body>'
        '<video width="100%" height="100%" controls autoplay>'
        f'<source src="{video_url}" type="video/mp4">'
        '</video>'
        '</body></html>',
        name='video_recording',
        attachment_type=allure.attachment_type.HTML,
    )


ios = pytest.mark.parametrize('mobile', ['ios'], indirect=True)
android = pytest.mark.parametrize('mobile', ['android'], indirect=True)
