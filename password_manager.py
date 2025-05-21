from cryptography.fernet import Fernet


class PasswordManager:
    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)
        print(f"Key saved to {path}.")

    def load_key(self, path):
        try:
            with open(path, 'rb') as f:
                self.key = f.read()
            print(f"Key loaded from {path}.")
        except FileNotFoundError:
            print("Key file not found.")

    def create_password_file(self, path, initial_values=None):
        self.password_file = path
        if initial_values is not None:
            for site, password in initial_values.items():
                self.add_password(site, password)
        print(f"Password file created at {path}.")

    def load_password_file(self, path):
        self.password_file = path
        try:
            with open(path, 'r') as f:
                for line in f:
                    site, encrypted_password = line.strip().split(':', 1)
                    decrypted_password = Fernet(self.key).decrypt(encrypted_password.encode()).decode()
                    self.password_dict[site] = decrypted_password
            print(f"Passwords loaded from {path}.")
        except FileNotFoundError:
            print("Password file not found.")
        except Exception as e:
            print(f"Error loading passwords: {e}")

    def add_password(self, site, password):
        if not self.key:
            print("Key not loaded.")
            return
        self.password_dict[site] = password
        if self.password_file is not None:
            with open(self.password_file, 'a') as f:
                encrypted_password = Fernet(self.key).encrypt(password.encode())
                f.write(site + ':' + encrypted_password.decode() + "\n")
            print(f"Password for {site} added.")

    def remove_password(self, site):
        if site not in self.password_dict:
            print("Password not found.")
            return

        del self.password_dict[site]

        if self.password_file:
            with open(self.password_file, 'w') as f:
                for s,p in self.password_dict.items():
                    encrypted_password = Fernet(self.key).encrypt(p.encode()).decode()
                    f.write(s + ':' + encrypted_password + "\n")
            print(f"Password for {site} removed.")

    def edit_password(self, site, new_password):
        if site not in self.password_dict:
            print("Password not found.")
            return

        self.password_dict[site] = new_password

        if self.password_file is not None:
            with open(self.password_file, 'w') as f:
                for s, p in self.password_dict.items():
                    encrypted_password = Fernet(self.key).encrypt(p.encode())
                    f.write(s + ':' + encrypted_password.decode() + "\n")
            print(f"Password for {site} edited.")



    def get_password(self, site):
        return self.password_dict.get(site, "Password not found.")

