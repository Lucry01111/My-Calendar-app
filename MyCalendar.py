import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
import datetime
import locale


class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendario")
        self.root.geometry("760x430")
        self.root.configure(bg="#f5f6f7")

        # Stile
        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure("TFrame", background="#f5f6f7")
        style.configure("TLabel", background="#f5f6f7", font=("Segoe UI", 11))
        style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("TEntry", font=("Segoe UI", 10))
        style.configure("TSeparator", background="#d1d5db")

        try:
            locale.setlocale(locale.LC_TIME, "it_IT")
        except locale.Error:
            messagebox.showerror("Errore Locale", "Italiano locale non disponibile")

        # Dizionario eventi: {"YYYY-MM-DD": [(orario, descrizione)]}
        self.events = {}

        main = ttk.Frame(self.root, padding=15)
        main.pack(fill=tk.BOTH, expand=True)

        # Calendario a sinistra
        left = ttk.Frame(main)
        left.pack(side=tk.LEFT, padx=(0, 15))

        ttk.Label(left, text="📅 Calendario", style="Title.TLabel").pack(anchor="w", pady=(0, 8))

        self.cal = Calendar(
            left,
            selectmode="day",
            locale="it_IT",
            date_pattern="yyyy-mm-dd",
            font=("Segoe UI", 14),         
            headersfont=("Segoe UI", 13, "bold"),  
            weekendfont=("Segoe UI", 14),
            showweeknumbers=False
        )
        self.cal.pack(padx=10, pady=10)

        # Eventi a destra
        right = ttk.Frame(main)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(right, text="🕒 Eventi del giorno", style="Title.TLabel").pack(anchor="w", pady=(0, 8))

        # Listbox 
        list_frame = ttk.Frame(right)
        list_frame.pack(fill=tk.BOTH, expand=True)

        self.event_listbox = tk.Listbox(
            list_frame,
            height=12,
            font=("Segoe UI", 11),
            bd=0,
            highlightthickness=1,
            highlightbackground="#d1d5db",
            selectbackground="#3b82f6",
            activestyle="none"
        )
        self.event_listbox.pack(fill=tk.BOTH, expand=True)

        # Inserimento eventi
        add_frame = ttk.Frame(right)
        add_frame.pack(fill=tk.X, pady=10)

        self.time_entry = ttk.Entry(add_frame, width=7)
        self.time_entry.pack(side=tk.LEFT, padx=(0, 8))
        self.time_entry.insert(0, "HH:MM")
        self.time_entry.configure(foreground="#6b7280")

        self.time_entry.bind("<FocusIn>", self._clear_time_placeholder)
        self.time_entry.bind("<FocusOut>", self._restore_time_placeholder)

        self.event_entry = ttk.Entry(add_frame)
        self.event_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Button(
            add_frame,
            text="➕ Aggiungi",
            command=self.add_event
        ).pack(side=tk.LEFT, padx=8)

        ttk.Separator(right).pack(fill=tk.X, pady=6)

        ttk.Button(
            right,
            text="🗑 Elimina selezionato",
            command=self.delete_event
        ).pack(fill=tk.X)

        self.cal.bind("<<CalendarSelected>>", self.load_events)
        self.load_events()

    def _clear_time_placeholder(self, event):
        if self.time_entry.get() == "HH:MM":
            self.time_entry.delete(0, tk.END)
            self.time_entry.configure(foreground="black")

    def _restore_time_placeholder(self, event):
        if not self.time_entry.get():
            self.time_entry.insert(0, "HH:MM")
            self.time_entry.configure(foreground="#6b7280")

    # Funzioni eventi
    def load_events(self, event=None):
        self.event_listbox.delete(0, tk.END)
        date = self.cal.get_date()

        if date in self.events:
            events_sorted = sorted(
                self.events[date],
                key=lambda x: datetime.datetime.strptime(x[0], "%H:%M")
            )

            for time, text in events_sorted:
                self.event_listbox.insert(tk.END, f"{time}  •  {text}")

    def add_event(self):
        date = self.cal.get_date()
        time = self.time_entry.get().strip()
        text = self.event_entry.get().strip()

        if time == "HH:MM":
            messagebox.showerror("Errore", "Inserisci un orario")
            return

        try:
            datetime.datetime.strptime(time, "%H:%M")
        except ValueError:
            messagebox.showerror("Errore", "Formato orario non valido (HH:MM)")
            return

        if not text:
            messagebox.showwarning("Attenzione", "Inserisci un evento")
            return

        self.events.setdefault(date, []).append((time, text))

        self.time_entry.delete(0, tk.END)
        self.event_entry.delete(0, tk.END)
        self._restore_time_placeholder(None)

        self.load_events()

    def delete_event(self):
        date = self.cal.get_date()
        sel = self.event_listbox.curselection()

        if not sel or date not in self.events:
            return

        index = sel[0]
        events_sorted = sorted(
            self.events[date],
            key=lambda x: datetime.datetime.strptime(x[0], "%H:%M")
        )

        self.events[date].remove(events_sorted[index])

        if not self.events[date]:
            del self.events[date]

        self.load_events()

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
