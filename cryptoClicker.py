import customtkinter as ctk

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

root.mainloop()