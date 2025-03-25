# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import tkinter as tk
from tkinter import ttk, messagebox
import json
import finance  # Import finance.py as a module


def enter_data():
    """Retrieve user inputs, save them to JSON, and run stock screener."""
    accepted = accept_var.get()

    if accepted == "Accepted":
        user_data = {
            "first_name": first_name_entry.get(),
            "last_name": last_name_entry.get(),
            "age": int(age_spinbox.get()),
            "career_point": career_combobox.get(),
            "risk_tolerance": risk_combobox.get(),
            "goal": goal_combobox.get(),
            "time": time_combobox.get(),
            "money_total": float(money_spinbox.get()),
            "money_for_stock": float(shares_spinbox.get()),
            "sector": sector_combobox.get()
        }

        with open("user_preferences.json", "w") as f:
            json.dump(user_data, f)

        recommended_stock = finance.run_stock_screener("user_preferences.json")

        if recommended_stock:
            messagebox.showinfo("Stock Recommendation", f"Best stock recommendation: {recommended_stock}")
        else:
            messagebox.showwarning("No Match", "No suitable stock found based on your preferences.")
    else:
        messagebox.showwarning("Error", "You haven't accepted the terms and conditions!")


# GUI Setup (unchanged from previous version)
window = tk.Tk()
window.title("Data Entry Form")

frame = tk.Frame(window)
frame.pack()

user_info_frame = tk.LabelFrame(frame, text="User Information")
user_info_frame.grid(row=0, column=0, padx=20, pady=10)

tk.Label(user_info_frame, text="First Name").grid(row=0, column=0)
tk.Label(user_info_frame, text="Last Name").grid(row=0, column=1)

first_name_entry = tk.Entry(user_info_frame)
last_name_entry = tk.Entry(user_info_frame)
first_name_entry.grid(row=1, column=0)
last_name_entry.grid(row=1, column=1)

age_frame = tk.LabelFrame(frame, text="Age Related Analysis")
age_frame.grid(row=1, column=0, padx=10, pady=10)

tk.Label(age_frame, text="Age").grid(row=0, column=0)
age_spinbox = tk.Spinbox(age_frame, from_=18, to=110)
age_spinbox.grid(row=1, column=0, padx=10, pady=10)

tk.Label(age_frame, text="Point in Career").grid(row=0, column=1)
career_combobox = ttk.Combobox(age_frame, values=["Beginning", "Middle", "Nearing Retirement", "Retired"])
career_combobox.grid(row=1, column=1, padx=10, pady=10)

tk.Label(age_frame, text="Risk Tolerance").grid(row=0, column=2)
risk_combobox = ttk.Combobox(age_frame, values=["Aggressive", "Conservative", "Moderate"])
risk_combobox.grid(row=1, column=2, padx=10, pady=10)

goal_frame = tk.LabelFrame(frame, text="Goals")
goal_frame.grid(row=2, column=0, padx=10, pady=10)

tk.Label(goal_frame, text="Goal").grid(row=0, column=0)
goal_combobox = ttk.Combobox(goal_frame, values=["Exponential Growth", "Beat Inflation", "Diversification of Income"])
goal_combobox.grid(row=1, column=0, padx=10, pady=10)

tk.Label(goal_frame, text="Time to Keep Stock").grid(row=0, column=1)
time_combobox = ttk.Combobox(goal_frame,
                             values=["Less than 1 year", "1 Year", "2 Years", "3+ Years", "Until % Growth Achieved"])
time_combobox.grid(row=1, column=1, padx=10, pady=10)

money_frame = tk.LabelFrame(frame, text="Money Questions")
money_frame.grid(row=3, column=0, padx=10, pady=10)

tk.Label(money_frame, text="Total $ to Invest").grid(row=0, column=0)
money_spinbox = tk.Spinbox(money_frame, from_=1, to="infinity")
money_spinbox.grid(row=1, column=0, padx=10, pady=10)

