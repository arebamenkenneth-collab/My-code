import tkinter as tk
from tkinter import scrolledtext
import threading
import time

# ----------------- MAIN WINDOW -----------------
root = tk.Tk()
root.title("KennethBuilds AI Chat")
root.geometry("420x600")
root.configure(bg="#0f0f0f")
root.resizable(False, False)

# ----------------- HEADER BAR -----------------
header = tk.Frame(root, bg="#1a1a2e", height=60)
header.pack(fill=tk.X)
header.pack_propagate(False)

avatar_label = tk.Label(header, text="🤖", font=("Arial", 22), bg="#1a1a2e")
avatar_label.pack(side=tk.LEFT, padx=10, pady=5)

name_frame = tk.Frame(header, bg="#1a1a2e")
name_frame.pack(side=tk.LEFT, pady=8)

tk.Label(name_frame, text="KennethBuilds", font=("Arial", 13, "bold"),
         bg="#1a1a2e", fg="#00e5ff").pack(anchor="w")
tk.Label(name_frame, text="🟢 Online", font=("Arial", 9),
         bg="#1a1a2e", fg="#aaaaaa").pack(anchor="w")

# ----------------- CHAT DISPLAY -----------------
chat_frame = tk.Frame(root, bg="#0f0f0f")
chat_frame.pack(padx=10, pady=8, fill=tk.BOTH, expand=True)

chat_area = scrolledtext.ScrolledText(
    chat_frame,
    wrap=tk.WORD,
    bg="#0f0f0f",
    fg="white",
    font=("Arial", 11),
    state="disabled",
    bd=0,
    relief="flat",
    padx=8,
    pady=8,
    cursor="arrow"
)
chat_area.pack(fill=tk.BOTH, expand=True)

# Text color tags
chat_area.tag_config("user_name", foreground="#00e5ff", font=("Arial", 10, "bold"))
chat_area.tag_config("user_msg", foreground="#e0e0e0", font=("Arial", 11))
chat_area.tag_config("bot_name", foreground="#ff9800", font=("Arial", 10, "bold"))
chat_area.tag_config("bot_msg", foreground="#e0e0e0", font=("Arial", 11))
chat_area.tag_config("typing", foreground="#888888", font=("Arial", 10, "italic"))
chat_area.tag_config("time_tag", foreground="#555555", font=("Arial", 8))

# ----------------- DIVIDER -----------------
tk.Frame(root, bg="#2a2a2a", height=1).pack(fill=tk.X, padx=10)

# ----------------- ENTRY AREA -----------------
entry_frame = tk.Frame(root, bg="#1a1a1a", pady=10)
entry_frame.pack(fill=tk.X, padx=10, pady=6)

user_input = tk.Entry(
    entry_frame,
    font=("Arial", 12),
    bg="#2a2a2a",
    fg="white",
    insertbackground="#00e5ff",
    relief="flat",
    bd=8
)
user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 8))
user_input.insert(0, "Type a message...")
user_input.config(fg="#666666")

def on_focus_in(e):
    if user_input.get() == "Type a message...":
        user_input.delete(0, tk.END)
        user_input.config(fg="white")

def on_focus_out(e):
    if user_input.get() == "":
        user_input.insert(0, "Type a message...")
        user_input.config(fg="#666666")

user_input.bind("<FocusIn>", on_focus_in)
user_input.bind("<FocusOut>", on_focus_out)

send_btn = tk.Button(
    entry_frame,
    text="➤",
    font=("Arial", 14),
    command=lambda: send_message(),
    bg="#00e5ff",
    fg="#0f0f0f",
    relief="flat",
    padx=12,
    pady=4,
    cursor="hand2",
    activebackground="#00b8cc",
    activeforeground="#0f0f0f"
)
send_btn.pack(side=tk.RIGHT)

