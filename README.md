# TornBot

An automated bot for Torn City that uses both the Torn API and browser automation to automate various activities.

## Features

- **API Integration**: Uses the Torn API to fetch user data, status, and other information
- **Browser Automation**: Uses Selenium to automate actions that can't be done through the API
- **Modular Design**: Separate modules for API interaction and browser automation
- **Configurable**: Enable/disable features via environment variables
- **Scheduled Actions**: Automatically performs actions based on a schedule

### Automated Activities

- **Crimes**: Automatically commits crimes when nerve is available
- **Gym Training**: Trains at the gym when energy is available
- **Item Usage**: Uses items from inventory (energy drinks, etc.)
- **Education**: Starts education courses when not currently studying
- **Travel**: (Disabled by default) Can be enabled for travel automation