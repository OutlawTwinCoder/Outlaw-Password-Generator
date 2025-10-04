import os
import random
import string
import hashlib
from cryptography.fernet import Fernet, InvalidToken
from base64 import urlsafe_b64encode
import tkinter as tk
from tkinter import messagebox

# Translation dictionary for English and French
translations = {
    'fr': {
        'title': "Outlaw Gestionnaire de Mot de Passe",
        'generate_password': "Générer le mot de passe",
        'app_name': "Nom de l'application:",
        'username': "Nom d'utilisateur:",
        'subscription_active': "Abonnement actif",
        'symbol_mode': "Type de symboles :",
        'password_field': "Mot de passe:",
        'symbols_none': "Aucun",
        'symbols_standard': "Standard",
        'symbols_advanced': "Avancé",
        'length': "Longueur:",
        'save_success': "Mot de passe sauvegardé pour",
        'update_success': "Mot de passe mis à jour pour",
        'regenerate_success': "Nouveau mot de passe généré pour",
        'update_error': "Impossible de mettre à jour le mot de passe.",
        'error': "Erreur",
        'fill_fields': "Veuillez remplir tous les champs.",
        'quit': "Voulez-vous vraiment quitter?",
        'confirm': "Confirmer",
        'confirm_delete': "Entrez le mot de passe maître pour confirmer :",
        'delete': "Supprimer",
        'edit': "Modifier",
        'regenerate': "Nouveau mot de passe",
        'show': "Afficher",
        'hide': "Masquer",
        'copy': "Copier",
        'close': "Quitter",
        'password_copied': "Mot de passe copié dans le presse-papiers.",
        'confirm_password': "Confirmer",
        'validation_error': "Mot de passe maître incorrect.",
        'language_button': "English",
        'master_password_error': "Attention, le mot de passe que vous avez tenté de générer sera impossible à lire. Veuillez vérifier votre mot de passe maître avant de réessayer.",
        'create_master_password': "Créer votre mot de passe maître:"
    },
    'en': {
        'title': "Outlaw Password Manager",
        'generate_password': "Generate Password",
        'app_name': "Application Name:",
        'username': "Username:",
        'subscription_active': "Active Subscription",
        'symbol_mode': "Symbol Type:",
        'password_field': "Password:",
        'symbols_none': "None",
        'symbols_standard': "Standard",
        'symbols_advanced': "Advanced",
        'length': "Length:",
        'save_success': "Password saved for",
        'update_success': "Password updated for",
        'regenerate_success': "New password generated for",
        'update_error': "Unable to update the password.",
        'error': "Error",
        'fill_fields': "Please fill all fields.",
        'quit': "Do you really want to quit?",
        'confirm': "Confirm",
        'confirm_delete': "Enter master password to confirm:",
        'delete': "Delete",
        'edit': "Edit",
        'regenerate': "Generate New Password",
        'show': "Show",
        'hide': "Hide",
        'copy': "Copy",
        'close': "Close",
        'password_copied': "Password copied to clipboard.",
        'confirm_password': "Confirm",
        'validation_error': "Incorrect master password.",
        'language_button': "Français",
        'master_password_error': "Warning, the password you attempted to generate will be unreadable. Please check your master password and try again.",
        'create_master_password': "Create your master password:"
    }
}

# Current language variable
current_language = 'en'

def update_language():
    """
    Updates the text labels and button names according to the current language setting.
    It pulls the translated strings from the 'translations' dictionary based on the current language.
    """
    title_label.config(text=translations[current_language]['title'])
    generate_button.config(text=translations[current_language]['generate_password'])
    app_label.config(text=translations[current_language]['app_name'])
    user_label.config(text=translations[current_language]['username'])
    subscription_check.config(text=translations[current_language]['subscription_active'])
    symbol_label.config(text=translations[current_language]['symbol_mode'])
    symbol_radio_none.config(text=translations[current_language]['symbols_none'])
    symbol_radio_standard.config(text=translations[current_language]['symbols_standard'])
    symbol_radio_advanced.config(text=translations[current_language]['symbols_advanced'])
    length_label.config(text=translations[current_language]['length'])
    language_button.config(text=translations[current_language]['language_button'])
    update_password_list()

