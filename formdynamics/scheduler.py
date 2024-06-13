# scheduler.py

import requests
import schedule
import time
import django
import os
from salesorder.models import salesorder  # replace 'your_app' with your actual app name

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
django.setup()

# Global variables
grant_token = "your_grant_token"
access_token = None
refresh_token = "your_refresh_token"
client_id = "your_client_id"
client_secret = "your_client_secret"
redirect_uri = "your_redirect_uri"

# Function to generate access token from refresh token
def generate_access_token_from_refresh_token():
    global access_token, refresh_token
    token_url = "https://accounts.zoho.in/oauth/v2/token"
    payload = {
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "refresh_token"
    }
    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens['access_token']
        print("Access token refreshed successfully.")
    else:
        print("Error refreshing access token:", response.json())
        if response.json().get("error") == "invalid_code":
            perform_complete_auth_flow()

# Function to perform the complete authentication flow
def perform_complete_auth_flow():
    global access_token, refresh_token, grant_token
    token_url = "https://accounts.zoho.in/oauth/v2/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "code": grant_token
    }
    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']
        print("Access token and refresh token generated successfully.")
    else:
        print("Error generating tokens:", response.json())

# Function to call the Zoho API
def apicall_salesorder():
    global access_token
    url = "https://www.zohoapis.in/books/v3/salesorders?organization_id=60004755614"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
       
        if "salesorders" in data:
            salesorders = data["salesorders"]
       
            for salesorder_data in salesorders:
                # Check if the salesorder_id already exists in the database
                if not salesorder.objects.filter(salesorder_id=salesorder_data["salesorder_id"]).exists():
                    salesorder.objects.create(
                        salesorder_id=salesorder_data["salesorder_id"],
                        zcrm_potential_id=salesorder_data["zcrm_potential_id"],
                        zcrm_potential_name=salesorder_data["zcrm_potential_name"],
                        customer_name=salesorder_data["customer_name"],
                        customer_id=salesorder_data["customer_id"],
                        email=salesorder_data["email"],
                        delivery_date=salesorder_data["delivery_date"],
                        company_name=salesorder_data["company_name"],
                        color_code=salesorder_data["color_code"],
                        current_sub_status_id=salesorder_data["current_sub_status_id"],
                        current_sub_status=salesorder_data["current_sub_status"],
                        pickup_location_id=salesorder_data["pickup_location_id"],
                        salesorder_number=salesorder_data["salesorder_number"],
                        reference_number=salesorder_data["reference_number"],
                        date=salesorder_data["date"],
                        shipment_date=salesorder_data["shipment_date"],
                        shipment_days=salesorder_data["shipment_days"],
                        due_by_days=salesorder_data["due_by_days"],
                        due_in_days=salesorder_data["due_in_days"],
                        currency_id=salesorder_data["currency_id"],
                        source=salesorder_data["source"],
                        currency_code=salesorder_data["currency_code"],
                        total=salesorder_data["total"],
                        bcy_total=salesorder_data["bcy_total"],
                        total_invoiced_amount=salesorder_data["total_invoiced_amount"],
                        created_time=salesorder_data["created_time"],
                        last_modified_time=salesorder_data["last_modified_time"],
                        is_emailed=salesorder_data["is_emailed"],
                        quantity_invoiced=salesorder_data["quantity_invoiced"],
                        order_status=salesorder_data["order_status"],
                        invoiced_status=salesorder_data["invoiced_status"],
                        paid_status=salesorder_data["paid_status"],
                        status=salesorder_data["status"],
                        salesperson_name=salesorder_data["salesperson_name"],
                        branch_id=salesorder_data["branch_id"],
                        branch_name=salesorder_data["branch_name"],
                        has_attachment=salesorder_data["has_attachment"],
                        custom_fields_list=salesorder_data["custom_fields_list"],
                        delivery_method=salesorder_data["delivery_method"],
                        delivery_method_id=salesorder_data["delivery_method_id"]
                    )
                    print("Sales order saved")
                else:
                    print(f"Sales order with ID {salesorder_data['salesorder_id']} already exists.")
                    
        return {"message": "Data processed successfully."}   
    else:
        error_data = {
            "error": f"Error: {response.status_code}",
            "error_message": response.text,
        }
        print("Error in API request:", error_data)
        return error_data

# Function to update access token every 58 minutes
def schedule_access_token_update():
    try:
        generate_access_token_from_refresh_token()
    except Exception as e:
        print("Error in scheduled access token update:", e)

# Scheduling the access token update function
schedule.every(58).minutes.do(schedule_access_token_update)

# Initial token generation
try:
    perform_complete_auth_flow()
except Exception as e:
    print("Error in initial token generation:", e)

# Schedule the sales order API call
schedule.every().hour.do(apicall_salesorder)

# Run the scheduler
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_scheduler()
