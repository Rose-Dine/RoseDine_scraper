import subprocess
import sys
import schedule
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os
import time

def delete_and_create_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted: {file_path}")
    open(file_path, 'a').close()
    print(f"Created: {file_path}")

def run_schedule():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    with open('PyScraping/output.txt', 'a') as file:
        schedule.scrape_weekly_meals(driver, file)
    driver.quit()

def run_api_jsonify():
    subprocess.run([sys.executable, "PyScraping/api_jsonify.py"])

if __name__ == "__main__":
    # Delete and recreate both files
    delete_and_create_file('PyScraping/output.txt')
    delete_and_create_file('PyScraping/nutrition_info.json')

    # Run schedule
    run_schedule()
    print("schedule.py finished. Waiting 1 second before running api_jsonify.py...")
    time.sleep(1)

    # Run api_jsonify
    run_api_jsonify()
    print("api_jsonify.py finished. Waiting 1 second before sending POST request...")
    time.sleep(1)

    # Send POST request (placeholder for your actual code)
    print("Sending POST request")
    # Your code to send the POST request goes here