def toggle_language():
    """
    Switches between 'en' (English) and 'fr' (French) for the application's interface.
    Updates the UI after changing the language.
    """
    global current_language
    current_language = 'en' if current_language == 'fr' else 'fr'
    update_language()
    save_language()

def center_window(window, width=800, height=600):
    """
    Centers the given window on the user's screen.

    Parameters:
    - window (tk.Tk or tk.Toplevel): The window to center.
    - width (int): The width of the window. Defaults to 800.
    - height (int): The height of the window. Defaults to 600.
    """
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def generate_password(length=16, symbol_mode='advanced'):
    """
    Generates a random password using letters, digits, and optional symbols.

    Parameters:
    - length (int): The length of the generated password. Defaults to 16.
    - symbol_mode (str): Controls which symbols to include. Can be 'none', 'standard', or 'advanced'.

    Returns:
    - str: The generated password.
    """
    chars = string.ascii_letters + string.digits
    if symbol_mode == 'standard':
        chars += "!@#$%^&*()-_=+[]{}"
    elif symbol_mode == 'advanced':
        chars += string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def derive_key_from_master_password(master_password):
    """
    Derives an encryption key from the master password using SHA-256 hashing.

    Parameters:
    - master_password (str): The master password to derive the key from.

    Returns:
    - bytes: A base64-encoded encryption key.
    """
    digest = hashlib.sha256(master_password.encode()).digest()
    return urlsafe_b64encode(digest)

def encrypt_message(message, key):
    """
    Encrypts a plaintext message using the provided encryption key.

    Parameters:
    - message (str): The plaintext message to encrypt.
    - key (bytes): The encryption key derived from the master password.

    Returns:
    - bytes: The encrypted message.
    """
    fernet = Fernet(key)
    return fernet.encrypt(message.encode())

def decrypt_message(encrypted_message, key):
    """
    Decrypts an encrypted message using the provided encryption key.

    Parameters:
    - encrypted_message (bytes): The message to decrypt.
    - key (bytes): The encryption key to use for decryption.

    Returns:
    - str: The decrypted message (plaintext).
    """
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_message).decode()

def save_password(application, username, password, is_active):
    """
    Encrypts and saves the generated password to a file, along with the associated application and username.

    Parameters:
    - application (str): The name of the application associated with the password.
    - username (str): The username for the application.
    - password (str): The generated password to save.
    - is_active (int): A flag to indicate whether the subscription is active (1) or not (0).
    """
    encrypted_username = encrypt_message(username, key)
    encrypted_password = encrypt_message(password, key)

    with open("passwords.enc", "a") as file:
        file.write(f"{application}||{encrypted_username.decode()}||{encrypted_password.decode()}||{is_active}\n")
    
    messagebox.showinfo(translations[current_language]['save_success'], 
                        f"{translations[current_language]['save_success']} {application} et l'utilisateur {username}.")
    update_password_list()

def generate_and_save_password():
    """
    Generates a password based on the user’s selected options (length and symbol inclusion),
    then saves the generated password along with application and username details.
    """
    application = app_entry.get()
    username = user_entry.get()

    if not application or not username:
        messagebox.showwarning(translations[current_language]['error'], translations[current_language]['fill_fields'])
        return

    symbol_mode = symbol_var.get()
    length = 16 if length_var.get() == 1 else 12

    password = generate_password(length=length, symbol_mode=symbol_mode)
    is_active = 1 if subscription_var.get() == 1 else 0
    
    try:
        save_password(application, username, password, is_active)
    except InvalidToken:
        messagebox.showerror(translations[current_language]['error'], translations[current_language]['master_password_error'])
        return