tk.Label(money_frame, text="$ for Multiple Shares of Same Stock").grid(row=0, column=1)
shares_spinbox = tk.Spinbox(money_frame, from_=1, to="infinity")
shares_spinbox.grid(row=1, column=1, padx=10, pady=10)

sector_frame = tk.LabelFrame(frame, text="Stock Specific Questions")
sector_frame.grid(row=4, column=0, padx=10, pady=10)

tk.Label(sector_frame, text="Sector").grid(row=0, column=0)
sector_combobox = ttk.Combobox(sector_frame,
                               values=["Technology", "Telecommunications", "Healthcare", "Financials",
                                       "Real Estate", "Consumer Discretionary", "Consumer Staples",
                                       "Industrials", "Basic Materials", "Energy", "Utilities"])
sector_combobox.grid(row=1, column=0, padx=10, pady=10)

terms_frame = tk.LabelFrame(frame, text="Terms and Conditions")
terms_frame.grid(row=5, column=0, padx=20, pady=20)

accept_var = tk.StringVar(value="Not Accepted")
terms_check = tk.Checkbutton(terms_frame, text="I accept the Terms and Conditions", variable=accept_var,
                             onvalue="Accepted", offvalue="Not Accepted")
terms_check.grid(row=0, column=0)

tk.Button(frame, text="Enter Data", command=enter_data).grid(row=6, column=0, pady=10)

window.mainloop()


