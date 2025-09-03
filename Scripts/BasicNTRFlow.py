import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
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

# Appium Service
appium_service = AppiumService()

try:
    print("🚀 Attempting to start Appium server...")
    appium_service.start()
    print("✅ Appium server started successfully.")
    
    # Create the driver
    print("🔗 Attempting to create a connection with the device...")
    driver = webdriver.Remote('http://localhost:4723', options=UiAutomator2Options().load_capabilities(capabilities))
    print("✅ Connection created successfully!")
    
    # Wait for the app to load
    print("⏳ Waiting for 15 seconds to allow the app to fully load...")
    time.sleep(15)
    
    # Step 1: Type the phone number one digit at a time
    phone_number = '4132300000'
    print(f"📱 Typing the number '{phone_number}' one digit at a time...")
    
    for digit in phone_number:
        button = driver.find_element(by=AppiumBy.XPATH, value=f'//android.widget.Button[@text="{digit}"]')
        button.click()
        print(f"✅ Clicked button '{digit}'.")
        time.sleep(1) # Short delay between clicks

    print("✅ Phone number typing completed.")
    
    # Step 2: Click the "OK" button
    print("🔍 Looking for the 'OK' button...")
    ok_button = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.Button[@text="OK"]')
    ok_button.click()
    print("✅ 'OK' button clicked successfully.")

    # Step 3: Wait for 5 seconds after the OK button is clicked
    print("⏳ Waiting for 5 seconds...")
    time.sleep(5)
    
    # Step 4: Click on the "Clip it!" button using its resource ID
    print("🔍 Looking for the 'Clip it!' button by its Resource ID...")
    clip_button = driver.find_element(by=AppiumBy.ID, value='com.appcard.androidterminal:id/view_featured_clip')
    clip_button.click()
    print("✅ 'Clip it!' button clicked successfully.")

    # Final wait to observe the result
    time.sleep(5)

except Exception as e:
    print(f"❌ An error occurred: {e}")
    print("\n--- Stacktrace ---")
    import traceback
    traceback.print_exc()

finally:
    if 'driver' in locals():
        print("🔌 Closing the driver...")
        driver.quit()
    
    print("👋 Shutting down Appium server...")
    appium_service.stop()
    print("✅ Appium server shut down successfully. Automation process finished.")