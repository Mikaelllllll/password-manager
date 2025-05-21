from password_manager import PasswordManager
from recent_file import save_recent_file, RECENT_PATH, load_recent_files

def main():
    password_manager = PasswordManager()
    recent = load_recent_files()
    print("🔐 Welcome to the Password Manager!")
    print("=" * 40)

    print("\n📂 Use a recent key file?")
    is_recent_keyfile_chosen = False
    is_recent_pwdfile_chosen = False
    keyfile = None
    for idx, path in enumerate(recent["keys"]):
        print(f"({idx + 1}) {path}")
    choosing_recent_files = input("➡️ Enter number or press Enter to skip: ")
    if choosing_recent_files.isdigit():
        path = recent["keys"][int(choosing_recent_files) - 1]
        password_manager.load_key(path)
        keyfile = recent["keys"][int(choosing_recent_files) - 1]
        is_recent_keyfile_chosen = True

    print(f"""
       You have entered the recent key file: {keyfile}!
        print("\n📂 Use a recent password file?")
       """)
    if is_recent_keyfile_chosen:
        for idx, path in enumerate(recent["passwords"]):
            print(f"({idx + 1}) {path}")
        choosing_recent_files = input("➡️ Enter number or press Enter to skip: ")
    if choosing_recent_files.isdigit():
        path = recent["passwords"][int(choosing_recent_files) - 1]
        password_manager.load_password_file(path)
        is_recent_pwdfile_chosen = True

    print("\n" + "=" * 40)
    print("🛠️  Main Menu")
    print("=" * 40)
    x = ("""Welcome to the password manager.
(1) 🔑 Create a new key
(2) 🔓 Load an existing key
(3) 📘 Create a new password file
(4) 📂 Load an existing password file
(5) ✏️  Manage passwords (add/edit/delete)
(6) 🔍 Get a saved password
(q) ❌ Quit
    """)
    print(x)

    while True:
        print(x)
        choice = input("👉 What would you like to do? ")

        if choice == "1":
            path = input("📝 Enter a path to save the new key: ")
            password_manager.create_key(path)
            save_recent_file("keys", path)

        elif choice == "2" and not is_recent_keyfile_chosen:
            path = input("📂️ Enter the key file path: ")
            password_manager.load_key(path)
            save_recent_file("keys", path)

        elif choice == "3":
            path = input("📘 Enter a path for the new password file: ")
            # Optional: add initial passwords
            initial = {}
            while True:
                add = input("➕ Add initial password? (y/n): ").lower()
                if add == 'y':
                    site = input("🔹Site: ")
                    pwd = input(f"🔹Password for {site}: ")
                    initial[site] = pwd
                else:
                    break
            password_manager.create_password_file(path, initial)
            save_recent_file("passwords", path)

        elif choice == "4" and not is_recent_pwdfile_chosen:
            path = input("📂 Enter the password file path: ")
            password_manager.load_password_file(path)
            save_recent_file("passwords", path)

        elif choice == "5":
            while True:
                print("\n🔧 Password Manager")

                print("""
            (a) Add a new password ➕
            (e) Edit a password ✏️
            (d) Delete a password 🗑️
            (b) Back to main menu 🔙

            """)
                modification = input("👉 What modification would you like to do? ")
                if modification == 'a':
                    site = input("🔹Enter the site name: ")
                    pwd = input(f"🔹Enter the password for {site}: ")
                    password_manager.add_password(site, pwd)
                elif modification == 'e':
                    site = input("🔹Enter the site name: ")
                    new_password = input("🔹Enter the new password: ")
                    password_manager.edit_password(site, new_password)
                elif modification == 'd':
                    site = input("🔹Enter the site name: ")
                    password_manager.remove_password(site)
                elif modification == 'b':
                    break
                else:
                    print("⚠️ Invalid modification.")


        elif choice == "6":
            site = input("🔍 Which site's password do you want? ")
            try:
                print(f"✅ Password for {site}: {password_manager.get_password(site)}")
            except KeyError:
                print("⚠️ Site not found.")

        elif choice.lower() == "q":
            print("👋 Thank you for using the password manager.")
            break

        else:
            print("⚠️ Invalid choice. Try again.")

if __name__ == "__main__":
    main()