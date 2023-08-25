import tkinter as tk
import random
import time
import pycountry
import requests
from io import BytesIO
from PIL import Image, ImageTk

def get_flag_url(country_name):
    try:
        country = pycountry.countries.get(name=country_name)
        return f"https://flagpedia.net/data/flags/normal/{country.alpha_2.lower()}.png"
    except:
        return None

FLAGS = {
    "United States": get_flag_url("United States"),
    "United Kingdom": get_flag_url("United Kingdom"),
    "Canada": get_flag_url("Canada"),
    "Japan": get_flag_url("Japan"),
    "Australia": get_flag_url("Australia"),
    "Germany": get_flag_url("Germany"),
    "France": get_flag_url("France"),
    "Italy": get_flag_url("Italy"),
    "Brazil": get_flag_url("Brazil"),
    "India": get_flag_url("India"),
    # Add more flags here...
}

class GuessTheFlagGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Guess the Flag")

        self.flag_countries = list(FLAGS.keys())
        self.current_country = None
        self.guess = ""

        self.score = 0
        self.total_time = 0
        self.start_time = None

        self.flag_images = {country: self.get_image(FLAGS[country]) for country in self.flag_countries}

        self.create_widgets()
        self.new_question()
        self.update_clock()

    def create_widgets(self):
        self.flag_label = tk.Label(self.root, image=None)
        self.flag_label.pack(pady=20)

        self.input_entry = tk.Entry(self.root, font=("Arial", 20))
        self.input_entry.pack(pady=10)
        self.input_entry.bind("<Return>", self.on_enter)

        self.feedback_label = tk.Label(self.root, text="", font=("Arial", 20))
        self.feedback_label.pack(pady=10)

        self.score_label = tk.Label(self.root, text="Score: 0", font=("Arial", 20))
        self.score_label.pack(pady=10)

        self.timer_label = tk.Label(self.root, text="Time: 00:00:00", font=("Arial", 20))
        self.timer_label.pack(pady=10)

    def new_question(self):
        if not self.flag_countries:
            self.flag_label.config(image=None, text="Game Over!")
            self.input_entry.config(state=tk.DISABLED)
            return

        self.current_country = random.choice(self.flag_countries)
        self.flag_label.config(image=self.flag_images[self.current_country], text="")
        self.guess = ""
        self.feedback_label.config(text="")
        self.start_time = time.time()

    def on_enter(self, event):
        guess = self.input_entry.get().strip().lower()
        self.input_entry.delete(0, tk.END)
        if guess == self.current_country.lower():
            self.feedback_label.config(text="Correct!", fg="green")
            self.flag_countries.remove(self.current_country)
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            elapsed_time = round(time.time() - self.start_time, 2)
            self.total_time += elapsed_time
            self.timer_label.config(text=f"Time: {self.format_time(self.total_time)}")
            self.new_question()
        else:
            self.feedback_label.config(text="Incorrect, try again.", fg="red")

    def format_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def update_clock(self):
        if not self.flag_countries:
            return
        elapsed_time = round(time.time() - self.start_time, 2)
        self.timer_label.config(text=f"Time: {self.format_time(self.total_time + elapsed_time)}")
        self.root.after(1000, self.update_clock)

    def get_image(self, url):
        try:
            response = requests.get(url)
            image_data = BytesIO(response.content)
            return ImageTk.PhotoImage(Image.open(image_data))
        except:
            return None

if __name__ == "__main__":
    root = tk.Tk()
    game = GuessTheFlagGame(root)
    root.mainloop()
