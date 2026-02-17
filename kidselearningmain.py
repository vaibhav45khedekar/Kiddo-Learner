import tkinter as tk
from PIL import Image, ImageTk
from module import alphabet, numbers, colors, animals, Opp_Syn, fruits, vegitables, days, months, birds, image_quiz, shapes

#from ui_components import title_label
import os

def launch_module(root, main_menu, show_frame, module):
   
    try:
        module.run(root, main_menu, show_frame)
    except TypeError:
       
        try:
            module.run(root=root)
        except TypeError:
           
            module.run()

def show_frame(frame):
    frame.tkraise()

def main():
    root = tk.Tk()
    root.title("Kiddo Learner")
 #   root.geometry("520x500")
    root.state('zoomed')  
    root.config(bg="#4A90E2")  
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    main_menu = tk.Frame(root, bg="#4A90E2")
    main_menu.grid(row=0, column=0, sticky="nsew")


    bg_path = os.path.join(os.path.dirname(__file__), "images", "bg.jpg")
    bg_img = Image.open(bg_path)
    bg_img = bg_img.resize((1920, 1080), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_img)
    bg_label = tk.Label(main_menu, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.grid(row=0, column=0, rowspan=7, columnspan=2, sticky="nsew")

    title = tk.Label(main_menu, text="📚 Welcome KIDDO LEARNER", font=("Comic Sans MS", 24, "bold"), bg="#4A90E2", fg="#FFFFFF")
    title.grid(row=0, column=0, columnspan=2, pady=20)

    btn_style = {
        "width": 20,
        "height": 2,
        "font": ("Comic Sans MS", 16, "bold"),
        "bd": 0,
        "activebackground": "#F8F8F7",
        "fg": "#333",
        "cursor": "hand2",
        "relief": "ridge"
    }

    tk.Button(main_menu, text="🔤 Learn Alphabet", bg="#FFD700", command=lambda: launch_module(root, main_menu, show_frame, alphabet), **btn_style).grid(row=1, column=0, padx=20, pady=10)
    tk.Button(main_menu, text="🔢 Learn Numbers", bg="#FFB347", command=lambda: launch_module(root, main_menu, show_frame, numbers), **btn_style).grid(row=1, column=1, padx=20, pady=10)
    tk.Button(main_menu, text="🎨 Learn Colors", bg="#77DD77", command=lambda: launch_module(root, main_menu, show_frame, colors), **btn_style).grid(row=3, column=0, padx=20, pady=10)
    tk.Button(main_menu, text="🦁 Learn Animals", bg="#FF6961", command=lambda: launch_module(root, main_menu, show_frame, animals), **btn_style).grid(row=2, column=1, padx=20, pady=10)
    tk.Button(main_menu, text="📝 Take a Quiz", bg="#84B6F4", command=lambda: launch_module(root, main_menu, show_frame, image_quiz), **btn_style).grid(row=6, column=1, padx=20, pady=10)
    tk.Button(main_menu, text="🔄 Opposites & Synonyms", bg="#C49CDE", command=lambda: launch_module(root, main_menu, show_frame, Opp_Syn), **btn_style).grid(row=3, column=1, padx=20, pady=10)
    
    tk.Button(main_menu, text="🍎 Learn Fruits", bg="#FF6F61", command=lambda: launch_module(root, main_menu, show_frame, fruits), **btn_style).grid(row=4, column=0, padx=20, pady=10)
    tk.Button(main_menu, text="🥦 Learn Vegetables", bg="#469608", command=lambda: launch_module(root, main_menu, show_frame, vegitables), **btn_style).grid(row=4, column=1, padx=20, pady=10)
    tk.Button(main_menu, text="🐦 Learn Birds", bg="#E8EFE3", command=lambda: launch_module(root, main_menu, show_frame, birds), **btn_style).grid(row=2, column=0, padx=20, pady=10)
    tk.Button(main_menu, text="🔷 Learn Shapes", bg="#1178A4", command=lambda: launch_module(root, main_menu, show_frame, shapes), **btn_style).grid(row=6, column=0, padx=20, pady=10)
    tk.Button(main_menu, text="📆 Learn Months", bg="#E32698", command=lambda: launch_module(root, main_menu, show_frame, months), **btn_style).grid(row=5, column=1, padx=20, pady=10)
    tk.Button(main_menu, text="📅 Learn Days", bg="#FF7F50", command=lambda: launch_module(root, main_menu, show_frame, days), **btn_style).grid(row=5, column=0, padx=20, pady=10)

   # tk.Button(main_menu, text="🖼️ Image Quiz", bg="#F4A460", command=lambda: launch_module(root, main_menu, show_frame, image_quiz), **btn_style).grid(row=7, column=0, columnspan=2, padx=20, pady=10)
    main_menu.grid_columnconfigure(0, weight=1)
    main_menu.grid_columnconfigure(1, weight=1)

    for i in range(7):
        main_menu.grid_rowconfigure(i, weight=1)

    show_frame(main_menu)
    root.mainloop()

if __name__ == "__main__":
    main()