# ----------------- BOT LOGIC -----------------
def bot_reply(message):
    message = message.lower()

    responses = {
        ("hello", "hi", "hey", "sup", "yo"):
            "Hey hey! 👋😄 Welcome to KennethBuilds AI! How can I help you today?",
        ("how are you", "how r u", "you good", "how are u"):
            "I'm running at full power! ⚡ No bugs today... hopefully 😂",
        ("game", "pygame", "build a game"):
            "Let's build something epic! 🎮 Pygame is great for 2D games on Android too!",
        ("python", "coding", "code", "programming"):
            "Python is 🔥! You can build games, AI, apps, bots — all from your phone!",
        ("who are you", "what are you", "your name"):
            "I'm KennethBuilds AI 🤖 — built by Kenneth to help you code smarter!",
        ("kenneth", "codewithkenneth"):
            "Yes! CodeWithKenneth is the brand 💪 Teaching Python on Android, no laptop needed!",
        ("pydroid", "android", "phone coding"):
            "Coding on Android is underrated! 📱 Pydroid 3 is powerful — Kenneth proves it daily!",
        ("tiktok", "social media", "content"):
            "Follow @arebamenkenneth on TikTok for Python & Pygame content! 🎬🔥",
        ("help", "what can you do"):
            "I can chat, answer Python questions, give coding tips & hype you up! 💡🚀",
        ("bye", "goodbye", "see you", "exit"):
            "Bye bye! 👋 Keep coding and stay awesome! 💪✨",
        ("thank", "thanks", "thank you"):
            "Anytime! 🙌 That's what I'm here for! Keep building 🚀",
        ("joke", "funny", "make me laugh"):
            "Why do programmers prefer dark mode? 🌑 Because light attracts bugs! 😂🐛",
        ("error", "bug", "not working"):
            "Bugs are just hidden features 😅 Check your indentation first — Python is strict! 🐍",
        ("loops", "for loop", "while loop"):
            "Loops are your best friend! 🔄 `for i in range(10): print(i)` — simple and powerful!",
        ("function", "def", "methods"):
            "Functions keep your code clean! ✨ Use `def` to define one — reuse it anywhere!",
        ("variable", "variables"):
            "Variables store data! 📦 Like: `name = 'Kenneth'` — easy and useful!",
        ("motivation", "inspire me", "motivate me"):
            "You started coding on a PHONE. That alone makes you a legend. Keep going! 🏆🔥",
        ("money", "earn", "freelance", "fiverr"):
            "Python skills = income! 💰 Try Fiverr, Freelancer, or sell your own Python course!",
    }

    for keywords, reply in responses.items():
        if any(k in message for k in keywords):
            return reply

    return "Hmm, I'm still learning 🤔 Try asking about Python, Pygame, or coding tips!"

# ----------------- TYPING EFFECT -----------------
def show_typing_then_reply(response):
    chat_area.config(state="normal")
    chat_area.insert(tk.END, "KennethBuilds is typing...\n", "typing")
    chat_area.config(state="disabled")
    chat_area.yview(tk.END)

    time.sleep(1.2)

    chat_area.config(state="normal")

    # Remove typing line
    content = chat_area.get("1.0", tk.END)
    lines = content.split("\n")
    lines = [l for l in lines if l.strip() != "KennethBuilds is typing..."]
    chat_area.delete("1.0", tk.END)
    for line in lines:
        chat_area.insert(tk.END, line + "\n")

    # Bot reply
    chat_area.insert(tk.END, "KennethBuilds  ", "bot_name")
    chat_area.insert(tk.END, get_time() + "\n", "time_tag")
    chat_area.insert(tk.END, response + "\n\n", "bot_msg")

    chat_area.config(state="disabled")
    chat_area.yview(tk.END)

def get_time():
    return time.strftime("%I:%M %p")

# ----------------- SEND MESSAGE -----------------
def send_message(event=None):
    msg = user_input.get().strip()
    if msg == "" or msg == "Type a message...":
        return

    chat_area.config(state="normal")
    chat_area.insert(tk.END, "You  ", "user_name")
    chat_area.insert(tk.END, get_time() + "\n", "time_tag")
    chat_area.insert(tk.END, msg + "\n\n", "user_msg")
    chat_area.config(state="disabled")
    chat_area.yview(tk.END)

    user_input.delete(0, tk.END)

    response = bot_reply(msg)
    threading.Thread(target=show_typing_then_reply, args=(response,), daemon=True).start()

# ----------------- WELCOME MESSAGE -----------------
def show_welcome():
    chat_area.config(state="normal")
    chat_area.insert(tk.END, "KennethBuilds  ", "bot_name")
    chat_area.insert(tk.END, get_time() + "\n", "time_tag")
    chat_area.insert(tk.END, "Hey! 👋 I'm KennethBuilds AI. Ask me anything about Python, Pygame, or coding!\n\n", "bot_msg")
    chat_area.config(state="disabled")

show_welcome()

# Enter key support
root.bind("<Return>", send_message)

# ----------------- RUN APP -----------------
root.mainloop()