def list_applications():
    """
    Reads and decrypts the list of saved applications, usernames, and passwords from the encrypted file.

    Returns:
    - list: A list of tuples containing application names, encrypted usernames, encrypted passwords, and subscription status.
    """
    if not os.path.exists("passwords.enc"):
        return []

    applications = []
    with open("passwords.enc", "r") as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split("||")
            if len(parts) == 3:
                app_name, encrypted_username, encrypted_password = parts
                is_active = "0"
            elif len(parts) == 4:
                app_name, encrypted_username, encrypted_password, is_active = parts
            else:
                continue
            applications.append((app_name, encrypted_username, encrypted_password, is_active))
    
    return applications

def toggle_display(app_frame, app_choice, username_choice, button):
    """
    Toggles between showing and hiding the username and password for a specific application in the UI.

    Parameters:
    - app_frame (tk.Frame): The frame containing the application details.
    - app_choice (str): The name of the application.
    - username_choice (str): The encrypted username for the application.
    - button (tk.Button): The button to toggle between show/hide states.
    """
    if button.cget("text") == translations[current_language]['show']:
        with open("passwords.enc", "r") as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split("||")
                if app_choice in line and username_choice in line:
                    username = decrypt_message(username_choice.encode(), key)
                    password = decrypt_message(parts[2].encode(), key)

                    button.username_label.config(text=username)
                    button.password_label.config(text=password)
                    button.config(text=translations[current_language]['hide'])

                    app_frame.real_password = password
                    app_frame.copy_button.config(command=lambda pw=password: copy_to_clipboard(pw, main_window))
    else:
        button.username_label.config(text="****")
        button.password_label.config(text="****")
        button.config(text=translations[current_language]['show'])

def copy_to_clipboard(password, window):
    """
    Copies the given password to the system clipboard.

    Parameters:
    - password (str): The password to copy.
    - window (tk.Tk): The main window of the application to display the success message.
    """
    window.clipboard_clear()
    window.clipboard_append(password)
    messagebox.showinfo(translations[current_language]['copy'], translations[current_language]['password_copied'])

def confirm_delete_password(app_name, encrypted_username):
    """
    Prompts the user to enter the master password for confirmation before deleting a saved password.

    Parameters:
    - app_name (str): The name of the application whose password is being deleted.
    - encrypted_username (str): The encrypted username associated with the application.
    """
    def check_master_password():
        entered_password = password_entry.get()
        hashed_input = hashlib.sha256(entered_password.encode()).hexdigest()
        
        if key.decode() == urlsafe_b64encode(hashlib.sha256(entered_password.encode()).digest()).decode():
            delete_password(app_name, encrypted_username)
            master_prompt.destroy()
        else:
            messagebox.showerror(translations[current_language]['error'], translations[current_language]['validation_error'])
            master_prompt.destroy()

    master_prompt = tk.Toplevel(main_window)
    master_prompt.title(translations[current_language]['confirm'])
    center_window(master_prompt, 300, 150)

    prompt_label = tk.Label(master_prompt, text=translations[current_language]['confirm_delete'])
    prompt_label.pack(pady=10)

    password_entry = tk.Entry(master_prompt, show="*", width=30)
    password_entry.pack(pady=5)

    confirm_button = tk.Button(master_prompt, text=translations[current_language]['confirm'], command=check_master_password)
    confirm_button.pack(pady=10)

def delete_password(app_name, encrypted_username):
    """
    Deletes the saved password for a specific application by removing it from the file.

    Parameters:
    - app_name (str): The name of the application whose password is being deleted.
    - encrypted_username (str): The encrypted username associated with the application.
    """
    with open("passwords.enc", "r") as file:
        lines = file.readlines()

    with open("passwords.enc", "w") as file:
        for line in lines:
            parts = line.strip().split("||")
            if parts[0] == app_name and parts[1] == encrypted_username:
                continue
            file.write(line)

    update_password_list()

