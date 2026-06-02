import customtkinter as ctk
import tkinter as tk
import math
import os
import random
import shutil
import subprocess
import time

root = ctk.CTk()
root.title("Crypto Clicker TEB")
root.geometry("600x700")
root.resizable(False, False)
root.configure(fg_color="#366b2f")
bg_canvas = tk.Canvas(root, width=600, height=600, bg="#005b96", highlightthickness=0)
bg_canvas.place(x=0, y=0)

value = 0
coins_per_click = 1
auto_coins = 0
bonus = 1

click_upgrade_price = 10
auto_upgrade_price = 25
bonus_upgrade_price = 50

message_text = ""
message_timer = 0

stats = {
    "started_at": time.time(),
    "total_clicks": 0,
    "total_earned": 0,
    "upgrades_bought": 0,
    "bonuses_caught": 0,
    "bonuses_missed": 0
}


class SoundManager:
    def __init__(self, tk_root):
        self.root = tk_root
        self.sound_enabled = True
        self.music_on = False
        self.music_process = None
        self.game_folder = os.path.dirname(os.path.abspath(__file__))
        self.music_file = self.find_music_file()

    def find_music_file(self):
        for file_name in os.listdir(self.game_folder):
            if file_name.lower().endswith(".mp3"):
                return os.path.join(self.game_folder, file_name)
        return None

    def play(self, sound_name):
        if self.sound_enabled:
            self.root.bell()

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        update_labels()

    def toggle_music(self):
        if self.music_on:
            self.stop_music()
        else:
            self.start_music()
        update_labels()

    def start_music(self):
        if not self.music_file:
            set_message("No mp3 file found")
            return

        if shutil.which("ffplay"):
            command = ["ffplay", "-nodisp", "-loglevel", "error", self.music_file]
        elif shutil.which("mpv"):
            command = ["mpv", "--no-video", "--loop=inf", self.music_file]
        elif shutil.which("cvlc"):
            command = ["cvlc", "--quiet", "--loop", self.music_file]
        elif shutil.which("vlc"):
            command = ["vlc", "--quiet", "--loop", self.music_file]
        else:
            set_message("Install ffmpeg/mpv/vlc for music")
            return

        self.music_on = True
        self.music_process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        self.root.after(1000, self.check_music)

    def check_music(self):
        if not self.music_process:
            return

        if self.music_process.poll() is None:
            self.root.after(1000, self.check_music)
            return

        exit_code = self.music_process.returncode
        self.music_process = None
        if self.music_on and exit_code == 0:
            self.start_music()
        else:
            self.music_on = False
            set_message("Music player error")
            update_labels()

    def stop_music(self):
        if self.music_process:
            self.music_process.terminate()
            self.music_process = None
        self.music_on = False


sound_manager = SoundManager(root)

falling_bonus = {
    "x": 0,
    "y": -50,
    "speed": 3,
    "radius": 20,
    "active": False,
    "multiplier": 1.0
}

time_bonus = {
    "active": False,
    "multiplier": 1.0,
    "timer": 0 
}

def set_message(text):
    global message_text, message_timer
    message_text = text
    message_timer = 100

def update_labels():
    clickButton.configure(text=f"+1 per click\nPrice: {click_upgrade_price}")
    autoButton.configure(text=f"+1 auto\nPrice: {auto_upgrade_price}")
    bonusButton.configure(text=f"Bonus x2\nPrice: {bonus_upgrade_price}")
    soundButton.configure(text=f"Sound: {'ON' if sound_manager.sound_enabled else 'OFF'}")
    musicButton.configure(text=f"Music: {'ON' if sound_manager.music_on else 'OFF'}")

mouse_x, mouse_y = 300, 300
coin_scale = 1.0
target_scale = 1.0

def on_mouse_move(event):
    global mouse_x, mouse_y
    mouse_x, mouse_y = event.x, event.y

