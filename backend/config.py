from git import Repo

# Repository path for Git operations
REPO_PATH = "C:/Users/maheru/Desktop/MCodingTest/fast_api/FastAPI_Project"

# Initialize the Git repository
repo = Repo(REPO_PATH)

# Gmail SMTP credentials
SMTP_SERVER = "smtp.gmail.com" 
SMTP_PORT = 465
GMAIL_USER = "maheshbirajdar37346@gmail.com"
GMAIL_APP_PASSWORD = "aauo nhdw vryu ijqo"

# Microsoft Teams webhook URL for notifications
TEAMS_WEBHOOK_URL = "https://teams.live.com/l/community/FEAsbpzjJVLoOPd_AI"

# JSON schema for the file
json_schema ={
  "timestamp": "2025-08-02T11:00:00",
  "category": "Food | Health | Finance | Task | Weather",
  "item": "Description of the item",
  "quantity": "Amount or count",
  "unit": "Kg, hours, INR, °C etc.",
  "priority": "Low | Medium | High",
  "notes": "Optional note for the item"
}