# ============================================
#      STUDENT FILE - CodeWithKenneth
# ============================================
# Pure Python | Runs in Pydroid 3 terminal
# No extra libraries needed!
# ============================================

# --- Student Data (list of dictionaries) ---
students = []


# --- Add a Student ---
def add_student():
    print("\n--- Add New Student ---")
    name = input("Enter student name: ")
    age = input("Enter student age: ")
    subject = input("Enter favourite subject: ")
    score = input("Enter student score (0-100): ")

    student = {
        "name": name,
        "age": age,
        "subject": subject,
        "score": int(score)
    }
    students.append(student)
    print(f"\n✅ {name} has been added successfully!")


# --- View All Students ---
def view_students():
    print("\n--- All Students ---")
    if len(students) == 0:
        print("No students added yet.")
        return

    for i, s in enumerate(students, 1):
        grade = get_grade(s["score"])
        print(f"\n#{i}")
        print(f"  Name    : {s['name']}")
        print(f"  Age     : {s['age']}")
        print(f"  Subject : {s['subject']}")
        print(f"  Score   : {s['score']}/100")
        print(f"  Grade   : {grade}")


# --- Search for a Student ---
def search_student():
    print("\n--- Search Student ---")
    keyword = input("Enter student name to search: ").lower()
    found = False

    for s in students:
        if keyword in s["name"].lower():
            grade = get_grade(s["score"])
            print(f"\n✅ Found!")
            print(f"  Name    : {s['name']}")
            print(f"  Age     : {s['age']}")
            print(f"  Subject : {s['subject']}")
            print(f"  Score   : {s['score']}/100")
            print(f"  Grade   : {grade}")
            found = True

    if not found:
        print("❌ No student found with that name.")


# --- Delete a Student ---
def delete_student():
    print("\n--- Delete Student ---")
    name = input("Enter student name to delete: ").lower()

    for i, s in enumerate(students):
        if s["name"].lower() == name:
            students.pop(i)
            print(f"✅ {s['name']} has been deleted.")
            return

    print("❌ Student not found.")


# --- Show Class Summary ---
def class_summary():
    print("\n--- Class Summary ---")
    if len(students) == 0:
        print("No students to summarize.")
        return

    total = len(students)
    avg_score = sum(s["score"] for s in students) / total
    highest = max(students, key=lambda s: s["score"])
    lowest  = min(students, key=lambda s: s["score"])

    print(f"  Total Students : {total}")
    print(f"  Average Score  : {avg_score:.1f}/100")
    print(f"  Highest Score  : {highest['name']} ({highest['score']})")
    print(f"  Lowest Score   : {lowest['name']} ({lowest['score']})")


# --- Grade Calculator ---
def get_grade(score):
    if score >= 70:
        return "A - Excellent 🌟"
    elif score >= 60:
        return "B - Good 👍"
    elif score >= 50:
        return "C - Average 😐"
    elif score >= 40:
        return "D - Below Average ⚠️"
    else:
        return "F - Fail ❌"


# --- Main Menu ---
def main():
    print("=" * 40)
    print("   STUDENT FILE - CodeWithKenneth")
    print("=" * 40)

    while True:
        print("\n📋 MENU")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Delete Student")
        print("5. Class Summary")
        print("6. Exit")

        choice = input("\nChoose an option (1-6): ")

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            class_summary()
        elif choice == "6":
            print("\n👋 Goodbye! - CodeWithKenneth")
            break
        else:
            print("❌ Invalid choice. Please enter 1-6.")


# --- Run the Program ---
main()