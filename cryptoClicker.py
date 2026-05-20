import customtkinter as ctk
import tkinter as tk

ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.title("Crypto Clicker TEB")
root.geometry("600x700")
root.resizable(False, False)
root.configure(fg_color="#1e1e1e")


header = ctk.CTkLabel(root, text="Crypto Clicker", font=("Arial", 28, "bold"), text_color="white", fg_color="transparent")
header.pack(pady=(20, 10))

coinsLabel = ctk.CTkLabel(root, text="TebCoin balance: 0", corner_radius=15, font=("Arial", 16, "bold"), text_color="#1e1e1e", fg_color="#ffffff", width=240, height=45)
coinsLabel.pack(pady=10)

value = 0
animating = False
coins_per_click = 1
auto_coins = 0
bonus = 1

click_upgrade_price = 10
auto_upgrade_price = 25
bonus_upgrade_price = 50

infoLabel = ctk.CTkLabel(root, text="Per click: 1 | Auto: 0 | Bonus: x1", font=("Arial", 14), text_color="white")
infoLabel.pack(pady=(0, 5))

messageLabel = ctk.CTkLabel(root, text="", font=("Arial", 13), text_color="#f9fe00")
messageLabel.pack(pady=(0, 5))

def update_labels():
    coinsLabel.configure(text=f"TebCoin balance: {value}")
    infoLabel.configure(text=f"Per click: {coins_per_click * bonus} | Auto: {auto_coins * bonus} | Bonus: x{bonus}")
    clickButton.configure(text=f"+1 per click\nPrice: {click_upgrade_price}")
    autoButton.configure(text=f"+1 auto\nPrice: {auto_upgrade_price}")
    bonusButton.configure(text=f"Bonus x2\nPrice: {bonus_upgrade_price}")

def add_coin():
    global value
    value += coins_per_click * bonus
    update_labels()

def buy_click_upgrade():
    global value, coins_per_click, click_upgrade_price
    if value >= click_upgrade_price:
        value -= click_upgrade_price
        coins_per_click += 1
        click_upgrade_price += 15
        messageLabel.configure(text="Click upgrade bought!")
    else:
        messageLabel.configure(text="Not enough TebCoin")
    update_labels()

def buy_auto_upgrade():
    global value, auto_coins, auto_upgrade_price
    if value >= auto_upgrade_price:
        value -= auto_upgrade_price
        auto_coins += 1
        auto_upgrade_price += 30
        messageLabel.configure(text="Auto income bought!")
    else:
        messageLabel.configure(text="Not enough TebCoin")
    update_labels()

def buy_bonus_upgrade():
    global value, bonus, bonus_upgrade_price
    if value >= bonus_upgrade_price:
        value -= bonus_upgrade_price
        bonus *= 2
        bonus_upgrade_price *= 2
        messageLabel.configure(text="Bonus bought!")
    else:
        messageLabel.configure(text="Not enough TebCoin")
    update_labels()

def add_auto_coins():
    global value
    if auto_coins > 0:
        value += auto_coins * bonus
        update_labels()
    root.after(1000, add_auto_coins)

def animate_grow(step=0):
    global animating
    animating = True
    if step < 10:
        x1 = 10 - step
        y1 = 10 - step
        x2 = 250 + step
        y2 = 250 + step
        coin_canvas.coords(coin_circle, x1, y1, x2, y2)
        root.after(20, lambda: animate_grow(step + 1))
    else:
        animating = False

def animate_shrink(step=0):
    global animating
    animating = True
    if step < 10:
        x1 = 10 - (10 - step)
        y1 = 10 - (10 - step)
        x2 = 250 + (10 - step)
        y2 = 250 + (10 - step)
        coin_canvas.coords(coin_circle, x1, y1, x2, y2)
        root.after(20, lambda: animate_shrink(step + 1))
    else:
        coin_canvas.coords(coin_circle, 10, 10, 250, 250)
        animating = False

coin_canvas = tk.Canvas(
    root,
    width=270,
    height=270,
    bg="#1e1e1e",
    highlightthickness=0
)
coin_canvas.pack(pady=25)

coin_circle = coin_canvas.create_oval(
    10, 10, 250, 250,
    fill="#f9fe00",
    outline=""
)

coin_text = coin_canvas.create_text(
    130, 130,
    text="TEBCOIN",
    fill="black",
    font=("Arial", 25, "bold")
)

coin_canvas.tag_bind(coin_circle, "<Button-1>", lambda event: add_coin())
coin_canvas.tag_bind(coin_text, "<Button-1>", lambda event: add_coin())
coin_canvas.tag_bind(coin_circle, "<ButtonPress-1>", lambda event: animate_grow())
coin_canvas.tag_bind(coin_text, "<ButtonPress-1>", lambda event: animate_grow())
coin_canvas.tag_bind(coin_circle, "<ButtonRelease-1>", lambda event: animate_shrink())
coin_canvas.tag_bind(coin_text, "<ButtonRelease-1>", lambda event: animate_shrink())

upgradesFrame = ctk.CTkFrame(root, fg_color="transparent")
upgradesFrame.pack(side="bottom", pady=25)

clickButton = ctk.CTkButton(upgradesFrame, text="", width=160, height=55, command=buy_click_upgrade)
clickButton.grid(row=0, column=0, padx=8)

autoButton = ctk.CTkButton(upgradesFrame, text="", width=160, height=55, command=buy_auto_upgrade)
autoButton.grid(row=0, column=1, padx=8)

bonusButton = ctk.CTkButton(upgradesFrame, text="", width=160, height=55, command=buy_bonus_upgrade)
bonusButton.grid(row=0, column=2, padx=8)

update_labels()
add_auto_coins()

root.mainloop()
