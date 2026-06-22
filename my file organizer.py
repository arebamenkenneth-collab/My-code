import os
import shutil
import json
import datetime

# ── CONFIG ──────────────────────────────────────────────
# Change this to the folder you want to organize
TARGET_FOLDER = "/sdcard/"

LOG_FILE = "/sdcard/organizer_log.json"

FILE_CATEGORIES = {
    "Images":     [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".heic", ".svg"],
    "Videos":     [".mp4", ".mkv", ".avi", ".mov", ".3gp", ".flv", ".wmv"],
    "Audio":      [".mp3", ".wav", ".aac", ".ogg", ".flac", ".m4a"],
    "Documents":  [".pdf", ".doc", ".docx", ".txt", ".pptx", ".xlsx", ".csv", ".odt"],
    "Code":       [".py", ".js", ".html", ".css", ".json", ".xml", ".java", ".cpp", ".c"],
    "Archives":   [".zip", ".rar", ".tar", ".gz", ".7z"],
    "APKs":       [".apk"],
    "Others":     []
}
# ────────────────────────────────────────────────────────


def get_category(filename):
    ext = os.path.splitext(filename)[1].lower()
    for category, exts in FILE_CATEGORIES.items():
        if ext in exts:
            return category
    return "Others"


def get_date_folder(filepath):
    timestamp = os.path.getmtime(filepath)
    date = datetime.datetime.fromtimestamp(timestamp)
    return date.strftime("%Y-%m")   # e.g. 2025-06


def load_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return {"sessions": []}


def save_log(log):
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)


def print_banner():
    print("=" * 48)
    print("   📁  FILE ORGANIZER — CodeWithKenneth")
    print("=" * 48)
    print()


def print_menu():
    print("What do you want to do?\n")
    print("  [1] 🔍 Scan & Preview (no changes made)")
    print("  [2] ✅ Organize by FILE TYPE")
    print("  [3] 📅 Organize by DATE (month/year)")
    print("  [4] 🔄 Organize by TYPE + DATE")
    print("  [5] ↩️  Undo Last Session")
    print("  [6] 📊 View Logs")
    print("  [7] ⚙️  Change Target Folder")
    print("  [0] 🚪 Exit")
    print()


def scan_folder(folder):
    files = []
    for item in os.listdir(folder):
        full = os.path.join(folder, item)
        if os.path.isfile(full):
            files.append(full)
    return files


def preview(folder):
    files = scan_folder(folder)
    if not files:
        print("⚠️  No files found in:", folder)
        return

    counts = {}
    total_size = 0
    for f in files:
        cat = get_category(os.path.basename(f))
        counts[cat] = counts.get(cat, 0) + 1
        total_size += os.path.getsize(f)

    print(f"\n📂 Folder: {folder}")
    print(f"📄 Total files: {len(files)}")
    print(f"💾 Total size:  {total_size / (1024*1024):.2f} MB\n")
    print(f"{'Category':<15} {'Files':>6}")
    print("-" * 24)
    for cat, count in sorted(counts.items()):
        print(f"  {cat:<13} {count:>6}")
    print()


def organize(folder, mode="type"):
    files = scan_folder(folder)
    if not files:
        print("⚠️  No files found.")
        return

    moved = []
    skipped = []
    errors = []

    print(f"\n🚀 Organizing {len(files)} files...\n")

    for filepath in files:
        filename = os.path.basename(filepath)
        cat = get_category(filename)

        if mode == "type":
            dest_dir = os.path.join(folder, cat)
        elif mode == "date":
            month = get_date_folder(filepath)
            dest_dir = os.path.join(folder, month)
        else:  # type + date
            month = get_date_folder(filepath)
            dest_dir = os.path.join(folder, cat, month)

        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, filename)

        # Handle duplicate filenames
        if os.path.exists(dest_path):
            name, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(dest_path):
                dest_path = os.path.join(dest_dir, f"{name}_{counter}{ext}")
                counter += 1

        try:
            shutil.move(filepath, dest_path)
            moved.append({"from": filepath, "to": dest_path})
            print(f"  ✅ {filename[:35]:<35} → {cat}")
        except Exception as e:
            errors.append({"file": filepath, "error": str(e)})
            print(f"  ❌ {filename} — {e}")

    # Save session to log
    log = load_log()
    session = {
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "folder": folder,
        "mode": mode,
        "moved": moved,
        "errors": errors
    }
    log["sessions"].append(session)
    save_log(log)

    print(f"\n{'='*40}")
    print(f"  ✅ Moved:   {len(moved)} files")
    print(f"  ⏭️  Skipped: {len(skipped)} files")
    print(f"  ❌ Errors:  {len(errors)} files")
    print(f"  📝 Log saved → {LOG_FILE}")
    print(f"{'='*40}\n")