def update_password_record(original_app, original_encrypted_username, new_app,
                           new_encrypted_username, new_encrypted_password, new_is_active=None):
    """
    Updates an existing password entry with new values.

    Parameters:
    - original_app (str): The original application name to identify the record.
    - original_encrypted_username (str): The original encrypted username used to locate the record.
    - new_app (str): The updated application name.
    - new_encrypted_username (str): The updated encrypted username.
    - new_encrypted_password (str): The updated encrypted password.
    - new_is_active (str|None): Optional new subscription status. If None, keeps existing value.

    Returns:
    - bool: True if the record was updated, False otherwise.
    """
    if not os.path.exists("passwords.enc"):
        return False

    updated = False
    with open("passwords.enc", "r") as file:
        lines = file.readlines()

    with open("passwords.enc", "w") as file:
        for line in lines:
            parts = line.strip().split("||")
            if len(parts) < 3:
                continue

            current_active = parts[3] if len(parts) > 3 else "0"

            if not updated and parts[0] == original_app and parts[1] == original_encrypted_username:
                active_value = new_is_active if new_is_active is not None else current_active
                file.write(f"{new_app}||{new_encrypted_username}||{new_encrypted_password}||{active_value}\n")
                updated = True
            else:
                file.write(f"{parts[0]}||{parts[1]}||{parts[2]}||{current_active}\n")

    return updated

def edit_password(app_name, encrypted_username, encrypted_password, is_active):
    """
    Opens a window that allows the user to modify an existing password entry.
    """
    try:
        current_username = decrypt_message(encrypted_username.encode(), key)
        current_password = decrypt_message(encrypted_password.encode(), key)
    except InvalidToken:
        messagebox.showerror(translations[current_language]['error'], translations[current_language]['validation_error'])
        return

    edit_window = tk.Toplevel(main_window)
    edit_window.title(translations[current_language]['edit'])
    center_window(edit_window, 400, 260)
    edit_window.transient(main_window)

    app_name_label = tk.Label(edit_window, text=translations[current_language]['app_name'])
    app_name_label.pack(pady=5)
    app_name_entry = tk.Entry(edit_window, width=40)
    app_name_entry.insert(0, app_name)
    app_name_entry.pack(pady=5)

    username_label = tk.Label(edit_window, text=translations[current_language]['username'])
    username_label.pack(pady=5)
    username_entry = tk.Entry(edit_window, width=40)
    username_entry.insert(0, current_username)
    username_entry.pack(pady=5)

    password_label = tk.Label(edit_window, text=translations[current_language]['password_field'])
    password_label.pack(pady=5)
    password_entry = tk.Entry(edit_window, width=40)
    password_entry.insert(0, current_password)
    password_entry.pack(pady=5)

    def save_changes():
        new_app = app_name_entry.get().strip()
        new_username = username_entry.get().strip()
        new_password = password_entry.get().strip()

        if not new_app or not new_username or not new_password:
            messagebox.showwarning(translations[current_language]['error'], translations[current_language]['fill_fields'])
            return

        new_encrypted_username = encrypt_message(new_username, key).decode()
        new_encrypted_password = encrypt_message(new_password, key).decode()

        if update_password_record(app_name, encrypted_username, new_app, new_encrypted_username,
                                  new_encrypted_password, is_active):
            messagebox.showinfo(translations[current_language]['confirm'],
                                f"{translations[current_language]['update_success']} {new_app}.")
            edit_window.destroy()
            update_password_list()
        else:
            messagebox.showerror(translations[current_language]['error'], translations[current_language]['update_error'])

    buttons_frame = tk.Frame(edit_window)
    buttons_frame.pack(pady=10)

    save_button = tk.Button(buttons_frame, text=translations[current_language]['confirm'], command=save_changes)
    save_button.pack(side="left", padx=5)

    cancel_button = tk.Button(buttons_frame, text=translations[current_language]['close'], command=edit_window.destroy)
    cancel_button.pack(side="left", padx=5)

    edit_window.bind("<Return>", lambda event: save_changes())

def regenerate_password_for_entry(app_name, encrypted_username, is_active):
    """
    Generates a new password for an existing entry and saves it.
    """
    length = 16 if length_var.get() == 1 else 12
    symbol_mode = symbol_var.get()

    new_password = generate_password(length=length, symbol_mode=symbol_mode)
    new_encrypted_password = encrypt_message(new_password, key).decode()

    if update_password_record(app_name, encrypted_username, app_name, encrypted_username,
                              new_encrypted_password, is_active):
        messagebox.showinfo(translations[current_language]['confirm'],
                            f"{translations[current_language]['regenerate_success']} {app_name}.")
        update_password_list()
    else:
        messagebox.showerror(translations[current_language]['error'], translations[current_language]['update_error'])

