import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import os

CURRENT_FILE = os.path.basename(__file__)

class DeviceActions:
    """Performs actions and validations on the device."""

    def __init__(self, appium_url='http://localhost:4723'):
        self.appium_url = appium_url
        self.driver = None

    def connect(self, capabilities):
        """Connects to the device with the given capabilities."""
        print(f"🔗 Attempting to connect to the device... (from {CURRENT_FILE})")
        options = UiAutomator2Options().load_capabilities(capabilities)
        self.driver = webdriver.Remote(self.appium_url, options=options)
        print(f"✅ Connection established. (from {CURRENT_FILE})")

    def enter_phone_number(self, phone_number):
        """Types a phone number one digit at a time."""
        print(f"📱 Entering phone number: {phone_number} (from {CURRENT_FILE})")
        for digit in phone_number:
            button = self.driver.find_element(by=AppiumBy.XPATH, value=f'//android.widget.Button[@text="{digit}"]')
            button.click()
            time.sleep(0.5)
        print(f"✅ Phone number entered successfully. (from {CURRENT_FILE})")

    def click_button_by_text(self, text):
        """Finds and clicks a button by its text."""
        print(f"🖱️ Clicking button with text: '{text}' (from {CURRENT_FILE})")
        button = self.driver.find_element(by=AppiumBy.XPATH, value=f'//android.widget.Button[@text="{text}"]')
        button.click()
        print(f"✅ Button '{text}' clicked. (from {CURRENT_FILE})")

    def wait_for_element_and_click(self, locator_type, locator_value, timeout=10, expected_text=None):
        """
        Waits for an element to be present, validates its text (if provided), and clicks it.
        This method is designed to prevent Stale Element exceptions.
        """
        print(f"⏳ Waiting for element: {locator_value} (from {CURRENT_FILE})")
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(EC.presence_of_element_located((locator_type, locator_value)))

        if expected_text:
            print(f"🔍 Validating text on element. Expected: '{expected_text}', Found: '{element.text}' (from {CURRENT_FILE})")
            assert element.text == expected_text, f"Element text mismatch. Expected '{expected_text}' but found '{element.text}'."
            print(f"✅ Validation successful: Text is correct. (from {CURRENT_FILE})")

        print(f"🖱️ Clicking the element... (from {CURRENT_FILE})")
        element.click()
        print(f"✅ Element found and clicked. (from {CURRENT_FILE})")
        return element

    def is_text_present(self, text, timeout=10):
        """Checks if a specific text is displayed on the screen."""
        print(f"🔍 Validating text: '{text}' (from {CURRENT_FILE})")
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, f'//*[contains(@text, "{text}")]')))
            if element.is_displayed():
                print(f"✅ Validation successful: '{text}' is displayed. (from {CURRENT_FILE})")
                return True
        except Exception:
            print(f"❌ Validation failed: '{text}' is not displayed. (from {CURRENT_FILE})")
            return False
        return False

    def validate_element_by_id(self, resource_id, timeout=10):
        """
        Waits for an element with a specific resource ID to be present and visible.
        This is a robust method to validate an element's existence.
        """
        print(f"🔍 Validating element by resource ID: {resource_id} (from {CURRENT_FILE})")
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located((AppiumBy.ID, resource_id)))
            print(f"✅ Validation successful: Element with ID '{resource_id}' is present. (from {CURRENT_FILE})")
            return True
        except Exception as e:
            print(f"❌ Validation failed: Element with ID '{resource_id}' is not present. (from {CURRENT_FILE})")
            raise Exception(f"Element with ID '{resource_id}' was not found: {e}")

    def validate_element_id_and_text(self, resource_id, expected_text, timeout=10):
        """
        Waits for an element by ID, then validates its text.
        """
        print(f"🔍 Validating element ID and text: ID='{resource_id}', Text='{expected_text}' (from {CURRENT_FILE})")
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located((AppiumBy.ID, resource_id)))
            
            # Now validate the text of the found element
            if element.text == expected_text:
                print(f"✅ Validation successful: ID '{resource_id}' and text '{expected_text}' both match. (from {CURRENT_FILE})")
                return True
            else:
                print(f"❌ Validation failed: Text mismatch. Expected '{expected_text}' but found '{element.text}'. (from {CURRENT_FILE})")
                return False
        except Exception as e:
            print(f"❌ Validation failed: Element with ID '{resource_id}' was not found. (from {CURRENT_FILE})")
            raise Exception(f"Element with ID '{resource_id}' not found or text validation failed: {e}")

    def validate_element_and_clickable(self, resource_id, timeout=10):
        """
        Waits for an element with a specific resource ID to be clickable.
        """
        print(f"🔍 Validating if element with ID '{resource_id}' is clickable. (from {CURRENT_FILE})")
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.element_to_be_clickable((AppiumBy.ID, resource_id)))
            print(f"✅ Validation successful: Element with ID '{resource_id}' is clickable. (from {CURRENT_FILE})")
            return True
        except Exception as e:
            print(f"❌ Validation failed: Element with ID '{resource_id}' is not clickable. (from {CURRENT_FILE})")
            raise Exception(f"Element with ID '{resource_id}' was not clickable: {e}")

    def enter_text_by_xpath(self, xpath, text, timeout=10):
        """Waits for a text field by XPATH and enters text."""
        print(f"📝 Waiting for text field with XPATH: '{xpath}' to enter text: '{text}' (from {CURRENT_FILE})")
        wait = WebDriverWait(self.driver, timeout)
        try:
            text_field = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
            text_field.send_keys(text)
            print(f"✅ Text entered successfully. (from {CURRENT_FILE})")
        except TimeoutException:
            raise NoSuchElementException(f"Timed out waiting for element with XPATH: {xpath}")

    def click_by_id_or_text(self, resource_id=None, text=None, timeout=10):
        """Finds and clicks an element by ID or text."""
        wait = WebDriverWait(self.driver, timeout)
        try:
            if resource_id:
                print(f"🖱️ Clicking element with ID: '{resource_id}' (from {CURRENT_FILE})")
                element = wait.until(EC.element_to_be_clickable((AppiumBy.ID, resource_id)))
            elif text:
                print(f"🖱️ Clicking element with text: '{text}' (from {CURRENT_FILE})")
                element = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, f'//android.widget.Button[@text="{text}"]')))
            else:
                raise ValueError("Must provide either a resource_id or text.")
            
            element.click()
            print(f"✅ Element clicked successfully. (from {CURRENT_FILE})")
        except TimeoutException:
            if resource_id:
                raise NoSuchElementException(f"Timed out waiting for element with ID: {resource_id}")
            else:
                raise NoSuchElementException(f"Timed out waiting for element with text: {text}")

    def quit(self):
        """Quits the driver session."""
        if self.driver:
            print(f"🔌 Closing the driver session... (from {CURRENT_FILE})")
            self.driver.quit()
            print(f"✅ Driver session closed. (from {CURRENT_FILE})")
