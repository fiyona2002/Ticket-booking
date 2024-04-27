import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RedBusPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        
        self.from_city_input = (By.ID, "src")
        self.to_city_input = (By.ID, "dest")
        self.date_input = (By.ID, "onward_cal")
        self.search_button = (By.ID, "search_btn")
        self.search_results = (By.CLASS_NAME, "service-name")

    def open(self, url):
        self.driver.get(url)

    def search_buses(self, from_city, to_city, date):
        self.driver.find_element(*self.from_city_input).send_keys(from_city)
        self.driver.find_element(*self.to_city_input).send_keys(to_city)
        self.driver.find_element(*self.date_input).send_keys(date)
        self.driver.find_element(*self.search_button).click()

    def get_number_of_buses(self):
        results = self.wait.until(EC.visibility_of_all_elements_located(self.search_results))
        return len(results)

# Read values from CSV file
def read_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

# Write results to CSV file
def write_csv(file_path, data):
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["From City", "Destination City", "Date", "Bus Count"])
        writer.writeheader()
        writer.writerows(data)

# Test script
if __name__ == "__main__":
    # Initialize WebDriver (you need to install the appropriate driver for your browser)
    driver = webdriver.Chrome()  # Change this line if you are using a different browser

    # Initialize RedBusPage
    redbus_page = RedBusPage(driver)

    # Open RedBus website
    redbus_page.open("https://www.redbus.in/")

    # Read values from CSV file
    csv_data = read_csv("test_data.csv")

    # Process only first 5 records
    results = []
    for row in csv_data[:5]:
        from_city = row["From City"]
        to_city = row["Destination City"]
        date = row["Date"]

        # Search buses
        redbus_page.search_buses(from_city, to_city, date)

        # Get number of buses
        num_buses = redbus_page.get_number_of_buses()

        # Append results
        row["Bus Count"] = num_buses
        results.append(row)

    # Write results back to CSV file
    write_csv("test_results.csv", results)

    # Close the WebDriver
    driver.quit()
