import tkinter as tk
from tkinter import ttk 
from PIL import Image, ImageTk 
import os
import sys
import pyttsx3

def create_title_label(parent, text):
    return tk.Label(
        parent,
        text=text,
        font=("Helvetica", 24, "bold"),
        bg="#BA2604",  
        fg="#ECF0F1", 
        pady=10
    )


Months = [
    "January", "February", "March", "April", 
    "May", "June", "July","August","September","October","November","December"
] 





IMAGE_DIR = r"D:/vvd/images/months"


print(f"Looking for images in: {IMAGE_DIR}")

class MonthsApp:
    def __init__(self, root, main_menu, show_frame):
        self.root = root
        self.main_menu = main_menu
        self.show_frame = show_frame
        self.root.title("Learn Months in Year")
        self.root.state('zoomed') 

       #self.root.geometry("450x650")
        self.root.config(bg="#F4F6F6")
        
        style = ttk.Style()
        style.theme_use('clam')

        self.index = 0
        self.tk_img = None 

        self.app_title = create_title_label(root, "Months in Year")
        self.app_title.pack(fill='x')

        self.month_label = tk.Label(
            root, text="", font=("Arial", 36, "bold"), 
            bg="#F4F6F6", fg="#BA2604"
        )
        self.month_label.pack(pady=(20, 10))

        self.img_label = tk.Label(root, bg="#BDC3C7")
        self.img_label.pack(pady=10, padx=20)

        self.voice_button = tk.Button(
            root,
            text="🔊",
            font=("Arial", 14, "bold"),
            bg="#85C1E9",
            fg="white",
            command=self.speak_month,
            width=20,
            height=2
        )
        self.voice_button.pack(pady=10)

        # Add hover effect to voice button
        def voice_on_enter(e):
            self.voice_button.config(bg="#5DADE2", relief="sunken")
            
        def voice_on_leave(e):
            self.voice_button.config(bg="#85C1E9", relief="raised")
        
        self.voice_button.bind("<Enter>", voice_on_enter)
        self.voice_button.bind("<Leave>", voice_on_leave)

        nav_frame = ttk.Frame(root)
        nav_frame.pack(pady=30)

        self.prev_btn = ttk.Button(nav_frame, text="⏮ Prev", command=self.prev_month, style='Nav.TButton')
        self.prev_btn.grid(row=0, column=0, padx=40)

        self.next_btn = ttk.Button(nav_frame, text="Next ⏭", command=self.next_month, style='Nav.TButton')
        self.next_btn.grid(row=0, column=1, padx=40)

        style.configure('Nav.TButton', font=('Arial', 14, 'bold'), padding=10)

        home_btn = tk.Button(root, text="🏠 Home", command=self.go_home, font=("Arial", 14, "bold"), bg="#4A90E2", fg="white", padx=20, pady=10)
        home_btn.pack(pady=10)

        self.show_months()

    def show_months(self):
        current_month = Months[self.index]
        self.month_label.config(text=current_month)

        name = current_month.lower()
        candidates = [
            name,
            name.replace(" ", "_"),
            name.replace(" ", "-"),
            name.replace(" ", "")
        ]

        img_path = None
        
        if os.path.exists(IMAGE_DIR):
            files = os.listdir(IMAGE_DIR)
            lower_files = {f.lower(): f for f in files}
            
            exts = [".jpg", ".jpeg", ".png"]

            for cand in candidates:
                for ext in exts:
                    want = (cand + ext).lower()
                    if want in lower_files:
                        img_path = os.path.join(IMAGE_DIR, lower_files[want])
                        break
                if img_path: break
            
            if not img_path:
                for cand in candidates:
                    for fname_lower, real_fname in lower_files.items():
                        if cand in fname_lower and any(fname_lower.endswith(ext) for ext in exts):
                            img_path = os.path.join(IMAGE_DIR, real_fname)
                            break
                    if img_path: break
        else:
            print(f"ERROR: The folder {IMAGE_DIR} does not exist!")

        if img_path:
            try:
                img = Image.open(img_path)
                if img.mode not in ("RGB", "RGBA"):
                    img = img.convert("RGBA")
                img = img.resize((750, 350))
                self.tk_img = ImageTk.PhotoImage(img, master=self.root)
                self.img_label.config(image=self.tk_img, text="")
                print(f"Loaded: {img_path}")
            except Exception as e:
                self.img_label.config(image="", text=f"Error loading image:\n{e}", bg="#FFEEEE", fg="red")
        else:
            self.img_label.config(
                image="", 
                text=f"Image Not Found\nLooking for: {current_month}\n(Check folder: {IMAGE_DIR})",
                bg="#ECF0F1", fg="gray", font=("Arial", 12), width=40, height=15
            )
            self.tk_img = None

    def next_month(self):
        self.index = (self.index + 1) % len(Months)
        self.show_months()

    def prev_month(self):
        self.index = (self.index - 1) % len(Months)
        self.show_months()

    def go_home(self):
        self.root.destroy()
        self.show_frame(self.main_menu)
    
    def speak_month(self):
        # Initialize the text-to-speech engine
        try:
            engine = pyttsx3.init()
            
            # Set speech properties
            rate = engine.getProperty('rate')
            engine.setProperty('rate', 150)  # Speed of speech
            volume = engine.getProperty('volume')
            engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)
            
            # Get the current animal and speak it
            current_monthvoice = Months[self.index]
            engine.say(f" {current_monthvoice}")
            engine.runAndWait()
        except Exception as e:
            print(f"Error with text-to-speech: {e}")

def run(parent_root, main_menu, show_frame):
    toplevel = tk.Toplevel(parent_root)
    app = MonthsApp(toplevel, main_menu, show_frame)

#if __name__ == '__main__':
#    run()