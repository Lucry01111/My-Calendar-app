# Calendar App 📅

A minimal desktop calendar application written in Python using **Tkinter** and **tkcalendar**, designed to manage daily events with a clean and intuitive interface.

## ⚙️ Features

* **Interactive Calendar**
  Select a date from the calendar to view and manage events for that specific day.

* **Daily Events Management**

  * Add events with a specific **time (HH:MM)** and description
  * View events in a sorted list by time
  * Delete selected events easily

* **Automatic Time Sorting**
  Events are automatically ordered chronologically for better readability.

* **Italian Locale Support 🇮🇹**
  Calendar and dates are displayed in Italian (if the locale is available on the system).

* **Modern UI with Tkinter & ttk**
  Clean layout, custom styles, and intuitive controls for a better user experience.

## 🛠️ Technologies Used

* **Python**
* **Tkinter / ttk** for the GUI
* **tkcalendar** for the calendar widget
* **datetime** for time validation and sorting
* **locale** for Italian date formatting

## 📌 Notes

* Time must be entered in **HH:MM** format.
* Events are stored in memory (they are not saved after closing the app).
