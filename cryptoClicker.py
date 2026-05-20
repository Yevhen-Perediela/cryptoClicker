import customtkinter as ctk
import tkinter as tk

ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.title("Crypto Clicker TEB")
root.geometry("600x600")
root.resizable(False, False)
root.configure(fg_color="#1e1e1e")


header = ctk.CTkLabel(root, text="Crypto Clicker", font=("Arial", 28, "bold"), text_color="white", fg_color="transparent")
header.pack(pady=(20, 10))

coinsLabel = ctk.CTkLabel(root, text="TebCoin balance: 0", corner_radius=15, font=("Arial", 16, "bold"), text_color="#1e1e1e", fg_color="#ffffff", width=240, height=45)
coinsLabel.pack(pady=10)

value = 0
animating = False

def add_coin():
    global value
    value += 1
    coinsLabel.configure(text=f"TebCoin balance: {value}")

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


root.mainloop()