'''
import tkinter
from tkinter import ttk
from tkinter import messagebox
window = tkinter.Tk()
window.title("Data Entry Form")

def enter_data():
    accepted = accept_var.get()

    if accepted == "Accepted":
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        age = age_spinbox.get()
        career_point = career_combobox.get()
        risk_tolerance = risk_combobox.get()
        goal = goal_combobox.get()
        time = time_combobox.get()
        money_total = money_spinbox.get()
        money_for_stock = shares_spinbox.get()
        sector = sector_combobox.get()
    else:
        tkinter.messagebox.showwarning(title = "Error", message="You haven't accepted the terms and conditions")



frame = tkinter.Frame(window)
frame.pack()

# save user info
user_info_frame = tkinter.LabelFrame(frame, text="User Information")
user_info_frame.grid(row = 0, column=0, padx=20, pady=10)

first_name_label = tkinter.Label(user_info_frame, text="First Name")
first_name_label.grid(row = 0, column=0)
last_name_label = tkinter.Label(user_info_frame, text="Last Name")
last_name_label.grid(row = 0, column=1)

first_name_entry = tkinter.Entry(user_info_frame)
last_name_entry = tkinter.Entry(user_info_frame)
first_name_entry.grid(row=1, column=0)
last_name_entry.grid(row=1, column=1)

for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

age_frame = tkinter.LabelFrame(frame, text="Age Related Analysis")
age_frame.grid(row = 1, column=0, sticky="news", pady=20, padx=10)

age_label = tkinter.Label(age_frame, text = "Age")
age_spinbox = tkinter.Spinbox(age_frame, from_ = 18, to = 110)
age_label.grid(row=0, column=0)
age_spinbox.grid(row=1, column=0, padx=10, pady=10)

career_label = tkinter.Label(age_frame, text = "Point in Career")
career_combobox = ttk.Combobox(age_frame, values=["Beginning", "Middle", "Nearing Retirement", "Retired"])
career_label.grid(row= 0, column=1)
career_combobox.grid(row=1, column=1, padx=10, pady=10)

risk_label = tkinter.Label(age_frame, text = "Risk Tolerance")
risk_combobox = ttk.Combobox(age_frame, values=["Aggressive", "Conservative", "Moderate"])
risk_label.grid(row= 0, column=2)
risk_combobox.grid(row=1, column=2,padx=10, pady=10)

for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

goal_frame = tkinter.LabelFrame(frame, text="Goals")
goal_frame.grid(row = 2, column=0, sticky="news", pady=20, padx=10)

goal_label = tkinter.Label(goal_frame, text = "Goal")
goal_combobox = ttk.Combobox(goal_frame, values=["Exponential Growth", "Beat Inflation", "Diversification of Income"])
goal_label.grid(row= 0, column=0)
goal_combobox.grid(row=1, column=0,padx=10, pady=10)

time_label = tkinter.Label(goal_frame, text = "Time to Keep Stock")
time_combobox = ttk.Combobox(goal_frame, values=["Less than 1 year", "1 Year", "2 Years", "3+ Years", "Until % Growth Achieved"])
time_label.grid(row= 0, column=1)
time_combobox.grid(row=1, column=1, padx=10, pady=10)

for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=10)

money_frame = tkinter.LabelFrame(frame, text="Money Questions")
money_frame.grid(row = 3, column=0, sticky="news", pady=20, padx=10)

money_label = tkinter.Label(money_frame, text = "Total $ to Invest")
money_spinbox = tkinter.Spinbox(money_frame, from_=1, to="infinity")
money_label.grid(row=0, column=0, padx=10)
money_spinbox.grid(row=1, column=0, padx=10, pady=10)

shares_label = tkinter.Label(money_frame, text = "$ for Multiple Shares of Same Stock")
shares_spinbox = tkinter.Spinbox(money_frame, from_=1, to="infinity")
shares_label.grid(row=0, column=1)
shares_spinbox.grid(row=1, column=1, padx=10, pady=10)

for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=10)

sector_frame = tkinter.LabelFrame(frame, text="Stock Specific Questions")
sector_frame.grid(row = 4, column=0, sticky="news", pady=20, padx=10)

sector_label = tkinter.Label(sector_frame, text = "Sector")
sector_combobox = ttk.Combobox(sector_frame, values=[ "No Clue", "Technology", "Financial Services", "Consumer Cyclical", "Healthcare", "Communication Services", "Industrials", "Consumer Defensive", "Energy", "Basic Materials", "Real Estate", "Utilities"])
sector_label.grid(row= 0, column=0)
sector_combobox.grid(row=1, column=0, padx=10, pady=10)

# for widget in user_info_frame.winfo_children():
#     widget.grid_configure(padx=10, pady=5)
#
# courses_frame = tkinter.LabelFrame(frame)
# courses_frame.grid(row = 5, column=0, sticky="news", pady=20, padx=10)
#
# registered_label = tkinter.Label(courses_frame, text="Registration Status")
# reg_status_var = tkinter.StringVar("Not Registered")
# registered_check = tkinter.Checkbutton(courses_frame, text="Currently Registered", variable=reg_status_var, onvalue="Registerd", offvalue="Not Registered")
# registered_label.grid(row = 0, column=0)
# registered_check.grid(row =1, column=0, pady=10, padx=10)
#
# numcourses_label = tkinter.Label(courses_frame, text="# Completed Courses")
# numcourses_spinbox = tkinter.Spinbox(courses_frame, from_=0, to='infinity')
# numcourses_label.grid(row = 0, column=1)
# numcourses_spinbox.grid(row = 1, column=1, padx=10, pady=10)
#
# numsemesters_label = tkinter.Label(courses_frame, text="# Semesters")
# numsemesters_spinbox = tkinter.Spinbox(courses_frame, from_=0, to='infinity')
# numsemesters_label.grid(row = 0, column=2)
# numsemesters_spinbox.grid(row = 1, column=2,padx=10, pady=10)

for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

terms_frame = tkinter.LabelFrame(frame, text="Terms and Conditions")
terms_frame.grid(row=5, column=0, sticky="news", padx=20, pady=20)

accept_var = tkinter.StringVar(value="Not Accepted")
terms_check = tkinter.Checkbutton(terms_frame, text="I accept the Terms and Conditions", variable=accept_var, onvalue="Accepted", offvalue="Not Accepted")
terms_check.grid(row=0, column=0)

button = tkinter.Button(frame, text="Enter Data", command=enter_data)
button.grid(row=6, column=0, pady=10, padx=10)

window.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
'''