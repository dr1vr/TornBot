import os
import time
import requests
from typing import Dict, Any, Optional, List, Union
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TornAPI:
    """
    A class to interact with the Torn API
    """
    BASE_URL = "https://api.torn.com"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the TornAPI class
        
        Args:
            api_key: Torn API key. If not provided, it will be loaded from environment variables
        """
        self.api_key = api_key or os.getenv("TORN_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required. Set it in .env file or pass it to the constructor.")
        
        self.last_request_time = 0
        self.min_request_interval = int(os.getenv("API_CALL_INTERVAL", "30"))
    
    def _make_request(self, section: str, selections: List[str], 
                     id: Optional[Union[int, str]] = None, 
                     params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a request to the Torn API
        
        Args:
            section: API section (user, property, faction, company, market, torn)
            selections: List of selections to request
            id: ID for the request (optional)
            params: Additional parameters for the request
            
        Returns:
            API response as a dictionary
        """
        # Respect rate limits
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last_request
            print(f"Rate limiting: Sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        # Build URL
        url = f"{self.BASE_URL}/{section}"
        if id is not None:
            url += f"/{id}"
        
        # Prepare parameters
        request_params = params or {}
        request_params["key"] = self.api_key
        request_params["selections"] = ",".join(selections)
        
        # Make request
        try:
            response = requests.get(url, params=request_params)
            self.last_request_time = time.time()
            
            # Check for errors
            if response.status_code != 200:
                print(f"Error: HTTP {response.status_code}")
                return {"error": {"code": response.status_code, "message": response.text}}
            
            data = response.json()
            
            # Check for API errors
            if "error" in data:
                error_code = data["error"]["code"]
                error_message = data["error"]["error"]
                print(f"API Error {error_code}: {error_message}")
                return data
            
            return data
        except Exception as e:
            print(f"Request failed: {str(e)}")
            return {"error": {"code": -1, "message": str(e)}}
    
    def get_user(self, selections: List[str], user_id: str = "") -> Dict[str, Any]:
        """
        Get user data from the API
        
        Args:
            selections: List of selections to request
            user_id: User ID (empty for current user)
            
        Returns:
            User data
        """
        return self._make_request("user", selections, user_id)
    
    def get_property(self, selections: List[str], property_id: str = "") -> Dict[str, Any]:
        """
        Get property data from the API
        
        Args:
            selections: List of selections to request
            property_id: Property ID (empty for current properties)
            
        Returns:
            Property data
        """
        return self._make_request("property", selections, property_id)
    
    def get_faction(self, selections: List[str], faction_id: str = "") -> Dict[str, Any]:
        """
        Get faction data from the API
        
        Args:
            selections: List of selections to request
            faction_id: Faction ID (empty for current faction)
            
        Returns:
            Faction data
        """
        return self._make_request("faction", selections, faction_id)
    
    def get_company(self, selections: List[str], company_id: str = "") -> Dict[str, Any]:
        """
        Get company data from the API
        
        Args:
            selections: List of selections to request
            company_id: Company ID (empty for current company)
            
        Returns:
            Company data
        """
        return self._make_request("company", selections, company_id)
    
    def get_market(self, selections: List[str], item_id: str = "") -> Dict[str, Any]:
        """
        Get market data from the API
        
        Args:
            selections: List of selections to request
            item_id: Item ID
            
        Returns:
            Market data
        """
        return self._make_request("market", selections, item_id)
    
    def get_torn(self, selections: List[str]) -> Dict[str, Any]:
        """
        Get torn data from the API
        
        Args:
            selections: List of selections to request
            
        Returns:
            Torn data
        """
        return self._make_request("torn", selections)


if __name__ == "__main__":
    # Example usage
    api = TornAPI()
    
    # Get user profile
    user_data = api.get_user(["profile"])
    if "error" not in user_data:
        print(f"Logged in as: {user_data.get('name', 'Unknown')} [{user_data.get('player_id', 'Unknown')}]")
    else:
        print("Failed to get user data")