# ================================
#   STUDENT REGISTER
#   CodeWithKenneth
# ================================

students = []

print("=" * 40)
print("   WELCOME TO STUDENT REGISTER")
print("=" * 40)

while True:
    print("\nWhat do you want to do?")
    print("1. Add a student")
    print("2. View all students")
    print("3. Delete a student")
    print("4. Quit")

    choice = input("\nEnter your choice (1/2/3/4): ").strip()

    # ---- ADD STUDENT ----
    if choice == "1":
        print("\n--- ADD NEW STUDENT ---")
        first_name = input("Enter first name: ").strip()
        surname = input("Enter surname: ").strip()

        if first_name == "" or surname == "":
            print("❌ Name cannot be empty! Try again.")
        else:
            student_number = len(students) + 1
            students.append({
                "number": student_number,
                "first_name": first_name.capitalize(),
                "surname": surname.capitalize()
            })
            print(f"✅ {first_name.capitalize()} {surname.capitalize()} added successfully!")

    # ---- VIEW STUDENTS ----
    elif choice == "2":
        print("\n--- STUDENT REGISTER ---")
        if len(students) == 0:
            print("No students registered yet.")
        else:
            print(f"{'No.':<5} {'First Name':<15} {'Surname':<15}")
            print("-" * 35)
            for s in students:
                print(f"{s['number']:<5} {s['first_name']:<15} {s['surname']:<15}")
            print("-" * 35)
            print(f"Total Students: {len(students)}")

    # ---- DELETE STUDENT ----
    elif choice == "3":
        if len(students) == 0:
            print("No students to delete.")
        else:
            print("\n--- STUDENT REGISTER ---")
            print(f"{'No.':<5} {'First Name':<15} {'Surname':<15}")
            print("-" * 35)
            for s in students:
                print(f"{s['number']:<5} {s['first_name']:<15} {s['surname']:<15}")

            try:
                del_num = int(input("\nEnter student number to delete: "))
                found = False
                for s in students:
                    if s["number"] == del_num:
                        confirm = input(f"Delete {s['first_name']} {s['surname']}? (yes/no): ").lower()
                        if confirm == "yes":
                            students.remove(s)
                            for i, st in enumerate(students):
                                st["number"] = i + 1
                            print("✅ Student deleted.")
                        else:
                            print("❌ Deletion cancelled.")
                        found = True
                        break
                if not found:
                    print("❌ Student number not found.")
            except ValueError:
                print("❌ Please enter a valid number.")

    # ---- QUIT ----
    elif choice == "4":
        print("\nGoodbye! Keep coding 🚀 - CodeWithKenneth")
        break

    else:
        print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")