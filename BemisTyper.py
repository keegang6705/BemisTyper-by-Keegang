import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import threading, time, pyautogui, keyboard #os
version = "1.1.0"

class BemisTyperApp(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("BemisTyper"+version+" - Stopped")

        #icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'col_studio.ico')
        #if os.path.exists(icon_path):
        #    self.master.iconbitmap(default=icon_path)

        self.master.geometry("500x400")

        self.text_to_type = ""
        self.running = False
        self.turbo_mode = tk.BooleanVar()
        self.turbo_mode.set(False)
        self.interval_var = tk.StringVar()
        self.interval_var.set("0.01")
        self.loop_var = tk.IntVar()
        self.loop_var.set(1)

        self.master.attributes('-topmost', 1)

        self.column = tk.Label(master, anchor=tk.NW, text="1                  2                  3                  4                  5                  6                  7                  8                  9                  10                11                12                13                14                15                16                17                18                19                20                21                22                23                24                25                26                27                28                29                30")
        self.column.grid(row=0, column=0, columnspan=3, padx=10,sticky=tk.W)

        self.text_entry = ScrolledText(master, width=45, height=10, wrap=tk.WORD)
        self.text_entry.grid(row=1, column=0, columnspan=3, padx=10,sticky="nsew")

        self.import_button = tk.Button(master, text="Import Text File", command=self.import_text_file)
        self.import_button.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

        self.type_each_char_checkbox = tk.Checkbutton(master, text="Turbo mode (if use on slow device, it may cause data errors.)", variable=self.turbo_mode)
        self.type_each_char_checkbox.grid(row=3, column=0, columnspan=3, sticky=tk.W)

        self.interval_label = tk.Label(master, text="Interval (seconds):")
        self.interval_label.grid(row=2, column=1, sticky=tk.E)
        self.interval_entry = tk.Entry(master, textvariable=self.interval_var)
        self.interval_entry.grid(row=2, column=2, sticky=tk.W)


        self.start_stop_button = tk.Button(master, text="Start Typing (F8)", command=self.toggle_start_stop)
        self.start_stop_button.grid(row=4, column=0, columnspan=3,pady=10)


        master.grid_rowconfigure(1, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)
        master.grid_columnconfigure(2, weight=1)

        keyboard.add_hotkey('F8', self.toggle_start_stop)
        self.bind("<B1-Motion>", self.on_resize)
        self.bind("<ButtonRelease-1>", self.stop_resizing)

        # Set the resizing flag to False initially
        self.resizing = False

    def on_resize(self, event):
        if self.resizing:
            # Calculate the new size based on the mouse position
            new_width = self.winfo_pointerx() - self.winfo_rootx()
            new_height = self.winfo_pointery() - self.winfo_rooty()

            # Set the new size for the window
            self.geometry(f"{new_width}x{new_height}")

    def start_resizing(self, event):
        # Set the resizing flag to True
        self.resizing = True

    def stop_resizing(self, event):
        # Set the resizing flag to False
        self.resizing = False

    def import_text_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                self.text_entry.delete(1.0, tk.END)
                self.text_entry.insert(tk.END, file.read())

    def toggle_start_stop(self):
        if not self.running:
            self.text_to_type = self.text_entry.get(1.0, tk.END)
            self.text_entry.config(state=tk.DISABLED)
            self.type_each_char_checkbox.config(state=tk.DISABLED)
            self.interval_entry.config(state=tk.DISABLED)
            self.import_button.config(state=tk.DISABLED)
            self.start_stop_button.config(text="Stop Typing (F8)")
            self.master.title("BemisTyper"+version+" - Running")

            self.loop_count = self.loop_var.get()
            self.running = True

            BemisTyper_thread = threading.Thread(target=self.autotype)
            BemisTyper_thread.start()
        else:
            self.text_entry.config(state=tk.NORMAL)
            self.type_each_char_checkbox.config(state=tk.NORMAL)
            self.interval_entry.config(state=tk.NORMAL)
            self.import_button.config(state=tk.NORMAL)
            self.start_stop_button.config(text="Start Typing (F8)")
            self.master.title("BemisTyper"+version+" - Stopped")

            self.running = False

    def autotype(self):
        text = self.text_to_type[:-1]
        text = text.replace("\n", "\t\t")
        text = text.replace(" ", "\t")
        interval = float(self.interval_var.get())
        for loop in range(self.loop_count):
            if self.turbo_mode.get():
                pyautogui.typewrite(text)
            else:
                for char in text:
                    if not self.running:
                        break

                    if self.turbo_mode.get():
                        pyautogui.typewrite(char)


                    time.sleep(interval)


        self.stop_program()

    def stop_program(self):
        self.text_entry.config(state=tk.NORMAL)
        self.type_each_char_checkbox.config(state=tk.NORMAL)
        self.interval_entry.config(state=tk.NORMAL)
        self.import_button.config(state=tk.NORMAL)
        self.start_stop_button.config(text="Start Typing (F8)")
        self.master.title("BemisTyper"+version+" - Stopped")

        self.running = False

if __name__ == "__main__":
    root = tk.Tk()  # Create an instance of Tk()
    app = BemisTyperApp(master=root)  # Pass Tk() instance as master
    app.mainloop()