def update_password_list():
    """
    Clears and updates the UI list of saved applications, showing the encrypted usernames and masked passwords.
    """
    for widget in password_frame.winfo_children():
        widget.destroy()

    apps = list_applications()
    if apps:
        for app_name, encrypted_username, encrypted_password, is_active in apps:
            app_frame = tk.Frame(password_frame, bg="white", bd=1, relief="solid")
            app_frame.pack(fill="x", padx=5, pady=5)

            delete_button = tk.Button(app_frame, text=translations[current_language]['delete'],
                                      command=lambda a=app_name, u=encrypted_username: confirm_delete_password(a, u))
            delete_button.grid(row=0, column=0, sticky="nsew")

            edit_button = tk.Button(app_frame, text=translations[current_language]['edit'],
                                    command=lambda a=app_name, u=encrypted_username, p=encrypted_password, s=is_active:
                                    edit_password(a, u, p, s))
            edit_button.grid(row=0, column=1, sticky="nsew")

            regenerate_button = tk.Button(app_frame, text=translations[current_language]['regenerate'],
                                          command=lambda a=app_name, u=encrypted_username, s=is_active:
                                          regenerate_password_for_entry(a, u, s))
            regenerate_button.grid(row=0, column=2, sticky="nsew")

            app_label = tk.Label(app_frame, text=app_name, width=20, relief="solid", borderwidth=1)
            app_label.grid(row=0, column=3, sticky="nsew")

            username_label = tk.Label(app_frame, text="****", width=20, relief="solid", borderwidth=1)
            username_label.grid(row=0, column=4, sticky="nsew")
            password_label = tk.Label(app_frame, text="****", width=20, relief="solid", borderwidth=1)
            password_label.grid(row=0, column=5, sticky="nsew")

            try:
                real_username = decrypt_message(encrypted_username.encode(), key)
                real_password = decrypt_message(encrypted_password.encode(), key)
                app_frame.real_password = real_password
            except InvalidToken:
                messagebox.showerror(translations[current_language]['error'], translations[current_language]['master_password_error'])
                return

            view_button = tk.Button(app_frame, text=translations[current_language]['show'])
            view_button.username_label = username_label
            view_button.password_label = password_label
            view_button.config(command=lambda a=app_name, u=encrypted_username, f=app_frame, b=view_button: toggle_display(f, a, u, b))
            view_button.grid(row=0, column=6, sticky="nsew")

            copy_button = tk.Button(app_frame, text=translations[current_language]['copy'],
                                    command=lambda pw=real_password: copy_to_clipboard(pw, main_window))
            copy_button.grid(row=0, column=7, sticky="nsew")

            app_frame.copy_button = copy_button

            subscription_var = tk.IntVar(value=int(is_active))

            subscription_check = tk.Checkbutton(app_frame, text=translations[current_language]['subscription_active'],
                                                variable=subscription_var,
                                                command=lambda a=app_name, u=encrypted_username, v=subscription_var: update_subscription_status(a, u, v.get()))
            subscription_check.grid(row=0, column=8, sticky="nsew")

def update_subscription_status(app_name, encrypted_username, is_active):
    """
    Updates the subscription status (active or inactive) of a saved application in the file.

    Parameters:
    - app_name (str): The name of the application whose subscription status is being updated.
    - encrypted_username (str): The encrypted username associated with the application.
    - is_active (int): The new subscription status (1 for active, 0 for inactive).
    """
    with open("passwords.enc", "r") as file:
        lines = file.readlines()

    with open("passwords.enc", "w") as file:
        for line in lines:
            parts = line.strip().split("||")
            if parts[0] == app_name and parts[1] == encrypted_username:
                parts[3] = str(is_active)
            file.write(f"{parts[0]}||{parts[1]}||{parts[2]}||{parts[3]}\n")

