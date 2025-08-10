import os
import json
from datetime import datetime

base_path = r"C:\Users\maheru\Desktop\MCodingTest\fast_api\FastAPI_Project"

json_schema ={
  "timestamp": "2025-08-02T11:00:00",
  "category": "Food | Health | Finance | Task | Weather",
  "item": "Description of the item",
  "quantity": "Amount or count",
  "unit": "Kg, hours, INR, °C etc.",
  "priority": "Low | Medium | High",
  "notes": "Optional note for the item"
}


data_map = {
    "food": {
        "breakfast.json": {
            "item": "Oats with banana", "quantity": "1", "unit": "bowl", "notes": "Add honey if needed"
        },
        "grocery_list.json": {
            "item": "Tomatoes", "quantity": "2", "unit": "kg", "notes": "Check for ripeness"
        },
        "dinner.json": {
            "item": "Grilled chicken", "quantity": "1", "unit": "plate", "notes": "Add lemon dressing"
        }
    },
    "health": {
        "medicine_schedule.json": {
            "item": "Vitamin D tablet", "quantity": "1", "unit": "tablet", "notes": "After breakfast"
        },
        "workout.json": {
            "item": "Cardio training", "quantity": "30", "unit": "minutes", "notes": "Focus on treadmill"
        },
        "health_checkup.json": {
            "item": "Blood pressure check", "quantity": "1", "unit": "check", "notes": "Use home monitor"
        }
    },
    "finance": {
        "expenses.json": {
            "item": "Petrol refill", "quantity": "1500", "unit": "INR", "notes": "Filled full tank"
        },
        "savings.json": {
            "item": "Monthly SIP", "quantity": "5000", "unit": "INR", "notes": "Auto-debited"
        },
        "monthly_budget.json": {
            "item": "August budget", "quantity": "25000", "unit": "INR", "notes": "Includes rent and utilities"
        }
    },
    "tasks": {
        "today_todo.json": {
            "item": "Reply to client emails", "quantity": "5", "unit": "emails", "notes": "Before 10 AM"
        },
        "home_maintenance.json": {
            "item": "Fix kitchen tap", "quantity": "1", "unit": "task", "notes": "Use plumber contact"
        },
        "work_tasks.json": {
            "item": "Finish API integration", "quantity": "1", "unit": "task", "notes": "Push to Git before EOD"
        }
    },
    "weather": {
        "morning_forecast.json": {
            "item": "Sunny", "quantity": "28", "unit": "°C", "notes": "UV index high"
        },
        "evening_forecast.json": {
            "item": "Cloudy", "quantity": "25", "unit": "°C", "notes": "Light breeze"
        },
        "alerts.json": {
            "item": "Heavy rainfall warning", "quantity": "60", "unit": "mm", "notes": "Avoid travel after 3 PM"
        }
    }
}

# Write JSON files
for folder, files in data_map.items():
    folder_path = os.path.join(base_path, folder)
    os.makedirs(folder_path, exist_ok=True)
    
    for filename, content in files.items():
        data = {
            "timestamp": datetime.now().isoformat(),
            "category": folder.capitalize(),
            "priority": "High" if folder in ["food", "finance", "tasks"] else "Medium",
            **content
        }
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

print("✅ All JSON files written successfully.")
