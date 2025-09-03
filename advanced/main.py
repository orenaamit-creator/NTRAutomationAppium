import time
from appium.webdriver.common.appiumby import AppiumBy
from appium_manager import AppiumManager
from device_actions import DeviceActions
import os

CURRENT_FILE = os.path.basename(__file__)
PHONE_NUMBER_FILE = "last_phone.txt"
INITIAL_PHONE_NUMBER = 4066720000

def get_and_update_phone_number():
    """
    Reads the last phone number from a file, increments it by 1,
    and saves the new number back to the file.
    Returns the new phone number as a string.
    """
    phone_number = 0
    # Check if the file exists
    if os.path.exists(PHONE_NUMBER_FILE):
        with open(PHONE_NUMBER_FILE, 'r') as f:
            try:
                phone_number = int(f.read().strip())
                print(f"Reading last phone number from file: {phone_number}")
            except (ValueError, FileNotFoundError):
                print("Error reading phone number from file. Using initial number.")
                phone_number = INITIAL_PHONE_NUMBER
    else:
        print("Phone number file not found. Using initial number.")
        phone_number = INITIAL_PHONE_NUMBER
    
    # Increment the phone number
    new_phone_number = phone_number + 1
    
    # Save the new phone number to the file
    with open(PHONE_NUMBER_FILE, 'w') as f:
        f.write(str(new_phone_number))
        
    return str(new_phone_number)

if __name__ == "__main__":
    appium_manager = AppiumManager()
    device_actions = DeviceActions()
    action_results = {}
    error_message = None

    print(f"🛠️ Starting automation process from {CURRENT_FILE}")

    try:
        # Step 1: Start Appium Server
        appium_manager.start_server()

        # Step 2: Define Capabilities and Connect
        capabilities = {
            'platformName': 'Android',
            'automationName': 'UiAutomator2',
            'deviceName': 'CAA25040001',
            'appPackage': 'com.appcard.androidterminal',
            'appActivity': 'com.appcard.androidterminal.ui.MainActivity',
            'appWaitActivity': 'com.appcard.androidterminal.ui.MainActivity',
            'noReset': False,
            'fullReset': False,
            'uiautomator2ServerInstallTimeout': 60000
        }
        device_actions.connect(capabilities)
        action_results['Connection & App Launch'] = '✅ Success'

        print(f"⏳ Waiting for 20 seconds for the app to load... (from {CURRENT_FILE})")
        time.sleep(20)

        # Step 3: Sanity Check - Verify 'Esp' text
        if not device_actions.is_text_present("Esp"):
            raise Exception("Validation Failed: 'Esp' text is not displayed.")
        action_results['First screen validation (Esp text)'] = '✅ Success'

        # Step 4: Validate the main header element by resource ID
        print(f"\n✨ Step 4: Validating the main header element by resource ID...")
        header_id = "com.appcard.androidterminal:id/activity_main_header"
        device_actions.validate_element_by_id(header_id)
        action_results['Header ID Validation'] = '✅ Success'
        
        # Step 5: Validate the phone number input field's ID and text
        print(f"\n📝 Step 5: Validating the phone number input field...")
        phone_number_field_id = "com.appcard.androidterminal:id/view_welcome_phone_number_empty"
        expected_text = "Enter your mobile #"
        device_actions.validate_element_id_and_text(phone_number_field_id, expected_text)
        action_results['Phone Number Field Validation'] = '✅ Success'

        # Step 6: Validate Terms and Privacy Policy links
        print(f"\n🔗 Step 6: Validating 'Terms of Service' and 'Privacy Policy' links...")
        
        # Validate Terms of Service link
        terms_id = "com.appcard.androidterminal:id/tv_terms"
        device_actions.validate_element_and_clickable(terms_id)
        action_results['Terms Link Validation'] = '✅ Success'
        
        # Validate Privacy Policy link
        privacy_id = "com.appcard.androidterminal:id/tv_privacy_policy"
        device_actions.validate_element_and_clickable(privacy_id)
        action_results['Privacy Link Validation'] = '✅ Success'

        # Step 7: Enter phone number from file
        test_phone_number = get_and_update_phone_number()
        print(f"\n📱 Step 7: Entering phone number: {test_phone_number}")
        device_actions.enter_phone_number(test_phone_number)
        action_results['Enter Phone Number'] = '✅ Success'

        # Step 8: Click 'OK' button
        device_actions.click_button_by_text('OK')
        action_results['Click OK Button'] = '✅ Success'
        
        # Step 9: Wait and click 'Confirm' button
        print(f"\n⏳ Step 9: Waiting for 'Confirm' button...")
        device_actions.click_by_id_or_text(text="Confirm")
        action_results['Click Confirm Button'] = '✅ Success'
        
        # Step 10: Wait, enter email, and click confirm
        print(f"\n⏳ Step 10: Waiting for the email screen...")
        
        # Enter the generated email address
        email_xpath = '//android.widget.EditText[@text="Enter E-mail Address"]'
        generated_email = f"orena+{test_phone_number}@appcard.com"
        device_actions.enter_text_by_xpath(email_xpath, generated_email)
        action_results['Enter Email Address'] = '✅ Success'

        # Wait 2 seconds
        print(f"⏳ Waiting 2 seconds after entering email...")
        time.sleep(2)
        
        # Click the confirm button for the email field
        confirm_email_button_id = "com.appcard.androidterminal:id/view_email_confirm"
        device_actions.click_by_id_or_text(resource_id=confirm_email_button_id)
        action_results['Click Email Confirm Button'] = '✅ Success'
        
        # Wait 3 seconds
        print(f"⏳ Waiting 3 seconds after clicking confirm...")
        time.sleep(3)
        
        # Step 11: Enter name and click confirm
        print(f"\n⏳ Step 11: Waiting for the name screen...")
        
        # Enter first name with dynamic phone number
        first_name_xpath = '//android.widget.EditText[@text="First name"]'
        first_name_text = f"ORENTHEKING{test_phone_number}"
        device_actions.enter_text_by_xpath(first_name_xpath, first_name_text)
        action_results['Enter First Name'] = '✅ Success'

        # Enter last name with dynamic phone number
        last_name_xpath = '//android.widget.EditText[@text="Last name"]'
        last_name_text = f"LAST{test_phone_number}"
        device_actions.enter_text_by_xpath(last_name_xpath, last_name_text)
        action_results['Enter Last Name'] = '✅ Success'
        
        # Click the confirm button on the name screen
        name_confirm_button_id = "com.appcard.androidterminal:id/tvConfirm"
        device_actions.click_by_id_or_text(resource_id=name_confirm_button_id)
        action_results['Click Name Confirm Button'] = '✅ Success'

        # Wait 3 seconds after clicking confirm
        print(f"⏳ Waiting 3 seconds after clicking name confirm...")
        time.sleep(3)
        
        print(f"🎉 Script completed successfully. (from {CURRENT_FILE})")

    except Exception as e:
        error_message = str(e)
        print(f"🛑 An error occurred: {error_message} (from {CURRENT_FILE})")
        action_results['Final Status'] = '❌ Failure'
    finally:
        # Final cleanup
        if 'device_actions' in locals() and device_actions.driver:
            device_actions.quit()
        if 'appium_manager' in locals():
            appium_manager.stop_server()

        # Print summary
        print("\n--- Script Execution Summary ---")
        for action, result in action_results.items():
            print(f"{result} {action}")
        if error_message:
            print(f"\n🛑 Execution finished with an error: {error_message}")
        else:
            print("\n🎉 Execution completed successfully, without errors.")