def add_coin():
    global value
    # Uwzględniamy dodatkowy bonus czasowy (jeśli jest aktywny)
    current_time_bonus = time_bonus["multiplier"] if time_bonus["active"] else 1.0
    earned = math.floor(coins_per_click * bonus * current_time_bonus)
    value += earned
    stats["total_earned"] += earned

def buy_click_upgrade():
    global value, coins_per_click, click_upgrade_price
    if value >= click_upgrade_price:
        value -= click_upgrade_price
        coins_per_click += 1
        click_upgrade_price += 15
        stats["upgrades_bought"] += 1
        sound_manager.play("buy")
        set_message("Click upgrade bought!")
    else:
        sound_manager.play("error")
        set_message("Not enough TebCoin")
    update_labels()

def buy_auto_upgrade():
    global value, auto_coins, auto_upgrade_price
    if value >= auto_upgrade_price:
        value -= auto_upgrade_price
        auto_coins += 1
        auto_upgrade_price += 30
        stats["upgrades_bought"] += 1
        sound_manager.play("buy")
        set_message("Auto income bought!")
    else:
        sound_manager.play("error")
        set_message("Not enough TebCoin")
    update_labels()

def buy_bonus_upgrade():
    global value, bonus, bonus_upgrade_price
    if value >= bonus_upgrade_price:
        value -= bonus_upgrade_price
        bonus *= 2
        bonus_upgrade_price *= 2
        stats["upgrades_bought"] += 1
        sound_manager.play("buy")
        set_message("Bonus bought!")
    else:
        sound_manager.play("error")
        set_message("Not enough TebCoin")
    update_labels()

def add_auto_coins():
    global value
    if auto_coins > 0:
        current_time_bonus = time_bonus["multiplier"] if time_bonus["active"] else 1.0
        earned = math.floor(auto_coins * bonus * current_time_bonus)
        value += earned
        stats["total_earned"] += earned
    root.after(1000, add_auto_coins)

def on_press(event):
    global target_scale, value
    
    if falling_bonus["active"]:
        dist_to_bonus = math.sqrt((event.x - falling_bonus["x"])**2 + (event.y - falling_bonus["y"])**2)
        if dist_to_bonus < falling_bonus["radius"] + 10:
            falling_bonus["active"] = False
            falling_bonus["y"] = -50
            stats["bonuses_caught"] += 1
            sound_manager.play("bonus")
            
            random_gain = random.randint(30, 50)
            time_bonus["active"] = True
            time_bonus["multiplier"] = 1.0 + (random_gain / 100.0)
            time_bonus["timer"] = 500  # 500 klatek * 20ms = 10 sekund
            set_message(f"SUPER BONUS! +{random_gain}% na 10s!")
            return

    dist = math.sqrt((event.x - 300)**2 + (event.y - 310)**2)
    if dist < 95 * coin_scale:
        target_scale = 0.88
        stats["total_clicks"] += 1
        sound_manager.play("click")
        add_coin()

def on_release(event):
    global target_scale
    target_scale = 1.0

def close_game():
    sound_manager.stop_music()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", close_game)

bg_canvas.bind("<Motion>", on_mouse_move)
bg_canvas.bind("<ButtonPress-1>", on_press)
bg_canvas.bind("<ButtonRelease-1>", on_release)

upgradesFrame = ctk.CTkFrame(root, fg_color="#366b2f", corner_radius=0)
upgradesFrame.pack(side="bottom", fill="x", pady=(0, 14), padx=0)

clickButton = ctk.CTkButton(upgradesFrame, text="", width=160, height=55, command=buy_click_upgrade)
clickButton.grid(row=0, column=0, padx=8)

autoButton = ctk.CTkButton(upgradesFrame, text="", width=160, height=55, command=buy_auto_upgrade)
autoButton.grid(row=0, column=1, padx=8)

bonusButton = ctk.CTkButton(upgradesFrame, text="", width=160, height=55, command=buy_bonus_upgrade)
bonusButton.grid(row=0, column=2, padx=8)