def on_closing():
    """
    Handles the closing of the application by showing a confirmation dialog and quitting the application cleanly if confirmed.
    """
    if messagebox.askokcancel(translations[current_language]['close'], translations[current_language]['quit']):
        master_window.destroy()
        main_window.quit()
        main_window.destroy()
        os._exit(0)

def save_master_password(master_password):
    """
    Hashes and returns the master password. This is used for comparison when validating the master password.
    
    Parameters:
    - master_password (str): The master password to hash.

    Returns:
    - str: The hashed master password.
    """
    return hashlib.sha256(master_password.encode()).hexdigest()

def verify_master_password():
    """
    Verifies the master password entered by the user. If it matches the stored password, allows access to the application.
    """
    global key
    global master_password_valid
    master_password_input = master_entry.get()

    if not os.path.exists("passwords.enc"):
        confirm_password = confirm_master_entry.get()

        if master_password_input == confirm_password:
            key = derive_key_from_master_password(master_password_input)
            master_password_valid = True
            messagebox.showinfo("Success", translations[current_language]['confirm_password'])
            master_window.destroy()
            open_main_window()
        else:
            master_password_valid = False
            messagebox.showerror(translations[current_language]['error'], translations[current_language]['validation_error'])
    else:
        key = derive_key_from_master_password(master_password_input)
        try:
            if list_applications():
                decrypt_message(list_applications()[0][1].encode(), key)
            master_password_valid = True
            master_window.destroy()
            open_main_window()
        except InvalidToken:
            master_password_valid = False
            messagebox.showerror(translations[current_language]['error'], translations[current_language]['validation_error'])

def toggle_fullscreen(event=None):
    """
    Enables fullscreen mode for the application window.
    """
    main_window.attributes("-fullscreen", True)

def end_fullscreen(event=None):
    """
    Disables fullscreen mode for the application window.
    """
    main_window.attributes("-fullscreen", False)

def open_main_window():
    """
    Opens the main application window and initializes the password management UI.
    """
    global main_window
    global password_frame
    global subscription_var
    global symbol_var
    global symbol_label
    global symbol_radio_none
    global symbol_radio_standard
    global symbol_radio_advanced
    global length_var
    global title_label
    global generate_button
    global app_label
    global user_label
    global length_label
    global language_button
    global subscription_check

    main_window = tk.Tk()
    main_window.title(translations[current_language]['title'])
    center_window(main_window, 960, 600)

    main_window.grid_rowconfigure(0, weight=1)
    main_window.grid_columnconfigure(0, weight=1)

    title_label = tk.Label(main_window, text=translations[current_language]['title'], font=("Arial", 16))
    title_label.pack(pady=10)

    options_frame = tk.Frame(main_window)
    options_frame.pack(pady=10)

    language_button = tk.Button(main_window, text=translations[current_language]['language_button'], command=toggle_language)
    language_button.place(x=10, y=10)

    symbol_var = tk.StringVar(value='standard')
    symbol_frame = tk.Frame(options_frame)
    symbol_frame.pack(side="left", padx=10)

    symbol_label = tk.Label(symbol_frame, text=translations[current_language]['symbol_mode'])
    symbol_label.pack(side="left", padx=(0, 5))

    symbol_radio_none = tk.Radiobutton(symbol_frame, text=translations[current_language]['symbols_none'],
                                       variable=symbol_var, value='none')
    symbol_radio_none.pack(side="left", padx=2)

    symbol_radio_standard = tk.Radiobutton(symbol_frame, text=translations[current_language]['symbols_standard'],
                                           variable=symbol_var, value='standard')
    symbol_radio_standard.pack(side="left", padx=2)

    symbol_radio_advanced = tk.Radiobutton(symbol_frame, text=translations[current_language]['symbols_advanced'],
                                           variable=symbol_var, value='advanced')
    symbol_radio_advanced.pack(side="left", padx=2)

    length_var = tk.IntVar(value=1)
    length_label = tk.Label(options_frame, text=translations[current_language]['length'])
    length_label.pack(side="left", padx=10)
    length_radio_16 = tk.Radiobutton(options_frame, text="16", variable=length_var, value=1)
    length_radio_12 = tk.Radiobutton(options_frame, text="12", variable=length_var, value=0)
    length_radio_16.pack(side="left", padx=5)
    length_radio_12.pack(side="left", padx=5)

    app_label = tk.Label(main_window, text=translations[current_language]['app_name'])
    app_label.pack(pady=5)
    global app_entry
    app_entry = tk.Entry(main_window, width=40)
    app_entry.pack(pady=5)

    user_label = tk.Label(main_window, text=translations[current_language]['username'])
    user_label.pack(pady=5)
    global user_entry
    user_entry = tk.Entry(main_window, width=40)
    user_entry.pack(pady=5)

    subscription_var = tk.IntVar()
    subscription_check = tk.Checkbutton(main_window, text=translations[current_language]['subscription_active'], variable=subscription_var)
    subscription_check.pack(pady=5)

    generate_button = tk.Button(main_window, text=translations[current_language]['generate_password'], command=generate_and_save_password)
    generate_button.pack(pady=10)

    password_frame = tk.Frame(main_window, bg="white", relief="sunken", borderwidth=1)
    password_frame.pack(fill="both", expand=True, padx=10, pady=10)

    update_password_list()

    main_window.bind("<Return>", lambda event: generate_and_save_password())
    main_window.bind("<F11>", toggle_fullscreen)
    main_window.bind("<Escape>", end_fullscreen)

    update_language()

    main_window.mainloop()