def undo_last(folder):
    log = load_log()
    if not log["sessions"]:
        print("⚠️  No sessions to undo.")
        return

    last = log["sessions"][-1]
    moved = last["moved"]

    if not moved:
        print("⚠️  Last session had no moves to undo.")
        return

    print(f"\n↩️  Undoing session from {last['date']}...\n")
    success = 0
    fail = 0

    for entry in reversed(moved):
        src = entry["to"]
        dst = entry["from"]
        try:
            if os.path.exists(src):
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.move(src, dst)
                print(f"  ↩️  Restored: {os.path.basename(dst)}")
                success += 1
            else:
                print(f"  ⚠️  Not found: {src}")
                fail += 1
        except Exception as e:
            print(f"  ❌ Error: {e}")
            fail += 1

    # Remove the undone session
    log["sessions"].pop()
    save_log(log)

    # Clean up empty folders
    for entry in last["moved"]:
        folder_path = os.path.dirname(entry["to"])
        try:
            if os.path.isdir(folder_path) and not os.listdir(folder_path):
                os.rmdir(folder_path)
        except:
            pass

    print(f"\n✅ Restored: {success}  |  ❌ Failed: {fail}\n")


def view_logs():
    log = load_log()
    sessions = log["sessions"]
    if not sessions:
        print("\n📭 No sessions logged yet.\n")
        return

    print(f"\n📊 Total sessions: {len(sessions)}\n")
    for i, s in enumerate(sessions, 1):
        print(f"  Session {i}:")
        print(f"    📅 Date:   {s['date']}")
        print(f"    📂 Folder: {s['folder']}")
        print(f"    ⚙️  Mode:   {s['mode']}")
        print(f"    ✅ Moved:  {len(s['moved'])} files")
        print(f"    ❌ Errors: {len(s['errors'])} files")
        print()


def change_folder():
    global TARGET_FOLDER
    print(f"\n📂 Current folder: {TARGET_FOLDER}")
    new = input("Enter new folder path: ").strip()
    if os.path.isdir(new):
        TARGET_FOLDER = new
        print(f"✅ Target folder changed to: {TARGET_FOLDER}\n")
    else:
        print("❌ Folder not found. Keeping current.\n")


# ── MAIN LOOP ────────────────────────────────────────────
print_banner()

while True:
    print(f"📂 Target: {TARGET_FOLDER}\n")
    print_menu()

    choice = input("Enter choice: ").strip()
    print()

    if choice == "1":
        preview(TARGET_FOLDER)

    elif choice == "2":
        confirm = input(f"Organize '{TARGET_FOLDER}' by TYPE? (yes/no): ").strip().lower()
        if confirm == "yes":
            organize(TARGET_FOLDER, mode="type")
        else:
            print("❌ Cancelled.\n")

    elif choice == "3":
        confirm = input(f"Organize '{TARGET_FOLDER}' by DATE? (yes/no): ").strip().lower()
        if confirm == "yes":
            organize(TARGET_FOLDER, mode="date")
        else:
            print("❌ Cancelled.\n")

    elif choice == "4":
        confirm = input(f"Organize '{TARGET_FOLDER}' by TYPE + DATE? (yes/no): ").strip().lower()
        if confirm == "yes":
            organize(TARGET_FOLDER, mode="both")
        else:
            print("❌ Cancelled.\n")

    elif choice == "5":
        undo_last(TARGET_FOLDER)

    elif choice == "6":
        view_logs()

    elif choice == "7":
        change_folder()

    elif choice == "0":
        print("👋 Bye! — CodeWithKenneth")
        break

    else:
        print("⚠️  Invalid choice. Try again.\n")