soundButton = ctk.CTkButton(upgradesFrame, text="", width=160, height=35, command=sound_manager.toggle_sound)
soundButton.grid(row=1, column=0, padx=8, pady=(10, 0))

musicButton = ctk.CTkButton(upgradesFrame, text="", width=160, height=35, command=sound_manager.toggle_music)
musicButton.grid(row=1, column=1, padx=8, pady=(10, 0))

for button in (clickButton, autoButton, bonusButton, soundButton, musicButton):
    button.configure(
        fg_color="#8b5a2b",
        hover_color="#a66a33",
        border_width=0,
        corner_radius=6,
        text_color="#ffffff"
    )

update_labels()
sound_manager.start_music()
update_labels()
add_auto_coins()

def draw_stat_panel(x, y, width, height, title, rows, accent_color):
    bg_canvas.create_rectangle(x + 3, y + 3, x + width + 3, y + height + 3, fill="#24411f", outline="")
    bg_canvas.create_rectangle(x, y, x + width, y + height, fill="#4b2d18", outline=accent_color, width=2)
    bg_canvas.create_text(x + width / 2, y + 22, text=title, font=("Georgia", 13, "bold"), fill="#ffffff")
    bg_canvas.create_line(x + 15, y + 40, x + width - 15, y + 40, fill=accent_color, width=1)

    for idx, (label, amount) in enumerate(rows):
        row_y = y + 55 + idx * 22
        bg_canvas.create_text(x + 20, row_y, anchor="w", text=label, font=("Georgia", 10, "bold"), fill="#f5dfb1")
        bg_canvas.create_text(x + width - 20, row_y, anchor="e", text=str(amount), font=("Georgia", 10, "bold"), fill="#ffffff")