def show_master_password_window():
    """
    Opens a window to prompt the user to enter or create the master password.
    """
    global master_window, master_entry, confirm_master_entry

    master_window = tk.Tk()
    master_window.title(translations[current_language]['confirm_password'])
    center_window(master_window, 350, 250)

    master_window.protocol("WM_DELETE_WINDOW", on_closing)

    try:
        if os.path.exists("passwords.enc"):
            master_label = tk.Label(master_window, text=translations[current_language]['confirm_password'])
            master_label.pack(pady=10)

            master_entry = tk.Entry(master_window, show="*", width=30)
            master_entry.pack(pady=10)

            master_button = tk.Button(master_window, text=translations[current_language]['confirm'], command=verify_master_password)
            master_button.pack(pady=10)
        else:
            create_label_text = translations[current_language]['create_master_password']
            confirm_label_text = translations[current_language]['confirm_password']

            master_label = tk.Label(master_window, text=create_label_text)
            master_label.pack(pady=10)

            master_entry = tk.Entry(master_window, show="*", width=30)
            master_entry.pack(pady=10)

            confirm_master_label = tk.Label(master_window, text=confirm_label_text)
            confirm_master_label.pack(pady=10)

            confirm_master_entry = tk.Entry(master_window, show="*", width=30)
            confirm_master_entry.pack(pady=10)

            warning_text = (
                "Attention : mémorisez bien votre mot de passe !\n"
                "Sinon, les mots de passe générés seront irrécupérables."
                if current_language == 'fr' else
                "Warning: Remember your password carefully!\n"
                "Otherwise, the generated passwords will be unrecoverable."
            )
            warning_label = tk.Label(master_window, text=warning_text, fg="red")
            warning_label.pack(pady=10)

            master_button = tk.Button(master_window, text=translations[current_language]['confirm'], command=verify_master_password)
            master_button.pack(pady=10)

    except Exception as e:
        messagebox.showerror(translations[current_language]['error'], f"Unexpected error: {str(e)}")

    master_window.mainloop()

def load_language():
    """
    Loads the saved language from a configuration file, or defaults to 'fr' if the file doesn't exist.

    Returns:
    - str: The loaded language.
    """
    if os.path.exists("langue.conf"):
        with open("langue.conf", "r") as file:
            language = file.read().strip()
            if language in translations:
                return language
    return 'fr'

def save_language():
    """
    Saves the current language setting to a configuration file.
    """
    with open("langue.conf", "w") as file:
        file.write(current_language)

current_language = load_language()

show_master_password_window()
