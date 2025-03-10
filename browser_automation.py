import os
import time
import random
from typing import Dict, Any, Optional, List, Union
from dotenv import load_dotenv
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Load environment variables
load_dotenv()

class TornBrowser:
    """
    A class to handle browser automation for Torn
    """
    
    def __init__(self, headless: bool = False):
        """
        Initialize the TornBrowser class
        
        Args:
            headless: Whether to run the browser in headless mode
        """
        self.base_url = "https://www.torn.com"
        self.api_key = os.getenv("TORN_API_KEY")
        self.username = os.getenv("TORN_USERNAME")
        self.password = os.getenv("TORN_PASSWORD")
        
        if not self.api_key:
            raise ValueError("API key is required. Set it in .env file.")
        
        if not self.username or not self.password:
            raise ValueError("Username and password are required for browser automation. Set them in .env file.")
        
        # Initialize browser
        self.driver = self._initialize_browser(headless)
        self.logged_in = False
    
    def _initialize_browser(self, headless: bool) -> webdriver.Chrome:
        """
        Initialize the browser
        
        Args:
            headless: Whether to run the browser in headless mode
            
        Returns:
            Selenium WebDriver instance
        """
        options = webdriver.ChromeOptions()
        
        if headless:
            options.add_argument("--headless")
        
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        
        # Add user agent to avoid detection
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # Create browser instance
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(1366, 768)
        
        return driver
    
    def login(self) -> bool:
        """
        Log in to Torn
        
        Returns:
            True if login successful, False otherwise
        """
        if self.logged_in:
            print("Already logged in.")
            return True
        
        try:
            print("Logging in to Torn...")
            
            # Navigate to login page
            self.driver.get(f"{self.base_url}/login")
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "player"))
            )
            
            # Enter username and password
            self.driver.find_element(By.ID, "player").send_keys(self.username)
            self.driver.find_element(By.ID, "password").send_keys(self.password)
            
            # Click login button
            self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
            
            # Wait for login to complete
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".user-info"))
            )
            
            self.logged_in = True
            print("Login successful.")
            
            # Handle any popups
            self._handle_popups()
            
            return True
        except Exception as e:
            print(f"Login failed: {str(e)}")
            return False
    
    def _handle_popups(self):
        """Handle any popups that appear after login"""
        try:
            # Wait a moment for popups to appear
            time.sleep(2)
            
            # Close any popups (adjust selectors as needed)
            popups = self.driver.find_elements(By.CSS_SELECTOR, ".popup-info .close-icon")
            for popup in popups:
                popup.click()
                time.sleep(0.5)
        except Exception as e:
            print(f"Error handling popups: {str(e)}")
    
    def commit_crime(self, crime_id: str) -> bool:
        """
        Commit a crime
        
        Args:
            crime_id: ID of the crime to commit
            
        Returns:
            True if crime was committed, False otherwise
        """
        if not self.logged_in and not self.login():
            return False
        
        try:
            print(f"Committing crime {crime_id}...")
            
            # Navigate to crimes page
            self.driver.get(f"{self.base_url}/crimes.php")
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".content-title"))
            )
            
            # Find and click on the crime
            crime_element = self.driver.find_element(By.CSS_SELECTOR, f"#crime{crime_id}")
            crime_element.click()
            
            # Wait for crime form to appear
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".submit-crime"))
            )
            
            # Click the submit button
            submit_button = self.driver.find_element(By.CSS_SELECTOR, ".submit-crime")
            submit_button.click()
            
            # Wait for result
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".msg"))
            )
            
            # Check result
            result_element = self.driver.find_element(By.CSS_SELECTOR, ".msg")
            result_text = result_element.text
            
            if "success" in result_text.lower():
                print("Crime successful!")
                return True
            else:
                print(f"Crime failed: {result_text}")
                return False
        except Exception as e:
            print(f"Error committing crime: {str(e)}")
            return False
    
    def train_gym(self, stat: str) -> bool:
        """
        Train at the gym
        
        Args:
            stat: Stat to train (strength, defense, speed, dexterity)
            
        Returns:
            True if training was successful, False otherwise
        """
        if not self.logged_in and not self.login():
            return False
        
        try:
            print(f"Training {stat} at the gym...")
            
            # Navigate to gym page
            self.driver.get(f"{self.base_url}/gym.php")
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".content-title"))
            )
            
            # Find and click on the stat
            stat_element = self.driver.find_element(By.CSS_SELECTOR, f"#train-{stat}")
            stat_element.click()
            
            # Wait for training form to appear
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".train-submit"))
            )
            
            # Click the submit button
            submit_button = self.driver.find_element(By.CSS_SELECTOR, ".train-submit")
            submit_button.click()
            
            # Wait for result
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".msg"))
            )
            
            # Check result
            result_element = self.driver.find_element(By.CSS_SELECTOR, ".msg")
            result_text = result_element.text
            
            if "trained" in result_text.lower():
                print("Training successful!")
                return True
            else:
                print(f"Training failed: {result_text}")
                return False
        except Exception as e:
            print(f"Error training at gym: {str(e)}")
            return False
    
    def use_item(self, item_id: str) -> bool:
        """
        Use an item from inventory
        
        Args:
            item_id: ID of the item to use
            
        Returns:
            True if item was used, False otherwise
        """
        if not self.logged_in and not self.login():
            return False
        
        try:
            print(f"Using item {item_id}...")
            
            # Navigate to items page
            self.driver.get(f"{self.base_url}/item.php")
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".content-title"))
            )
            
            # Find and click on the item
            item_element = self.driver.find_element(By.CSS_SELECTOR, f"#item{item_id}")
            item_element.click()
            
            # Find and click the use button
            use_button = self.driver.find_element(By.CSS_SELECTOR, ".use-item")
            use_button.click()
            
            # Wait for result
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".msg"))
            )
            
            # Check result
            result_element = self.driver.find_element(By.CSS_SELECTOR, ".msg")
            result_text = result_element.text
            
            if "used" in result_text.lower():
                print("Item used successfully!")
                return True
            else:
                print(f"Failed to use item: {result_text}")
                return False
        except Exception as e:
            print(f"Error using item: {str(e)}")
            return False
    
    def start_education(self, course_id: str) -> bool:
        """
        Start an education course
        
        Args:
            course_id: ID of the course to start
            
        Returns:
            True if course was started, False otherwise
        """
        if not self.logged_in and not self.login():
            return False
        
        try:
            print(f"Starting education course {course_id}...")
            
            # Navigate to education page
            self.driver.get(f"{self.base_url}/education.php")
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".content-title"))
            )
            
            # Check if already studying
            current_course = self.driver.find_elements(By.CSS_SELECTOR, ".education-active")
            if current_course:
                print("Already studying a course.")
                return False
            
            # Find and click on the course
            course_element = self.driver.find_element(By.CSS_SELECTOR, f"#course{course_id}")
            course_element.click()
            
            # Wait for course details to appear
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".start-education"))
            )
            
            # Click the start button
            start_button = self.driver.find_element(By.CSS_SELECTOR, ".start-education")
            start_button.click()
            
            # Wait for result
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".msg"))
            )
            
            # Check result
            result_element = self.driver.find_element(By.CSS_SELECTOR, ".msg")
            result_text = result_element.text
            
            if "started" in result_text.lower():
                print("Course started successfully!")
                return True
            else:
                print(f"Failed to start course: {result_text}")
                return False
        except Exception as e:
            print(f"Error starting education course: {str(e)}")
            return False
    
    def close(self):
        """Close the browser"""
        if self.driver:
            try:
                print("Closing browser...")
                self.driver.quit()
                print("Browser closed.")
            except Exception as e:
                print(f"Error closing browser: {str(e)}")


if __name__ == "__main__":
    # Example usage
    headless = os.getenv("HEADLESS_BROWSER", "false").lower() in ("true", "1", "t", "yes", "y")
    
    try:
        browser = TornBrowser(headless=headless)
        print("Browser initialized.")
        
        if browser.login():
            print("Logged in successfully.")
            
            # Example: Commit a crime
            # browser.commit_crime("1")
            
            # Example: Train at the gym
            # browser.train_gym("strength")
            
            # Example: Use an item
            # browser.use_item("1")
            
            # Example: Start an education course
            # browser.start_education("1")
            
            # Close browser
            browser.close()
    except Exception as e:
        print(f"Error: {str(e)}")