def update_loop():
    global coin_scale, message_timer, message_text, value
    coin_scale += (target_scale - coin_scale) * 0.22
    
    dx = (mouse_x - 300) / 10.0
    dy = (mouse_y - 300) / 10.0
    
    if message_timer > 0:
        message_timer -= 1
        if message_timer == 0:
            message_text = ""
            
    bg_canvas.delete("all")
    
    sky_colors = ["#005b96", "#006aa6", "#007ab7", "#008bc9", "#009bdb", "#00aded", "#1cb7ff", "#3ec1ff", "#60cbff", "#82d5ff"]
    for idx, color in enumerate(sky_colors):
        bg_canvas.create_rectangle(0, idx * 50, 600, (idx + 1) * 50, fill=color, outline="")
        
    sun_x, sun_y = 440 - dx * 0.5, 280 - dy * 0.5
    bg_canvas.create_oval(sun_x - 35, sun_y - 35, sun_x + 35, sun_y + 35, fill="#ffd56b", outline="#ffa500", width=2)
    
    m_pts = [(-100, 800), (-100, 360), (100, 300), (250, 400), (400, 270), (700, 380), (700, 800)]
    shifted_m = [(x - dx * 1.5, y - dy * 1.5) for x, y in m_pts]
    bg_canvas.create_polygon(shifted_m, fill="#325d79", outline="")
    
    h_pts = [(-150, 800), (-150, 440), (200, 390), (450, 450), (750, 400), (750, 800)]
    shifted_h = [(x - dx * 3.0, y - dy * 3.0) for x, y in h_pts]
    bg_canvas.create_polygon(shifted_h, fill="#489a51", outline="")
    
    f_pts = [(-200, 900), (-200, 520), (300, 480), (800, 540), (800, 900)]
    shifted_f = [(x - dx * 5.0, y - dy * 5.0) for x, y in f_pts]
    bg_canvas.create_polygon(shifted_f, fill="#55a630", outline="")
    
    bg_canvas.create_text(302, 52, text="Crypto Clicker", font=("Georgia", 28, "bold"), fill="#1a2d3c")
    bg_canvas.create_text(300, 50, text="Crypto Clicker", font=("Georgia", 28, "bold"), fill="#ffffff")
    
    bg_canvas.create_rectangle(180, 90, 420, 135, fill="#3d2616", outline="#ffd700", width=2)
    bg_canvas.create_text(300, 112, text=f"TebCoin balance: {value}", font=("Georgia", 14, "bold"), fill="#ffffff")
    
    curr_mult = bonus * (time_bonus["multiplier"] if time_bonus["active"] else 1.0)
    bg_canvas.create_text(300, 150, text=f"Per click: {math.floor(coins_per_click * curr_mult)} | Auto: {math.floor(auto_coins * curr_mult)} | Bonus: x{curr_mult:.1f}", font=("Georgia", 11, "bold"), fill="#ffffff")

    play_time = int(time.time() - stats["started_at"])
    minutes = play_time // 60
    seconds = play_time % 60
    cps = math.floor(auto_coins * curr_mult)
    draw_stat_panel(
        25,
        430,
        230,
        145,
        "Statystyki",
        [
            ("Kliknięcia", stats["total_clicks"]),
            ("Zebrane monety", stats["total_earned"]),
            ("Monety / sek.", cps),
            ("Czas gry", f"{minutes:02d}:{seconds:02d}")
        ],
        "#77d9ff"
    )
    draw_stat_panel(
        345,
        430,
        230,
        125,
        "Bonusy",
        [
            ("Ulepszenia", stats["upgrades_bought"]),
            ("Złapane bonusy", stats["bonuses_caught"]),
            ("Pominięte bonusy", stats["bonuses_missed"])
        ],
        "#ffd56b"
    )
    
    if message_text:
        bg_canvas.create_text(300, 175, text=message_text, font=("Georgia", 12, "bold"), fill="#f9fe00")

    if time_bonus["active"]:
        time_bonus["timer"] -= 1
        seconds_left = math.ceil(time_bonus["timer"] / 50)
        bg_canvas.create_text(300, 200, text=f"Złoty bonus aktywny jeszcze: {seconds_left}s", font=("Georgia", 12, "italic"), fill="#00ffcc")
        if time_bonus["timer"] <= 0:
            time_bonus["active"] = False
            set_message("Bonus czasowy się skończył")

    if not falling_bonus["active"] and random.randint(1, 300) == 1:
        falling_bonus["active"] = True
        falling_bonus["x"] = random.randint(50, 550)
        falling_bonus["y"] = -30
        falling_bonus["speed"] = random.randint(3, 6)

    if falling_bonus["active"]:
        falling_bonus["y"] += falling_bonus["speed"]
        
        bx, by, br = falling_bonus["x"], falling_bonus["y"], falling_bonus["radius"]
        bg_canvas.create_oval(bx - br, by - br, bx + br, by + br, fill="#ffd700", outline="#fff", width=2)
        bg_canvas.create_text(bx, by, text="⭐", font=("Georgia", 14, "bold"), fill="#3d2616")
        
        if falling_bonus["y"] > 600:
            falling_bonus["active"] = False
            stats["bonuses_missed"] += 1
            sound_manager.play("miss")
            penalty = math.floor(value * 0.75)
            value -= penalty
            set_message(f"Za późno! Straciłeś 75% monet (-{penalty})")

    s_rad = 95 * coin_scale
    bg_canvas.create_oval(300 - s_rad, 310 - s_rad, 300 + s_rad, 310 + s_rad, fill="#7d848c", outline="#2c3035", width=2)
    bg_canvas.create_oval(300 - s_rad*0.88, 310 - s_rad*0.88, 300 + s_rad*0.88, 310 + s_rad*0.88, fill="#b25d1f", outline="#402008", width=2)
    bg_canvas.create_oval(300 - s_rad*0.32, 310 - s_rad*0.32, 300 + s_rad*0.32, 310 + s_rad*0.32, fill="#9ea5ad", outline="#202224", width=2)
    bg_canvas.create_text(300, 310, text="T", font=("Georgia", max(8, int(20 * coin_scale)), "bold"), fill="#202224")
    
    root.after(20, update_loop)

update_loop()
root.mainloop()
