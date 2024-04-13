import os
import requests
from behave import given, when, then

# import logging
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select, WebDriverWait
# from selenium.webdriver.support import expected_conditions

# @given(u'the following recommendations')
# def step_impl(context):
#     raise NotImplementedError(u'STEP: Given the following recommendations')

@given('the server is started')
def step_impl(context):
    context.base_url = os.getenv(
        'BASE_URL', 
        'http://localhost:8000'
    )
    context.resp = requests.get(context.base_url + '/')
    assert context.resp.status_code == 200

@when('I visit the "home page"')
def step_impl(context):
    context.driver.get(context.base_url)
    
@then('I should see "{message}" in the title')
def step_impl(context, message):
    """ Check the document title for a message """
    assert(message in context.driver.title)

@then('I should not see "{text_string}"')
def step_impl(context, text_string):
    element = context.driver.find_element(By.TAG_NAME, 'body')
    assert(text_string not in element.text)

@when('I press the "{button}" button')
def step_impl(context, button):
    button_id = button.lower() + '-btn'
    context.driver.find_element(By.ID, button_id).click()

@then('I should see "{name}" in the results')
def step_impl(context, name):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'search_results'),
            name
        )
    )
    assert(found)

@then('I should not see "{name}" in the results')
def step_impl(context, name):
    element = context.driver.find_element(By.ID, 'search_results')
    assert(name not in element.text)

@then('I should see the message "{message}"')
def step_impl(context, message):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'flash_message'),
            message
        )
    )
    assert(found)