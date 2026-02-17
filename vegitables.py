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
        bg="#27AE60",
        fg="white",
        padx=20,
        pady=10
    )
vegetables = [
    "Carrot", "Potato", "Tomato", "Onion", "Cabbage", "Broccoli",
    "Capsicum", "Cucumber", "Beetroot", "Pumpkin",
    "Fenugreek", "Coriander", "Radish",
    "Sweet Potato", "Garlic", "Ginger", "Brinjal",
    "Lady finger", "Peas", "Mushroom", "Corn"
]




IMAGE_DIR = os.environ.get(
    "IMAGE_DIR",
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "images", "vegitables")
)

print(f"IMAGE_DIR set to: {IMAGE_DIR}")

class VegetableApp:
    def __init__(self, root, main_menu, show_frame):
        self.root = root
        self.main_menu = main_menu  
        self.show_frame_func = show_frame
        self.root.title("Learn Vegetables")
        self.root.state('zoomed')
        #self.root.geometry("450x650") 
        self.root.config(bg="#FFF8E1")  

        style = ttk.Style()
        style.theme_use('clam') 
        self.index = 0

        # Top frame for title and home button
        top_frame = tk.Frame(root, bg="#F4F6F6")
        top_frame.pack(fill="x", padx=20, pady=10)
        
        # Title on the left
        self.app_title = create_title_label(top_frame, "Vegetables")
        self.app_title.pack(in_=top_frame)
        
        
        # Home button on the right
        home_btn = tk.Button(top_frame, text="🏠 Home", command=self.go_home, font=("Comic Sans MS", 16, "bold"), bg="#4A90E2", fg="white", padx=20, pady=10)
        home_btn.pack(side="right")
        
        self.vegetable_label = tk.Label(
            root, 
            text="", 
            font=("Arial", 36, "bold"), 
            bg="#FFF8E1",
            fg="#F57C00" 
        )
        self.vegetable_label.pack(pady=(20, 10))
        
        # Voice button
        self.voice_button = tk.Button(
            root,
            text="🔊Pronounce",
            font=("Arial", 14, "bold"),
            bg="#85C1E9",
            fg="white",
            command=self.speak_vegetable,
            width=20,
            height=1
        )
        self.voice_button.pack(pady=5)

        self.img_label = tk.Label(root, bg="#FFECB3")  
        self.img_label.pack(pady=10, padx=20)

        nav_frame = ttk.Frame(root)
        nav_frame.pack(pady=30)

        self.prev_btn = ttk.Button(
            nav_frame, 
            text="← Previous", 
            command=self.prev_vegetable,
            style='Nav.TButton' 
        )
        self.prev_btn.grid(row=0, column=0, padx=40)

        self.next_btn = ttk.Button(
            nav_frame, 
            text="Next →", 
            command=self.next_vegetable,
            style='Nav.TButton' 
        )
        self.next_btn.grid(row=0, column=1, padx=40)

        style.configure('Nav.TButton', font=('Arial', 14, 'bold'), padding=10)

        
        self.show_vegetable()

    def show_vegetable(self):
        vegetable = vegetables[self.index]
        self.vegetable_label.config(text=vegetable)

        name = vegetable.lower()
        candidates = [
            name.replace(" ", "_"),
            name.replace(" ", "-"),
            name.replace(" ", ""),
            name,
        ]

        img_path = None
        print(f"[DEBUG] show_vegetable: vegetable='{vegetable}'")
        print(f"[DEBUG] IMAGE_DIR = {IMAGE_DIR}")
        if os.path.isdir(IMAGE_DIR):
            files = os.listdir(IMAGE_DIR)
            print(f"[DEBUG] files in IMAGE_DIR ({len(files)}): {files}")
            lower_files = {f.lower(): f for f in files}

            exts = [".jpg", ".jpeg", ".png"]
            for cand in candidates:
                for ext in exts:
                    want = (cand + ext).lower()
                    print(f"[DEBUG] checking exact: {want}")
                    if want in lower_files:
                        img_path = os.path.join(IMAGE_DIR, lower_files[want])
                        print(f"[DEBUG] exact match -> {img_path}")
                        break
                if img_path:
                    break

            if not img_path:
                for cand in candidates:
                    print(f"[DEBUG] checking contains candidate: {cand}")
                    for fname_lower, real_fname in lower_files.items():
                        if cand in fname_lower and os.path.splitext(real_fname)[1].lower() in exts:
                            img_path = os.path.join(IMAGE_DIR, real_fname)
                            print(f"[DEBUG] substring match -> {img_path}")
                            break
                    if img_path:
                        break
        else:
            print(f"Warning: IMAGE_DIR does not exist: {IMAGE_DIR}", file=sys.stderr)

        if img_path:
            try:
                img = Image.open(img_path)
                if img.mode not in ("RGB", "RGBA"):
                    img = img.convert("RGBA")
                img = img.resize((620, 320), Image.Resampling.LANCZOS)  
                self.tk_img = ImageTk.PhotoImage(img, master=self.root)
                self.img_label.config(image=self.tk_img, text="")
                print(f"[DEBUG] Loaded image: {img_path}")
            except Exception as e:
                err_msg = f"Error loading image {img_path}: {e}"
                print(err_msg, file=sys.stderr)
                display_text = "! Image Error !\n" + str(e)
                self.img_label.config(image="", text=display_text, font=("Arial", 12, "italic"), bg="#FFEEEE", fg="#C0392B", justify='center')
        else:
            self.img_label.config(
                image="", 
                text=f"No Image Found:\n'{candidates[0]}.(jpg/png)'", 
                font=("Arial", 14, "italic"),
                width=420, 
                height=420,
                bg="#ECF0F1", 
                fg="#7F8C8D"
            )
            self.tk_img = None 


    def next_vegetable(self):
        self.index = (self.index + 1) % len(vegetables)
        self.show_vegetable()

    def prev_vegetable(self):
        self.index = (self.index - 1) % len(vegetables)
        self.show_vegetable()
    
    def speak_vegetable(self):
        # Initialize the text-to-speech engine
        try:
            # Initialize engine without creating extra window
            engine = pyttsx3.init()
            
            # Set speech properties
            rate = engine.getProperty('rate')
            engine.setProperty('rate', 150)  # Speed of speech
            volume = engine.getProperty('volume')
            engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)
            
            # Get the current vegetable and speak it
            current_vegetable = vegetables[self.index]
            engine.say(current_vegetable)
            engine.runAndWait()
        except Exception as e:
            print(f"Error with text-to-speech: {e}")

    def go_home(self):
        if hasattr(self, 'show_frame_func') and self.show_frame_func and hasattr(self, 'main_menu') and self.main_menu:
            self.root.destroy()
            self.show_frame_func(self.main_menu)
        else:
            self.root.destroy()

def run(parent_root, main_menu, show_frame):
    toplevel = tk.Toplevel(parent_root)
    app = VegetableApp(toplevel, main_menu, show_frame)

"""
if __name__ == '__main__':
    run()
"""