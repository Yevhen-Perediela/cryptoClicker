import customtkinter as ctk
import tkinter as tk
import math

root = ctk.CTk()
root.title("Crypto Clicker TEB")
root.geometry("600x600")
root.resizable(False, False)
bg_canvas = tk.Canvas(root, width=600, height=600, bg="#005b96", highlightthickness=0)
bg_canvas.place(x=0, y=0)

value = 0
mouse_x, mouse_y = 300, 300
coin_scale = 1.0
target_scale = 1.0

def on_mouse_move(event):
    global mouse_x, mouse_y
    mouse_x, mouse_y = event.x, event.y

def on_press(event):
    global target_scale, value
    dist = math.sqrt((event.x - 300)**2 + (event.y - 310)**2)
    if dist < 95 * coin_scale:
        target_scale = 0.88
        value += 1

def on_release(event):
    global target_scale
    target_scale = 1.0

bg_canvas.bind("<Motion>", on_mouse_move)
bg_canvas.bind("<ButtonPress-1>", on_press)
bg_canvas.bind("<ButtonRelease-1>", on_release)

def update_loop():
    global coin_scale
    coin_scale += (target_scale - coin_scale) * 0.22
    
    dx = (mouse_x - 300) / 10.0
    dy = (mouse_y - 300) / 10.0
    
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
    
    s_rad = 95 * coin_scale
    bg_canvas.create_oval(300 - s_rad, 310 - s_rad, 300 + s_rad, 310 + s_rad, fill="#7d848c", outline="#2c3035", width=2)
    bg_canvas.create_oval(300 - s_rad*0.88, 310 - s_rad*0.88, 300 + s_rad*0.88, 310 + s_rad*0.88, fill="#b25d1f", outline="#402008", width=2)
    bg_canvas.create_oval(300 - s_rad*0.32, 310 - s_rad*0.32, 300 + s_rad*0.32, 310 + s_rad*0.32, fill="#9ea5ad", outline="#202224", width=2)
    bg_canvas.create_text(300, 310, text="T", font=("Georgia", max(8, int(20 * coin_scale)), "bold"), fill="#202224")
    
    root.after(20, update_loop)

update_loop()
root.mainloop()