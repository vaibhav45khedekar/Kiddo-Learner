import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
try:
    # When imported as part of the package
    from .ui_components import title_label
except Exception:
    # When run directly (module executed as script), fall back to absolute import
    try:
        from module.ui_components import title_label
    except Exception:
        # Last-resort: try import from local file (same folder)
        from ui_components import title_label

# Centralized theme for colors used in this module
THEME = {
    "BG": "#FFF7F3",
    "HEADER_BG": "#FF69B4",
    "HEADER_TEXT": "#FFFFFF",
    "CARD_BG": "#FFFFFF",
    "ROW_ALT": "#F4F6F8",
    "TEXT": "#2c3e50",
    "OPPOSITE": "#E74C3C",
    "SYNONYM": "#27AE60",
    "HEADER1": "#3498DB",
    "HEADER2": "#E74C3C",
    "HEADER3": "#2ECC71",
    "INFO_BG": "#34495E",
    "BORDER": "#DDDDDD"
}

def run(root=None, main_menu=None, show_frame=None):
    if root:
        win = tk.Toplevel(root)
    else:
        # When run standalone, create a root window instead of a Toplevel
        win = tk.Tk()
    win.title("Learn Opposite & Synonyms Words")
   
    win.state('zoomed')  
    win.config(bg=THEME["BG"])

    title_frame = tk.Frame(win, bg=THEME["HEADER_BG"], height=100)
    title_frame.pack(fill="x", pady=(0, 30))
    title_frame.pack_propagate(False)
    
    title_font = font.Font(family="Arial", size=32, weight="bold")
    tk.Label(
        title_frame, text="🔤 Opposite & Synonymous Words",
        font=title_font, bg=THEME["HEADER_BG"], fg=THEME["HEADER_TEXT"]
    ).pack(expand=True)

    words = [
        {"word": "Happy", "img": "happy.png", "opposite": "Sad", "opposite_img": "sad.png", "synonym": "Joyful", "synonym_img": "joyful.png"},
        {"word": "Big", "img": "big.png", "opposite": "Small", "opposite_img": "small.png", "synonym": "Large", "synonym_img": "large.png"},
        {"word": "Fast", "img": "fast.png", "opposite": "Slow", "opposite_img": "slow.png", "synonym": "Quick", "synonym_img": "quick.png"},
        {"word": "Hot", "img": "hot.png", "opposite": "Cold", "opposite_img": "cold.png", "synonym": "Scorching", "synonym_img": "hot.png"},
        {"word": "Beautiful", "img": "beautiful.png", "opposite": "Ugly", "opposite_img": "ugly.png", "synonym": "Pretty", "synonym_img": "pretty.png"},
        {"word": "Strong", "img": "strong.png", "opposite": "Weak", "opposite_img": "weak.png", "synonym": "Powerful", "synonym_img": "powerful.png"},
        {"word": "Light", "img": "happy.png", "opposite": "Dark", "opposite_img": "ugly.png", "synonym": "Bright", "synonym_img": "happy.png"},
        {"word": "Easy", "img": "big.png", "opposite": "Difficult", "opposite_img": "small.png", "synonym": "Simple", "synonym_img": "big.png"},
        {"word": "High", "img": "fast.png", "opposite": "Low", "opposite_img": "slow.png", "synonym": "Tall", "synonym_img": "fast.png"},
    ]

    main_container = tk.Frame(win, bg=THEME["BG"])
    main_container.pack(fill="both", expand=True, padx=40, pady=(0, 30))
    
    canvas = tk.Canvas(main_container, bg=THEME["BG"], highlightthickness=0)
    scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f0f4f8")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Table frame with modern styling
    frame = tk.Frame(scrollable_frame, bg=THEME["CARD_BG"], relief="raised", bd=3)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Enhanced headers with icons and colors
    header_font = font.Font(family="Arial", size=20, weight="bold")
    headers_config = [
        {"text": "📝 Word", "bg": THEME["HEADER1"], "colspan": 2},
        {"text": "⚡ Opposite", "bg": THEME["HEADER2"], "colspan": 2},
        {"text": "✨ Synonym", "bg": THEME["HEADER3"], "colspan": 2}
    ]
    
    col_index = 0
    for header in headers_config:
        header_label = tk.Label(
            frame, text=header["text"], font=header_font,
            bg=header["bg"], fg=THEME["HEADER_TEXT"], padx=25, pady=20
        )
        header_label.grid(row=0, column=col_index, columnspan=header["colspan"], 
                         sticky="nsew", padx=2, pady=2)
        col_index += header["colspan"]

    # Store image references to prevent garbage collection
    images = []
    
    # Custom fonts for better readability
    word_font = font.Font(family="Arial", size=18, weight="bold")
    
    for row, entry in enumerate(words, start=1):
        # Alternating row colors for better readability
        row_bg = THEME["ROW_ALT"] if row % 2 == 0 else THEME["CARD_BG"]
        
        # Word section with enhanced styling
        word_label = tk.Label(
            frame, text=entry["word"], font=word_font,
            bg=row_bg, fg=THEME["TEXT"], padx=25, pady=25,
            anchor="center", width=12
        )
        word_label.grid(row=row, column=0, sticky="nsew", padx=2, pady=2)

        # Word image with border effect - LARGER SIZE
        try:
            img_path = f"images/{entry['img']}"
            img = Image.open(img_path).resize((120, 120), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            images.append(photo)
            img_label = tk.Label(frame, image=photo, bg=row_bg, relief="solid", bd=2)
            img_label.grid(row=row, column=1, padx=15, pady=15)
        except:
            # Fallback if image not found
            tk.Label(frame, text="📷", font=("Arial", 50), bg=row_bg).grid(row=row, column=1, padx=15, pady=15)

        # Opposite word section
        opposite_label = tk.Label(
            frame, text=entry["opposite"], font=word_font,
            bg=row_bg, fg=THEME["OPPOSITE"], padx=25, pady=25,
            anchor="center", width=12
        )
        opposite_label.grid(row=row, column=2, sticky="nsew", padx=2, pady=2)
        
        try:
            opp_img_path = f"images/{entry['opposite_img']}"
            opp_img = Image.open(opp_img_path).resize((120, 120), Image.Resampling.LANCZOS)
            opp_photo = ImageTk.PhotoImage(opp_img)
            images.append(opp_photo)
            opp_img_label = tk.Label(frame, image=opp_photo, bg=row_bg, relief="solid", bd=2)
            opp_img_label.grid(row=row, column=3, padx=15, pady=15)
        except:
            tk.Label(frame, text="📷", font=("Arial", 50), bg=row_bg).grid(row=row, column=3, padx=15, pady=15)

        # Synonym word section
        synonym_label = tk.Label(
            frame, text=entry["synonym"], font=word_font,
            bg=row_bg, fg=THEME["SYNONYM"], padx=25, pady=25,
            anchor="center", width=12
        )
        synonym_label.grid(row=row, column=4, sticky="nsew", padx=2, pady=2)
        
        try:
            syn_img_path = f"images/{entry['synonym_img']}"
            syn_img = Image.open(syn_img_path).resize((120, 120), Image.Resampling.LANCZOS)
            syn_photo = ImageTk.PhotoImage(syn_img)
            images.append(syn_photo)
            syn_img_label = tk.Label(frame, image=syn_photo, bg=row_bg, relief="solid", bd=2)
            syn_img_label.grid(row=row, column=5, padx=15, pady=15)
        except:
            tk.Label(frame, text="📷", font=("Arial", 50), bg=row_bg).grid(row=row, column=5, padx=15, pady=15)
    
    # Information footer
    info_frame = tk.Frame(scrollable_frame, bg=THEME["INFO_BG"], height=80)
    info_frame.pack(fill="x", pady=(30, 0))
    info_frame.pack_propagate(False)
    
    info_font = font.Font(family="Arial", size=14, slant="italic")
    tk.Label(
        info_frame, 
        text="💡 Tip: Opposite words have opposite meanings, while synonyms have similar meanings!",
        font=info_font, bg=THEME["INFO_BG"], fg=THEME["HEADER_TEXT"]
    ).pack(expand=True)

    # Keep a reference to images to avoid garbage collection
    win.images = images
if __name__ == '__main__':
    run()
