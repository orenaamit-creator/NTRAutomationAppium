import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.appium_service import AppiumService

print("🛠️ Starting automation process...")

# Desired Capabilities
capabilities = {
    'platformName': 'Android',
    'automationName': 'UiAutomator2',
    'deviceName': 'CAA25040001',
    'appPackage': 'com.appcard.androidterminal',
    'appActivity': 'com.appcard.androidterminal.ui.MainActivity',
    'appWaitActivity': 'com.appcard.androidterminal.ui.MainActivity',
    'noReset': False,
    'fullReset': False
}

print(f"📄 Capabilities set: {capabilities}")

appium_service = AppiumService()
driver = None
action_results = {}
error_message = None

try:
    print("🚀 Attempting to start Appium server and connect to device...")
    appium_service.start()
    driver = webdriver.Remote('http://localhost:4723', options=UiAutomator2Options().load_capabilities(capabilities))
    action_results['Connection & App Launch'] = '✅ Success'
    print("✅ Connection created successfully!")
    
    print("⏳ Waiting for 20 seconds to allow the app to fully load...")
    time.sleep(20)

    # First Validation
    print("🔍 Validating: Checking for 'Español' text on the screen...")
    wait = WebDriverWait(driver, 10)
    espanol_text = wait.until(
        EC.presence_of_element_located((AppiumBy.XPATH, '//*[contains(@text, "Español")]'))
    )
    if espanol_text.is_displayed():
        action_results['First screen validation (Español text)'] = '✅ Success'
        print("✅ Validation successful: 'Español' text is displayed.")
    else:
        raise Exception("Validation Failed: 'Español' text is not displayed.")

    # Step 1: Type the phone number
    phone_number = '4132300000'
    print(f"📱 Typing the phone number '{phone_number}' one digit at a time...")
    for digit in phone_number:
        print(f"   🔍 Finding and clicking button '{digit}'...")
        button = driver.find_element(by=AppiumBy.XPATH, value=f'//android.widget.Button[@text="{digit}"]')
        button.click()
        print(f"   ✅ Successfully clicked button '{digit}'.")
        time.sleep(0.5)
    action_results['Enter Phone Number'] = '✅ Success'
    
    # Step 2: Click the "OK" button
    print("🔍 Finding and clicking 'OK' button...")
    ok_button = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.Button[@text="OK"]')
    ok_button.click()
    action_results['Click OK Button'] = '✅ Success'
    print("✅ 'OK' button clicked successfully.")
    
    # Step 3: Wait for the "Clip it!" button
    print("⏳ Waiting for the 'Clip it!' button to appear (max 10 seconds)...")
    wait = WebDriverWait(driver, 10)
    clip_button = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.appcard.androidterminal:id/view_featured_clip'))
    )
    
    # Step 4: Click the "Clip it!" button with Text Validation
    print("🔍 Validating 'Clip it!' button text...")
    
    # Check if the text of the found element is what we expect
    assert clip_button.text == "Clip it!", f"Expected button text to be 'Clip it!' but found '{clip_button.text}'."
    
    print("✅ Validation successful: Button text is correct. Clicking it now...")
    clip_button.click()
    action_results['Click Clip it! Button'] = '✅ Success'
    print("✅ 'Clip it!' button clicked successfully.")

    time.sleep(5)

except Exception as e:
    error_message = str(e)
    # Register failure for the last attempted action
    if 'Connection & App Launch' not in action_results:
        action_results['Connection & App Launch'] = '❌ Failure'
    elif 'First screen validation (Español text)' not in action_results:
        action_results['First screen validation (Español text)'] = '❌ Failure'
    elif 'Enter Phone Number' not in action_results:
        action_results['Enter Phone Number'] = '❌ Failure'
    elif 'Click OK Button' not in action_results:
        action_results['Click OK Button'] = '❌ Failure'
    elif 'Click Clip it! Button' not in action_results:
        action_results['Click Clip it! Button'] = '❌ Failure'
    
finally:
    if driver:
        print("🔌 Closing the driver...")
        driver.quit()
    
    print("👋 Shutting down Appium server...")
    appium_service.stop()
    
    # Print execution summary
    print("\n--- Script Execution Summary ---")
    for action, result in action_results.items():
        print(f"{result} {action}")
    
    if error_message:
        print(f"\n🛑 Execution finished with an error: {error_message}")
    else:
        print("\n🎉 Execution completed successfully, without errors.")