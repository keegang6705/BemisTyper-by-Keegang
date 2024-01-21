import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import threading
import time
import pyautogui
import keyboard
import os

class AutoTyperApp:
    def __init__(self, master):
        self.master = master
        self.master.title("BemisTyper by keegang - Stopped")

        icon_path = r"D:\keegang project\code\python\helpfull_program\be-mis proj\col_studio.ico"
        if os.path.exists(icon_path):
            self.master.iconbitmap(default=icon_path)

        # Set the window size to 600x900
        self.master.geometry("500x300")

        # Autotyper variables
        self.text_to_type = ""
        self.running = False
        self.type_each_character = tk.BooleanVar()
        self.type_each_character.set(True)  # Set default to True
        self.interval_var = tk.StringVar()
        self.interval_var.set("0.01")  # Set default interval to 0.01
        self.loop_var = tk.IntVar()
        self.loop_var.set(1)  # Default loop count

        # Set the window to be always on top
        self.master.attributes('-topmost', 1)

        # Add a scrolled text field for the text to type (spanning two columns)
        self.text_entry = ScrolledText(master, width=45, height=10, wrap=tk.WORD)
        self.text_entry.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Add a button to open a file dialog for importing text file (Column 1)
        self.import_button = tk.Button(master, text="Import Text File", command=self.import_text_file)
        self.import_button.grid(row=1, column=0, padx=10, pady=0, sticky=tk.W)  # Pack to the left in Column 1

        # Add an entry widget for the typing interval (Column 2)
        self.interval_label = tk.Label(master, text="Interval (seconds):")
        self.interval_label.grid(row=1, column=1, padx=10, pady=0, sticky=tk.E)  # Pack to the right in Column 2
        self.interval_entry = tk.Entry(master, textvariable=self.interval_var)
        self.interval_entry.grid(row=1, column=2, padx=10, pady=0, sticky=tk.W)  # Pack to the left in Column 2

        # Add a start/stop button (spanning two columns)
        self.start_stop_button = tk.Button(master, text="Start Typing (F8)", command=self.toggle_start_stop)
        self.start_stop_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

                # Configure row and column weights to make the grid stretch
        for i in range(3):  # Adjust the range based on your layout
            master.grid_rowconfigure(i, weight=1)
            master.grid_columnconfigure(i, weight=1)

        # Bind F8 key to the toggle_start_stop method
        keyboard.add_hotkey('F8', self.toggle_start_stop)

    def import_text_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                self.text_entry.delete(1.0, tk.END)  # Clear existing text
                self.text_entry.insert(tk.END, file.read())

    def toggle_start_stop(self):
        if not self.running:
            # Get the text to type
            self.text_to_type = self.text_entry.get(1.0, tk.END)  # Get all text from the ScrolledText widget

            # Disable the text entry and update the button and window title
            self.text_entry.config(state=tk.DISABLED)

            self.interval_entry.config(state=tk.DISABLED)
            self.import_button.config(state=tk.DISABLED)

            self.start_stop_button.config(text="Stop Typing (F8)")
            self.master.title("BemisTyper by keegang - Running")

            # Set loop count and start the autotyper in a separate thread
            self.loop_count = self.loop_var.get()
            self.running = True
            autotyper_thread = threading.Thread(target=self.autotype)
            autotyper_thread.start()
        else:
            # Enable the text entry and update the button and window title
            self.text_entry.config(state=tk.NORMAL)
            self.interval_entry.config(state=tk.NORMAL)
            self.import_button.config(state=tk.NORMAL)
            self.start_stop_button.config(text="Start Typing (F8)")
            self.master.title("BemisTyper by keegang - Stopped")

            self.running = False

    def autotype(self):
        interval = float(self.interval_var.get())
        for loop in range(self.loop_count):
            for char in self.text_to_type[:-1]:
                if not self.running:
                    break

                if self.type_each_character.get():
                    if char == '\n':
                        pyautogui.press('tab')
                        pyautogui.press('tab')
                    else:
                        pyautogui.typewrite(char)
                else:
                    pyautogui.typewrite(self.text_to_type)

                time.sleep(interval)

            # Update the loop count label

        # Stop the program after completing the specified number of loops
        self.stop_program()

    def stop_program(self):
        # Enable the text entry and update the button and window title
        self.text_entry.config(state=tk.NORMAL)
        self.interval_entry.config(state=tk.NORMAL)
        self.import_button.config(state=tk.NORMAL)
        self.start_stop_button.config(text="Start Typing (F8)")
        self.master.title("BemisTyper by keegang - Stopped")

        self.running = False

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoTyperApp(root)
    root.mainloop()
