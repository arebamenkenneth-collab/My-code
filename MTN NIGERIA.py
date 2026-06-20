import os
import time

def clear():
    os.system("clear")

def border(text):
    width = 40
    print("=" * width)
    print(text.center(width))
    print("=" * width)

def show_result(title, message):
    clear()
    border("MTN NIGERIA")
    print()
    print(f"  {title}")
    print()
    for line in message.split("\n"):
        print(f"  {line}")
    print()
    print("=" * 40)
    print()
    input("  Press Enter to go back... ")

def ussd_menu():
    clear()
    border("MTN NIGERIA")
    print()
    print("  Welcome to MTN USSD Menu")
    print("  *101#")
    print()
    print("  1. Buy Data")
    print("  2. Buy Airtime")
    print("  3. Gift Data")
    print("  4. Like CodeWithKenneth Video")
    print("  5. Follow CodeWithKenneth")
    print("  6. Share CodeWithKenneth")
    print()
    print("  0. End Session")
    print()
    print("=" * 40)

def run():
    while True:
        clear()
        border("MTN NIGERIA DIALER")
        print()
        print("  Dial a USSD code to begin.")
        print()
        code = input("  Enter code: ").strip()

        if code == "*101#":
            while True:
                ussd_menu()
                choice = input("  Enter option: ").strip()

                if choice == "1":
                    show_result(
                        "Buy Data",
                        "Select a bundle:\n\n"
                        "  1. 1GB  - N300\n"
                        "  2. 3GB  - N1,000\n"
                        "  3. 10GB - N2,000\n\n"
                        "Dial *101*1*[option]# to proceed."
                    )

                elif choice == "2":
                    show_result(
                        "Buy Airtime",
                        "Dial: *101*2*[amount]#\n\n"
                        "Minimum: N50\n"
                        "Maximum: N50,000"
                    )

                elif choice == "3":
                    show_result(
                        "Gift Data",
                        "Dial: *101*3*[number]*[bundle]#\n\n"
                        "Your friend gets the data instantly!"
                    )

                elif choice == "4":
                    clear()
                    border("MTN NIGERIA")
                    print()
                    print("  ACTION CONFIRMED!")
                    print()
                    print("  You just liked CodeWithKenneth's")
                    print("  video!")
                    print()
                    print("  Kenneth codes ENTIRELY on Android")
                    print("  using Pydroid 3 - and so can you!")
                    print()
                    print("  Follow @arebamenkenneth on TikTok")
                    print()
                    print("=" * 40)
                    print()
                    input("  Press Enter to go back... ")

                elif choice == "5":
                    clear()
                    border("MTN NIGERIA")
                    print()
                    print("  YOU ARE NOW FOLLOWING!")
                    print()
                    print("  You are now following")
                    print("  CodeWithKenneth!")
                    print()
                    print("  Welcome to the community where")
                    print("  we prove you don't need a laptop")
                    print("  to build ANYTHING in Python!")
                    print()
                    print("  Join the WhatsApp class today!")
                    print()
                    print("=" * 40)
                    print()
                    input("  Press Enter to go back... ")

                elif choice == "6":
                    show_result(
                        "Share CodeWithKenneth",
                        "Copy and send to your friends:\n\n"
                        "I found a Python teacher who\n"
                        "codes ONLY on his phone!\n\n"
                        "Check out CodeWithKenneth\n"
                        "@arebamenkenneth on TikTok\n"
                        "and join the free class!"
                    )

                elif choice == "0":
                    clear()
                    border("MTN NIGERIA")
                    print()
                    print("  Session ended.")
                    print()
                    time.sleep(1.5)
                    break

                else:
                    clear()
                    border("MTN NIGERIA")
                    print()
                    print("  Invalid option.")
                    print("  Please choose 1 to 6.")
                    print()
                    time.sleep(1.5)

        elif code == "0" or code.lower() == "exit":
            clear()
            print("  Goodbye!")
            break

        else:
            clear()
            border("ERROR")
            print()
            print(f"  '{code}' is not a valid USSD code.")
            print("  Try dialing: *101#")
            print()
            time.sleep(2)

if __name__ == "__main__":
    run()