import subprocess
import time
from appium.webdriver.appium_service import AppiumService
import os

CURRENT_FILE = os.path.basename(__file__)

class AppiumManager:
    """Manages the Appium server lifecycle."""

    def __init__(self, port=4723):
        self.port = port
        self.service = AppiumService()

    def start_server(self):
        """Starts the Appium server."""
        print("🚀 Starting Appium server...")
        try:
            self.service.start()
            print("✅ Appium server started successfully.")
            time.sleep(5)  # Give the server a moment to get ready
        except Exception as e:
            print(f"❌ Failed to start Appium server: {e}")
            raise

    def stop_server(self):
        """Stops the Appium server."""
        print("👋 Shutting down Appium server...")
        try:
            self.service.stop()
            print("✅ Appium server shut down.")
        except Exception as e:
            print(f"❌ Failed to stop Appium server: {e}")