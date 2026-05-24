import tkinter as tk
from tkinter import scrolledtext

# ----------------- MAIN WINDOW -----------------
root = tk.Tk()
root.title("Advanced Chat Box")
root.geometry("420x500")
root.configure(bg="#1e1e1e")

# ----------------- CHAT DISPLAY -----------------
chat_area = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    bg="#2b2b2b",
    fg="white",
    font=("Arial", 11),
    state="disabled"
)
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# ----------------- ENTRY FIELD -----------------
entry_frame = tk.Frame(root, bg="#1e1e1e")
entry_frame.pack(fill=tk.X, padx=10, pady=5)

user_input = tk.Entry(
    entry_frame,
    font=("Arial", 12),
    bg="#3a3a3a",
    fg="white",
    insertbackground="white"
)
user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

# ----------------- BOT LOGIC -----------------
def bot_reply(message):
    message = message.lower()

    if "hello" in message:
        return "Hi there! 👋"
    elif "how are you" in message:
        return "I'm just code, but I'm doing great!"
    elif "game" in message:
        return "I can help you build a game in Pygame 🎮"
    elif "python" in message:
        return "Python is powerful for apps, AI, and games!"
    else:
        return "I don't understand that yet."

# ----------------- SEND MESSAGE -----------------
def send_message(event=None):
    msg = user_input.get().strip()
    if msg == "":
        return

    chat_area.config(state="normal")
    chat_area.insert(tk.END, "You: " + msg + "\n")

    response = bot_reply(msg)
    chat_area.insert(tk.END, "Bot: " + response + "\n\n")

    chat_area.config(state="disabled")
    chat_area.yview(tk.END)

    user_input.delete(0, tk.END)

# ----------------- SEND BUTTON -----------------
send_btn = tk.Button(
    entry_frame,
    text="Send",
    command=send_message,
    bg="#4CAF50",
    fg="white"
)
send_btn.pack(side=tk.RIGHT)

# Enter key support
root.bind("<Return>", send_message)

# ----------------- RUN APP -----------------
root.mainloop()