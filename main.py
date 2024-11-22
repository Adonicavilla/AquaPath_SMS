import tkinter as tk
from tkinter import messagebox
import requests
import mysql.connector

def fetch_phone_numbers():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_sms"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT phone_number FROM contacts")
        rows = cursor.fetchall()
        phone_numbers = [row[0] for row in rows]
        conn.close()
        return ','.join(phone_numbers)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return ""

def send_sms(message):
    apiSecret = "d876bad8084ee5626e015904752ea9b3df328588"
    deviceId = "00000000-0000-0000-29ac-666853fbd26e"
    phones = fetch_phone_numbers()  # Get phone numbers from database

    if not phones:
        messagebox.showerror("Error", "Failed to fetch phone numbers.")
        return

    message_data = {
        "secret": apiSecret,
        "mode": "devices",
        "campaign": "bulk test",
        "numbers": phones,
        "groups": "1,2,3,4",  # Ensure this aligns with API expectations if applicable
        "device": deviceId,
        "sim": 1,
        "priority": 1,
        "message": message
    }

    try:
        r = requests.post(url="https://www.cloud.smschef.com/api/send/sms.bulk", params=message_data, timeout=30)
        r.raise_for_status()
        result = r.json()
        print("Response JSON:", result)
        if result.get('status') == 200:
            messagebox.showinfo("Success", "Message sent successfully!")
        else:
            messagebox.showerror("Error", f"Failed to send message: {result.get('message')}")
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        messagebox.showerror("Error", "Failed to send message. Please try again.")

# Set up the tkinter window
root = tk.Tk()
root.title("SMS Sender")

# Green button
green_button = tk.Button(root, text="Safe to Go", bg="green", command=lambda: send_sms("Safe to go"))
green_button.grid(row=0, column=0, padx=10, pady=10)

# Yellow button
yellow_button = tk.Button(root, text="Warning: There's Water", bg="yellow", command=lambda: send_sms("Warning: there's water"))
yellow_button.grid(row=0, column=1, padx=10, pady=10)

# Red button
red_button = tk.Button(root, text="Street is Blocked", bg="red", command=lambda: send_sms("This street is blocked"))
red_button.grid(row=0, column=2, padx=10, pady=10)

# Start the tkinter main loop
root.mainloop()
