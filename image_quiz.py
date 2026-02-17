import tkinter as tk
from tkinter import ttk, messagebox
import random
import os
from PIL import Image, ImageTk


class ImageQuizApp:
    def __init__(self, root, main_menu=None, show_frame=None):
        self.root = root
        self.main_menu = main_menu
        self.show_frame = show_frame

        # ---------------- QUIZ DATA ----------------
        self.quiz_data = [
            {"image": "tiger", "options": ["Tiger", "Lion", "Cat", "Dog"], "correct": "Tiger",
             "explanation": "This is a tiger! Tigers have orange fur with black stripes."},

            {"image": "lion", "options": ["Lion", "Tiger", "Cat", "Bear"], "correct": "Lion",
             "explanation": "This is a lion! Lions are called the king of the jungle."},

            {"image": "cat", "options": ["Cat", "Dog", "Rabbit", "Mouse"], "correct": "Cat",
             "explanation": "This is a cat! Cats say meow."},

            {"image": "dog", "options": ["Dog", "Cat", "Cow", "Horse"], "correct": "Dog",
             "explanation": "This is a dog! Dogs say woof woof."},

            {"image": "elephant", "options": ["Elephant", "Hippo", "Rhino", "Cow"], "correct": "Elephant",
             "explanation": "This is an elephant! Elephants have long trunks."},

            {"image": "apple", "options": ["Apple", "Banana", "Orange", "Grape"], "correct": "Apple",
             "explanation": "This is an apple! Apples are sweet."},

            {"image": "banana", "options": ["Banana", "Apple", "Pear", "Orange"], "correct": "Banana",
             "explanation": "This is a banana! Bananas are yellow."},

            {"image": "carrot", "options": ["Carrot", "Tomato", "Potato", "Cucumber"], "correct": "Carrot",
             "explanation": "This is a carrot! Carrots are orange."},

            {"image": "ball", "options": ["Ball", "Cube", "Cone", "Box"], "correct": "Ball",
             "explanation": "This is a ball! Balls are round."},

            {"image": "car", "options": ["Car", "Bus", "Truck", "Train"], "correct": "Car",
             "explanation": "This is a car! Cars drive on roads."}
        ]

        random.shuffle(self.quiz_data)
        self.total_questions = min(10, len(self.quiz_data))
        self.questions = self.quiz_data[:self.total_questions]

        self.current_index = 0
        self.score = 0
        self.selected_answer = None

        self.setup_ui()
        self.load_question()

    # ---------------- UI SETUP ----------------
    def setup_ui(self):
        self.root.title("It's Test Time")
        self.root.state("zoomed")
        self.root.configure(bg="#FFE4E1")

        # Header
        header = tk.Frame(self.root, bg="#FF69B4", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text="🌟 Test Time 🌟",
            font=("Arial", 26, "bold"), bg="#FF69B4", fg="white"
        ).pack(side="left", padx=20)

        tk.Button(
            header, text="🏠 Home", font=("Arial", 14, "bold"),
            bg="#FF6B6B", fg="white", command=self.go_home
        ).pack(side="right", padx=20)

        # Progress
        info = tk.Frame(self.root, bg="#FFE4E1")
        info.pack(fill="x", pady=5)

        self.progress_label = tk.Label(info, font=("Arial", 16), bg="#FFE4E1", fg="#FF69B4")
        self.progress_label.pack(side="left", padx=20)

        self.score_label = tk.Label(info, font=("Arial", 16), bg="#FFE4E1", fg="#FF69B4")
        self.score_label.pack(side="right", padx=20)

        # Content
        self.content = tk.Frame(self.root, bg="#FFE4E1")
        self.content.pack(fill="both", expand=True)

        self.image_label = tk.Label(
            self.content, bg="white", relief="solid", borderwidth=2
        )
        # Use a fixed image box so the image cannot grow and push options off-screen
        self.image_label.pack(padx=40, pady=20)
        self.image_label.config(width=600, height=300)

        tk.Label(
            self.content, text="What do you see?",
            font=("Arial", 22, "bold"), bg="#FFE4E1"
        ).pack(pady=10)

        # Options - 2 per row layout
        self.options_frame = tk.Frame(self.content, bg="#FFE4E1")
        self.options_frame.pack()

        self.option_buttons = []
        
        # Create two rows with 2 buttons each
        for row in range(2):
            row_frame = tk.Frame(self.options_frame, bg="#FFE4E1")
            row_frame.pack(pady=3)
            
            for col in range(2):
                idx = row * 2 + col
                btn = tk.Button(
                    row_frame, font=("Arial", 18, "bold"),
                    bg="#87CEEB", fg="white", width=12, height=2,
                    command=lambda i=idx: self.select_option(i)
                )
                btn.pack(side="left", padx=10)
                self.option_buttons.append(btn)


        self.feedback_label = tk.Label(
            self.content, font=("Arial", 18),
            wraplength=900, bg="#FFE4E1"
        )
        self.feedback_label.pack(pady=10)


    # ---------------- LOAD QUESTION ----------------
    def load_question(self):
        # Cancel any pending auto-next when loading a new question
        if hasattr(self, '_auto_next_id') and self._auto_next_id:
            self.root.after_cancel(self._auto_next_id)
        
        q = self.questions[self.current_index]

        self.progress_label.config(
            text=f"Question {self.current_index + 1} / {self.total_questions}"
        )
        self.score_label.config(text=f"Score: {self.score}")

        self.load_image(q["image"])

        options = q["options"].copy()
        random.shuffle(options)

        for i, btn in enumerate(self.option_buttons):
            btn.config(text=options[i], state="normal", bg="#87CEEB")

        self.selected_answer = None
        self.selected_button_index = None
        self.feedback_label.config(text="")
        # Clear any previous selection
        for btn in self.option_buttons:
            btn.config(bg="#87CEEB")
        # No navigation buttons to hide
        
        # Clear auto progression flags
        self._auto_submit_in_progress = False
        self._auto_progress_scheduled = False
        self._auto_progressing = False

    # ---------------- IMAGE LOADER ----------------
    def load_image(self, image_name):
        base = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images")
        found = False
        clean = image_name.lower().replace(" ", "")

        for root, _, files in os.walk(base):
            for f in files:
                name = f.lower().replace("_", "").replace("-", "")
                if clean in name and f.lower().endswith((".jpg", ".png", ".jpeg")):
                    path = os.path.join(root, f)
                    img = Image.open(path)
                    # Constrain images to fit inside a 900x300 box so UI controls stay visible
                    img.thumbnail((600, 300), Image.Resampling.LANCZOS)

                    # Paste the thumbnail onto a white background of exact size (900x300)
                    bg = Image.new('RGB', (600, 300), (255, 255, 255))
                    x = (600 - img.width) // 2
                    y = (300 - img.height) // 2
                    bg.paste(img, (x, y))

                    self.photo = ImageTk.PhotoImage(bg)
                    self.image_label.config(image=self.photo, text="")
                    found = True
                    break
            if found:
                break

        if not found:
            self.image_label.config(
                image="",
                text=f"No image for {image_name}",
                font=("Arial", 22, "bold"), fg="red"
            )

    # ---------------- LOGIC ----------------
    def select_option(self, idx):
        # Prevent multiple selections during auto-progress
        if hasattr(self, '_auto_progressing') and self._auto_progressing:
            return
            
        for i, btn in enumerate(self.option_buttons):
            btn.config(bg="#FFD700" if i == idx else "#87CEEB")
        self.selected_answer = self.option_buttons[idx].cget("text")
        self.selected_button_index = idx
        
        # Automatically submit after selection for continuous flow
        # This makes it more like a mock test where you move through questions continuously
        if not hasattr(self, '_auto_submit_in_progress') or not self._auto_submit_in_progress:
            self._auto_submit_in_progress = True
            self._auto_submit_id = self.root.after(2000, self.auto_submit)  # Auto-submit after 500ms
        
    def auto_submit(self):
        # Clear the auto-submit ID to avoid canceling after execution
        if hasattr(self, '_auto_submit_id'):
            self._auto_submit_id = None
        
        if self.selected_answer and not (hasattr(self, '_auto_progress_scheduled') and self._auto_progress_scheduled):
            self.check_answer()

    def check_answer(self):
        if not self.selected_answer:
            messagebox.showwarning("Select option", "Please select an answer 😊")
            self._auto_submit_in_progress = False
            return

        # Validate answer against original correct answer
        correct_answer = self.questions[self.current_index]["correct"]
        
        # Check if selected answer matches the correct answer
        is_correct = self.selected_answer == correct_answer
        
        if is_correct:
            self.score += 1
            self.feedback_label.config(text="🎉 Correct!", fg="green")
        else:
            self.feedback_label.config(
                text=f"❌ Correct answer is: {correct_answer}", fg="red"
            )

        self.score_label.config(text=f"Score: {self.score}")

        # Disable all buttons
        for btn in self.option_buttons:
            btn.config(state="disabled")

        # Auto-progress to next question after delay
        if not hasattr(self, '_auto_progress_scheduled') or not self._auto_progress_scheduled:
            self._auto_progress_scheduled = True
            self._auto_progressing = True
            
            # Automatically move to next question after a delay
            if self.current_index + 1 < self.total_questions:
                self._auto_next_id = self.root.after(1500, self.auto_next_question)  # Move to next after 1.5 seconds
            else:
                # Show results when quiz is completed
                self.root.after(1500, self.show_final_results)
        
    def auto_next_question(self):
        # Clear the auto-next ID to avoid canceling after execution
        if hasattr(self, '_auto_next_id'):
            self._auto_next_id = None
        
        # Reset auto progression flags
        self._auto_progress_scheduled = False
        self._auto_submit_in_progress = False
        self._auto_progressing = False
        
        # Move to next question automatically
        if self.current_index + 1 < self.total_questions:
            self.current_index += 1
            self.load_question()

    # Navigation functions removed
            
    def show_final_results(self):
        # Calculate percentage
        percentage = (self.score / self.total_questions) * 100
        
        # Prepare results message
        result_message = f"Quiz Completed!\n\nFinal Score: {self.score}/{self.total_questions}\nPercentage: {percentage:.1f}%\n\nGreat job!"        
        messagebox.showinfo("Quiz Results", result_message)
        self.root.destroy()

    # Previous question function removed

    def go_home(self):
        self.root.destroy()
        if self.show_frame and self.main_menu:
            self.show_frame(self.main_menu)


# ---------------- RUN ----------------
def run(root=None, main_menu=None, show_frame=None):
    if root:
        win = tk.Toplevel(root)
    else:
        win = tk.Tk()
    ImageQuizApp(win, main_menu, show_frame)
    if not root:
        win.mainloop()
