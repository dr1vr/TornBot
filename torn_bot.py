import os
import time
import random
import schedule
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

from torn_api import TornAPI

# Load environment variables
load_dotenv()

class TornBot:
    """
    A bot to automate various activities in Torn
    """
    
    def __init__(self):
        """Initialize the TornBot"""
        self.api = TornAPI()
        self.user_id = None
        self.name = None
        
        # Feature flags
        self.enable_crimes = self._parse_bool_env("ENABLE_CRIMES", True)
        self.enable_gym = self._parse_bool_env("ENABLE_GYM", True)
        self.enable_items = self._parse_bool_env("ENABLE_ITEMS", True)
        self.enable_education = self._parse_bool_env("ENABLE_EDUCATION", True)
        self.enable_travel = self._parse_bool_env("ENABLE_TRAVEL", False)
        
        # Cache for data
        self.cache = {}
        
        # Initialize user data
        self._initialize()
    
    def _parse_bool_env(self, key: str, default: bool = False) -> bool:
        """Parse boolean environment variables"""
        value = os.getenv(key, str(default)).lower()
        return value in ("true", "1", "t", "yes", "y")
    
    def _initialize(self):
        """Initialize the bot with user data"""
        print("Initializing TornBot...")
        
        # Get user profile
        user_data = self.api.get_user(["profile"])
        if "error" in user_data:
            print("Failed to initialize bot. Check your API key.")
            return
        
        self.user_id = user_data.get("player_id")
        self.name = user_data.get("name")
        
        print(f"Bot initialized for: {self.name} [{self.user_id}]")
        print(f"Features enabled:")
        print(f"  - Crimes: {self.enable_crimes}")
        print(f"  - Gym: {self.enable_gym}")
        print(f"  - Items: {self.enable_items}")
        print(f"  - Education: {self.enable_education}")
        print(f"  - Travel: {self.enable_travel}")
    
    def update_status(self):
        """Update and print the current user status"""
        # Get user data with multiple selections
        selections = ["profile", "bars", "cooldowns", "notifications"]
        if self.enable_education:
            selections.append("education")
        
        user_data = self.api.get_user(selections)
        if "error" in user_data:
            print("Failed to update status.")
            return
        
        # Cache the data
        self.cache["user_data"] = user_data
        
        # Print status
        print("\n" + "="*50)
        print(f"Status update for {self.name} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50)
        
        # Print bars
        if "bars" in user_data:
            bars = user_data["bars"]
            print(f"Energy: {bars['energy']['current']}/{bars['energy']['maximum']}")
            print(f"Nerve: {bars['nerve']['current']}/{bars['nerve']['maximum']}")
            print(f"Happy: {bars['happy']['current']}/{bars['happy']['maximum']}")
            print(f"Life: {bars['life']['current']}/{bars['life']['maximum']}")
        
        # Print cooldowns
        if "cooldowns" in user_data:
            cooldowns = user_data["cooldowns"]
            for name, seconds in cooldowns.items():
                if seconds > 0:
                    minutes = seconds // 60
                    remaining_seconds = seconds % 60
                    print(f"{name.capitalize()} cooldown: {minutes}m {remaining_seconds}s")
        
        # Print notifications
        if "notifications" in user_data and user_data["notifications"]:
            print("\nNotifications:")
            for category, count in user_data["notifications"].items():
                if count > 0:
                    print(f"  - {category}: {count}")
        
        # Print education status
        if "education" in user_data and "education_current" in user_data:
            current = user_data["education_current"]
            if current:
                time_left = current.get("time_left", 0)
                minutes = time_left // 60
                remaining_seconds = time_left % 60
                print(f"\nCurrently studying: {current.get('name', 'Unknown')} - {minutes}m {remaining_seconds}s remaining")
        
        print("="*50)
        
        # Run actions based on status
        self._run_actions()
    
    def _run_actions(self):
        """Run actions based on current status"""
        if not self.cache.get("user_data"):
            print("No user data available. Skipping actions.")
            return
        
        user_data = self.cache["user_data"]
        
        # Check if we can perform actions
        if "status" in user_data and user_data["status"].get("state") != "okay":
            state = user_data["status"].get("state", "unknown")
            print(f"Cannot perform actions. Current state: {state}")
            return
        
        # Run enabled actions
        if self.enable_crimes:
            self.do_crimes()
        
        if self.enable_gym:
            self.do_gym()
        
        if self.enable_items:
            self.use_items()
        
        if self.enable_education:
            self.do_education()
    
    def do_crimes(self):
        """Perform crimes if nerve is available"""
        if not self.cache.get("user_data"):
            return
        
        user_data = self.cache["user_data"]
        
        # Check if we have nerve
        if "bars" in user_data and user_data["bars"]["nerve"]["current"] > 0:
            print("\nPerforming crimes...")
            
            # Get crime data
            crime_data = self.api.get_user(["crimes"])
            if "error" in crime_data:
                print("Failed to get crime data.")
                return
            
            # Find the best crime to commit
            best_crime = None
            best_success = 0
            
            for crime_id, crime in crime_data.get("crimes", {}).items():
                success = crime.get("success", 0)
                nerve = crime.get("nerve", 100)  # Default to high value if not found
                
                # Only consider crimes we have enough nerve for
                if user_data["bars"]["nerve"]["current"] >= nerve:
                    if success > best_success:
                        best_success = success
                        best_crime = crime_id
            
            if best_crime:
                # Commit the crime
                print(f"Committing crime: {crime_data['crimes'][best_crime]['name']} (Success rate: {best_success}%)")
                # In a real implementation, this would make an API call to commit the crime
                # Since the Torn API doesn't support this directly, this would require browser automation
                print("Note: Crime automation requires browser interaction which is not implemented in this API-only bot")
            else:
                print("No suitable crimes found.")
        else:
            print("Not enough nerve to commit crimes.")
    
    def do_gym(self):
        """Train at the gym if energy is available"""
        if not self.cache.get("user_data"):
            return
        
        user_data = self.cache["user_data"]
        
        # Check if we have energy
        if "bars" in user_data and user_data["bars"]["energy"]["current"] > 0:
            print("\nTraining at the gym...")
            
            # Get gym data
            gym_data = self.api.get_user(["gyms"])
            if "error" in gym_data:
                print("Failed to get gym data.")
                return
            
            # Find the best gym to train at
            # In a real implementation, this would make an API call to train at the gym
            # Since the Torn API doesn't support this directly, this would require browser automation
            print("Note: Gym automation requires browser interaction which is not implemented in this API-only bot")
        else:
            print("Not enough energy to train at the gym.")
    
    def use_items(self):
        """Use items from inventory"""
        print("\nChecking inventory for usable items...")
        
        # Get inventory data
        inventory_data = self.api.get_user(["inventory"])
        if "error" in inventory_data:
            print("Failed to get inventory data.")
            return
        
        # Check for energy drinks, etc.
        # In a real implementation, this would make an API call to use items
        # Since the Torn API doesn't support this directly, this would require browser automation
        print("Note: Item usage requires browser interaction which is not implemented in this API-only bot")
    
    def do_education(self):
        """Start education courses if not currently studying"""
        if not self.cache.get("user_data"):
            return
        
        user_data = self.cache["user_data"]
        
        # Check if we're already studying
        if "education_current" in user_data and user_data["education_current"]:
            print("Already studying a course.")
            return
        
        print("\nChecking for education courses...")
        
        # Get education data
        if "education" not in user_data:
            education_data = self.api.get_user(["education"])
            if "error" in education_data:
                print("Failed to get education data.")
                return
            user_data["education"] = education_data.get("education", {})
        
        # Find a suitable course
        # In a real implementation, this would make an API call to start a course
        # Since the Torn API doesn't support this directly, this would require browser automation
        print("Note: Education automation requires browser interaction which is not implemented in this API-only bot")
    
    def run(self):
        """Run the bot"""
        print("Starting TornBot...")
        
        # Update status immediately
        self.update_status()
        
        # Schedule status updates
        interval = int(os.getenv("API_CALL_INTERVAL", "60"))
        print(f"Scheduling status updates every {interval} seconds")
        
        schedule.every(interval).seconds.do(self.update_status)
        
        # Run the scheduler
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nBot stopped by user.")
        except Exception as e:
            print(f"\nBot stopped due to error: {str(e)}")


if __name__ == "__main__":
    bot = TornBot()
    bot.run()