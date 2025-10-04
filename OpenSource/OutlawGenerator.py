import os
import random
import string
import hashlib
from cryptography.fernet import Fernet, InvalidToken
from base64 import urlsafe_b64encode
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Translation dictionary for English and French
translations = {
    'fr': {
        'title': "Outlaw Gestionnaire de Mot de Passe",
        'generate_password': "Générer le mot de passe",
        'app_name': "Nom de l'application:",
        'username': "Nom d'utilisateur:",
        'subscription_active': "Abonnement actif",
        'length': "Longueur:",
        'save_success': "Mot de passe sauvegardé pour",
        'error': "Erreur",
        'fill_fields': "Veuillez remplir tous les champs.",
        'quit': "Voulez-vous vraiment quitter?",
        'confirm': "Confirmer",
        'confirm_delete': "Entrez le mot de passe maître pour confirmer :",
        'delete': "Supprimer",
        'show': "Afficher",
        'hide': "Masquer",
        'copy': "Copier",
        'close': "Quitter",
        'password_copied': "Mot de passe copié dans le presse-papiers.",
        'confirm_password': "Confirmer",
        'validation_error': "Mot de passe maître incorrect.",
        'language_button': "English",
        'master_password_error': "Attention, le mot de passe que vous avez tenté de générer sera impossible à lire. Veuillez vérifier votre mot de passe maître avant de réessayer.",
        'create_master_password': "Créer votre mot de passe maître:",
        'symbol_mode': "Type de symboles:",
        'symbols_none': "Sans symboles",
        'symbols_standard': "Symboles standards",
        'symbols_extended': "Tous les symboles",
        'regenerate': "Nouveau mot de passe",
        'edit': "Modifier",
        'update_success': "Mot de passe mis à jour pour",
        'edit_title': "Modifier le mot de passe",
        'password_label': "Mot de passe:",
        'save_changes': "Enregistrer",
        'cancel': "Annuler",
        'empty_state': "Aucun mot de passe enregistré. Générer un mot de passe pour commencer!",
        'saved_passwords': "Mots de passe enregistrés"
    },
    'en': {
        'title': "Outlaw Password Manager",
        'generate_password': "Generate Password",
        'app_name': "Application Name:",
        'username': "Username:",
        'subscription_active': "Active Subscription",
        'length': "Length:",
        'save_success': "Password saved for",
        'error': "Error",
        'fill_fields': "Please fill all fields.",
        'quit': "Do you really want to quit?",
        'confirm': "Confirm",
        'confirm_delete': "Enter master password to confirm:",
        'delete': "Delete",
        'show': "Show",
        'hide': "Hide",
        'copy': "Copy",
        'close': "Close",
        'password_copied': "Password copied to clipboard.",
        'confirm_password': "Confirm",
        'validation_error': "Incorrect master password.",
        'language_button': "Français",
        'master_password_error': "Warning, the password you attempted to generate will be unreadable. Please check your master password and try again.",
        'create_master_password': "Create your master password:",
        'symbol_mode': "Symbol Style:",
        'symbols_none': "No Symbols",
        'symbols_standard': "Standard Symbols",
        'symbols_extended': "All Symbols",
        'regenerate': "Generate New",
        'edit': "Edit",
        'update_success': "Password updated for",
        'edit_title': "Edit Saved Password",
        'password_label': "Password:",
        'save_changes': "Save Changes",
        'cancel': "Cancel",
        'empty_state': "No passwords saved yet. Generate one to get started!",
        'saved_passwords': "Saved Passwords"
    }
}

# Current language variable
current_language = 'en'

styles_initialized = False
symbol_display_map = {}

master_entry = None
confirm_master_entry = None


def refresh_symbol_mode_options():
    """Update the symbol mode combobox choices according to the selected language."""
    global symbol_display_map
    if 'symbol_mode_combobox' not in globals() or 'symbol_mode_var' not in globals():
        return

    options = [
        translations[current_language]['symbols_none'],
        translations[current_language]['symbols_standard'],
        translations[current_language]['symbols_extended'],
    ]

    symbol_display_map = {
        'none': options[0],
        'standard': options[1],
        'extended': options[2],
    }

    if 'symbol_display_var' in globals():
        symbol_mode_combobox['values'] = list(symbol_display_map.values())
        symbol_display_var.set(symbol_display_map.get(symbol_mode_var.get(), options[2]))


def on_symbol_mode_change(event=None):
    """Synchronise the internal symbol mode when the user changes the combobox value."""
    if 'symbol_display_var' not in globals() or 'symbol_mode_var' not in globals():
        return

    selected_label = symbol_display_var.get()
    for mode_key, label in symbol_display_map.items():
        if label == selected_label:
            symbol_mode_var.set(mode_key)
            break


def initialize_styles():
    """Initialise custom ttk styles for the application UI."""
    global styles_initialized
    if styles_initialized:
        return

    style = ttk.Style()
    try:
        style.theme_use('clam')
    except tk.TclError:
        pass

    style.configure('App.TFrame', background='#0f172a')
    style.configure('Header.TFrame', background='#0f172a')
    style.configure('Card.TFrame', background='#1e293b')
    style.configure('ListItem.TFrame', background='#111c2d', relief='ridge')
    style.configure('Title.TLabel', background='#0f172a', foreground='#38bdf8', font=('Segoe UI', 20, 'bold'))
    style.configure('Card.TLabel', background='#1e293b', foreground='#e2e8f0', font=('Segoe UI', 11))
    style.configure('Section.TLabel', background='#1e293b', foreground='#f8fafc', font=('Segoe UI', 14, 'bold'))
    style.configure('Warning.TLabel', background='#1e293b', foreground='#f97316', font=('Segoe UI', 10))
    style.configure('BodyInverse.TLabel', background='#0f172a', foreground='#94a3b8', font=('Segoe UI', 10))

    style.configure('Primary.TButton', font=('Segoe UI', 11, 'bold'), foreground='#ffffff', background='#2563eb', padding=8)
    style.map('Primary.TButton', background=[('active', '#1d4ed8')])

    style.configure('Secondary.TButton', font=('Segoe UI', 10), foreground='#e2e8f0', background='#334155', padding=6)
    style.map('Secondary.TButton', background=[('active', '#475569')])

    style.configure('Accent.TButton', font=('Segoe UI', 10, 'bold'), foreground='#0f172a', background='#38bdf8', padding=6)
    style.map('Accent.TButton', background=[('active', '#0ea5e9')])

    style.configure('Danger.TButton', font=('Segoe UI', 10), foreground='#fecdd3', background='#7f1d1d', padding=6)
    style.map('Danger.TButton', background=[('active', '#991b1b')])

    style.configure('Card.TCheckbutton', background='#1e293b', foreground='#e2e8f0', font=('Segoe UI', 10))
    style.configure('Main.TCheckbutton', background='#1e293b', foreground='#e2e8f0', font=('Segoe UI', 11))
    style.configure('Card.TRadiobutton', background='#1e293b', foreground='#e2e8f0', font=('Segoe UI', 10))

    style.configure('Modern.TEntry', fieldbackground='#0f172a', foreground='#e2e8f0')
    style.map('Modern.TEntry', fieldbackground=[('focus', '#1e293b')])

    style.configure('Card.TCombobox', fieldbackground='#0f172a', foreground='#e2e8f0', padding=4)
    style.map('Card.TCombobox', fieldbackground=[('readonly', '#0f172a')])

    styles_initialized = True

def update_language():
    """
    Updates the text labels and button names according to the current language setting.
    It pulls the translated strings from the 'translations' dictionary based on the current language.
    """
    if 'title_label' in globals():
        title_label.config(text=translations[current_language]['title'])
    if 'generate_button' in globals():
        generate_button.config(text=translations[current_language]['generate_password'])
    if 'app_label' in globals():
        app_label.config(text=translations[current_language]['app_name'])
    if 'user_label' in globals():
        user_label.config(text=translations[current_language]['username'])
    if 'subscription_check' in globals():
        subscription_check.config(text=translations[current_language]['subscription_active'])
    if 'length_label' in globals():
        length_label.config(text=translations[current_language]['length'])
    if 'language_button' in globals():
        language_button.config(text=translations[current_language]['language_button'])
    if 'symbol_label' in globals():
        symbol_label.config(text=translations[current_language]['symbol_mode'])
        refresh_symbol_mode_options()
    if 'saved_label' in globals():
        saved_label.config(text=translations[current_language]['saved_passwords'])

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

def generate_password(length=16, symbol_mode='extended'):
    """
    Generates a random password using letters, digits, and optional symbols.

    Parameters:
    - length (int): The length of the generated password. Defaults to 16.
    - symbol_mode (str): Symbol preference ('none', 'standard', 'extended'). Defaults to 'extended'.

    Returns:
    - str: The generated password.
    """
    chars = string.ascii_letters + string.digits
    if symbol_mode == 'standard':
        chars += '!@#$%^&*()-_=+'
    elif symbol_mode == 'extended':
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
    application = app_entry.get().strip()
    username = user_entry.get().strip()

    if not application or not username:
        messagebox.showwarning(translations[current_language]['error'], translations[current_language]['fill_fields'])
        return

    length = 16 if length_var.get() == 1 else 12
    symbol_mode = symbol_mode_var.get() if 'symbol_mode_var' in globals() else 'extended'

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
                    app_frame.copy_button.config(command=lambda: copy_to_clipboard(app_frame.real_password, main_window))
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
    center_window(master_prompt, 340, 200)
    master_prompt.configure(bg="#0f172a")
    initialize_styles()
    master_prompt.transient(main_window)
    master_prompt.grab_set()

    container = ttk.Frame(master_prompt, style='Card.TFrame', padding=20)
    container.pack(fill='both', expand=True)

    prompt_label = ttk.Label(container, text=translations[current_language]['confirm_delete'], style='Card.TLabel', wraplength=260)
    prompt_label.pack(pady=(0, 10))

    password_entry = ttk.Entry(container, show="*", width=30, style='Modern.TEntry')
    password_entry.pack(fill='x', pady=(0, 10))
    password_entry.focus_set()

    button_row = ttk.Frame(container, style='Card.TFrame')
    button_row.pack(fill='x')

    confirm_button = ttk.Button(button_row, text=translations[current_language]['confirm'],
                                style='Primary.TButton', command=check_master_password)
    confirm_button.pack(side='right', padx=5)

    cancel_button = ttk.Button(button_row, text=translations[current_language]['cancel'],
                               style='Secondary.TButton', command=master_prompt.destroy)
    cancel_button.pack(side='right', padx=5)

    master_prompt.bind('<Return>', lambda event: (check_master_password(), 'break'))

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
            stripped = line.strip()
            if not stripped:
                continue
            parts = stripped.split("||")
            if len(parts) < 3:
                continue
            if parts[0] == app_name and parts[1] == encrypted_username:
                continue
            if len(parts) < 4:
                parts.append('0')
            file.write(f"{parts[0]}||{parts[1]}||{parts[2]}||{parts[3]}\n")

    update_password_list()


def update_password_record(original_app, original_encrypted_username, new_app, new_username, new_password, is_active):
    """Update the record of a saved password with new values."""
    with open("passwords.enc", "r") as file:
        lines = file.readlines()

    with open("passwords.enc", "w") as file:
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            parts = stripped.split("||")
            if len(parts) < 3:
                continue

            current_app, current_username, current_password = parts[:3]
            current_status = parts[3] if len(parts) > 3 else '0'

            if current_app == original_app and current_username == original_encrypted_username:
                encrypted_username = encrypt_message(new_username, key).decode()
                encrypted_password = encrypt_message(new_password, key).decode()
                current_app = new_app
                current_username = encrypted_username
                current_password = encrypted_password
                current_status = str(is_active)

            file.write(f"{current_app}||{current_username}||{current_password}||{current_status}\n")


def regenerate_password_for_entry(app_name, encrypted_username, is_active):
    """Generate a new password for an existing entry using the current options."""
    try:
        username = decrypt_message(encrypted_username.encode(), key)
    except InvalidToken:
        messagebox.showerror(translations[current_language]['error'], translations[current_language]['master_password_error'])
        return

    length = 16 if length_var.get() == 1 else 12
    symbol_mode = symbol_mode_var.get() if 'symbol_mode_var' in globals() else 'extended'
    new_password = generate_password(length=length, symbol_mode=symbol_mode)

    update_password_record(app_name, encrypted_username, app_name, username, new_password, is_active)
    messagebox.showinfo(translations[current_language]['generate_password'],
                        f"{translations[current_language]['update_success']} {app_name}.")
    update_password_list()


def open_edit_window(app_name, encrypted_username, encrypted_password, is_active):
    """Open a modal window allowing the user to edit an existing password entry."""
    try:
        current_username = decrypt_message(encrypted_username.encode(), key)
        current_password = decrypt_message(encrypted_password.encode(), key)
    except InvalidToken:
        messagebox.showerror(translations[current_language]['error'], translations[current_language]['master_password_error'])
        return

    edit_window = tk.Toplevel(main_window)
    edit_window.title(translations[current_language]['edit_title'])
    center_window(edit_window, 420, 360)
    edit_window.configure(bg="#0f172a")
    initialize_styles()
    edit_window.transient(main_window)
    edit_window.grab_set()

    container = ttk.Frame(edit_window, style='Card.TFrame', padding=20)
    container.pack(fill='both', expand=True)

    app_name_var = tk.StringVar(value=app_name)
    username_var = tk.StringVar(value=current_username)
    password_var = tk.StringVar(value=current_password)

    app_label_edit = ttk.Label(container, text=translations[current_language]['app_name'], style='Card.TLabel')
    app_label_edit.pack(anchor='w', pady=(0, 5))
    app_entry_edit = ttk.Entry(container, textvariable=app_name_var, style='Modern.TEntry')
    app_entry_edit.pack(fill='x', pady=(0, 10))

    username_label_edit = ttk.Label(container, text=translations[current_language]['username'], style='Card.TLabel')
    username_label_edit.pack(anchor='w', pady=(0, 5))
    username_entry_edit = ttk.Entry(container, textvariable=username_var, style='Modern.TEntry')
    username_entry_edit.pack(fill='x', pady=(0, 10))

    password_label_edit = ttk.Label(container, text=translations[current_language]['password_label'], style='Card.TLabel')
    password_label_edit.pack(anchor='w', pady=(0, 5))
    password_entry_edit = ttk.Entry(container, textvariable=password_var, style='Modern.TEntry')
    password_entry_edit.pack(fill='x', pady=(0, 10))

    button_row = ttk.Frame(container, style='Card.TFrame')
    button_row.pack(fill='x', pady=(10, 0))

    def save_changes():
        new_app_name = app_name_var.get().strip()
        new_username = username_var.get().strip()
        new_password_value = password_var.get().strip()

        if not new_app_name or not new_username or not new_password_value:
            messagebox.showwarning(translations[current_language]['error'], translations[current_language]['fill_fields'])
            return

        update_password_record(app_name, encrypted_username, new_app_name, new_username, new_password_value, is_active)
        messagebox.showinfo(translations[current_language]['edit_title'],
                            f"{translations[current_language]['update_success']} {new_app_name}.")
        edit_window.destroy()
        update_password_list()

    save_button = ttk.Button(button_row, text=translations[current_language]['save_changes'],
                             style='Primary.TButton', command=save_changes)
    save_button.pack(side='right', padx=5)

    cancel_button = ttk.Button(button_row, text=translations[current_language]['cancel'],
                               style='Secondary.TButton', command=edit_window.destroy)
    cancel_button.pack(side='right', padx=5)

    edit_window.bind('<Return>', lambda event: (save_changes(), 'break'))

def update_password_list():
    """
    Clears and updates the UI list of saved applications, showing the encrypted usernames and masked passwords.
    """
    for widget in password_frame.winfo_children():
        widget.destroy()

    apps = list_applications()
    if not apps:
        empty_label = ttk.Label(password_frame, text=translations[current_language]['empty_state'],
                                 style='Card.TLabel', anchor='center', justify='center')
        empty_label.pack(fill='both', expand=True, pady=40)
        return

    for app_name, encrypted_username, encrypted_password, is_active in apps:
        app_frame = ttk.Frame(password_frame, style='ListItem.TFrame', padding=12)
        app_frame.pack(fill='x', expand=True, padx=5, pady=6)

        for column_index in range(1, 4):
            app_frame.columnconfigure(column_index, weight=1)

        delete_button = ttk.Button(app_frame, text=translations[current_language]['delete'], style='Danger.TButton',
                                   command=lambda a=app_name, u=encrypted_username: confirm_delete_password(a, u))
        delete_button.grid(row=0, column=0, padx=4, pady=4, sticky='nsew')

        app_label = ttk.Label(app_frame, text=app_name, style='Card.TLabel')
        app_label.grid(row=0, column=1, padx=4, pady=4, sticky='w')

        username_label = ttk.Label(app_frame, text='****', style='Card.TLabel', width=18)
        username_label.grid(row=0, column=2, padx=4, pady=4, sticky='w')

        password_label = ttk.Label(app_frame, text='****', style='Card.TLabel', width=18)
        password_label.grid(row=0, column=3, padx=4, pady=4, sticky='w')

        try:
            real_username = decrypt_message(encrypted_username.encode(), key)
            real_password = decrypt_message(encrypted_password.encode(), key)
            app_frame.real_password = real_password
        except InvalidToken:
            messagebox.showerror(translations[current_language]['error'], translations[current_language]['master_password_error'])
            return

        view_button = ttk.Button(app_frame, text=translations[current_language]['show'], style='Secondary.TButton')
        view_button.username_label = username_label
        view_button.password_label = password_label
        view_button.config(command=lambda a=app_name, u=encrypted_username, f=app_frame, b=view_button: toggle_display(f, a, u, b))
        view_button.grid(row=0, column=4, padx=4, pady=4, sticky='nsew')

        copy_button = ttk.Button(app_frame, text=translations[current_language]['copy'], style='Secondary.TButton',
                                 command=lambda frame=app_frame: copy_to_clipboard(frame.real_password, main_window))
        copy_button.grid(row=0, column=5, padx=4, pady=4, sticky='nsew')
        app_frame.copy_button = copy_button

        regenerate_button = ttk.Button(app_frame, text=translations[current_language]['regenerate'], style='Secondary.TButton',
                                       command=lambda a=app_name, u=encrypted_username, s=is_active: regenerate_password_for_entry(a, u, s))
        regenerate_button.grid(row=0, column=6, padx=4, pady=4, sticky='nsew')

        edit_button = ttk.Button(app_frame, text=translations[current_language]['edit'], style='Secondary.TButton',
                                 command=lambda a=app_name, u=encrypted_username, p=encrypted_password, s=is_active: open_edit_window(a, u, p, s))
        edit_button.grid(row=0, column=7, padx=4, pady=4, sticky='nsew')

        subscription_var = tk.IntVar(value=int(is_active))
        subscription_check = ttk.Checkbutton(app_frame, text=translations[current_language]['subscription_active'],
                                             variable=subscription_var, style='Card.TCheckbutton',
                                             command=lambda a=app_name, u=encrypted_username, var=subscription_var: update_subscription_status(a, u, var.get()))
        subscription_check.grid(row=0, column=8, padx=4, pady=4, sticky='e')

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
            stripped = line.strip()
            if not stripped:
                continue
            parts = stripped.split("||")
            if len(parts) < 3:
                continue

            if len(parts) < 4:
                parts.append('0')

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
    global length_var
    global title_label
    global generate_button
    global app_label
    global user_label
    global length_label
    global language_button
    global subscription_check
    global symbol_label
    global symbol_mode_var
    global symbol_display_var
    global symbol_mode_combobox
    global saved_label

    main_window = tk.Tk()
    main_window.title(translations[current_language]['title'])
    center_window(main_window, 900, 640)
    main_window.configure(bg="#0f172a")
    initialize_styles()

    container = ttk.Frame(main_window, style='App.TFrame', padding=20)
    container.pack(fill='both', expand=True)

    header_frame = ttk.Frame(container, style='Header.TFrame')
    header_frame.pack(fill='x')

    title_label = ttk.Label(header_frame, text=translations[current_language]['title'], style='Title.TLabel')
    title_label.pack(side='left')

    language_button = ttk.Button(header_frame, text=translations[current_language]['language_button'],
                                 style='Accent.TButton', command=toggle_language)
    language_button.pack(side='right')

    form_card = ttk.Frame(container, style='Card.TFrame', padding=20)
    form_card.pack(fill='x', pady=(20, 10))
    form_card.columnconfigure(1, weight=1)

    app_label = ttk.Label(form_card, text=translations[current_language]['app_name'], style='Card.TLabel')
    app_label.grid(row=0, column=0, sticky='w', pady=(0, 6))
    global app_entry
    app_entry = ttk.Entry(form_card, width=40, style='Modern.TEntry')
    app_entry.grid(row=0, column=1, sticky='ew', pady=(0, 6))

    user_label = ttk.Label(form_card, text=translations[current_language]['username'], style='Card.TLabel')
    user_label.grid(row=1, column=0, sticky='w', pady=(0, 6))
    global user_entry
    user_entry = ttk.Entry(form_card, width=40, style='Modern.TEntry')
    user_entry.grid(row=1, column=1, sticky='ew', pady=(0, 6))

    symbol_label = ttk.Label(form_card, text=translations[current_language]['symbol_mode'], style='Card.TLabel')
    symbol_label.grid(row=2, column=0, sticky='w', pady=(0, 6))
    symbol_mode_var = tk.StringVar(value='extended')
    symbol_display_var = tk.StringVar()
    symbol_mode_combobox = ttk.Combobox(form_card, textvariable=symbol_display_var, state='readonly',
                                        style='Card.TCombobox')
    symbol_mode_combobox.grid(row=2, column=1, sticky='ew', pady=(0, 6))
    symbol_mode_combobox.bind('<<ComboboxSelected>>', on_symbol_mode_change)

    length_label = ttk.Label(form_card, text=translations[current_language]['length'], style='Card.TLabel')
    length_label.grid(row=3, column=0, sticky='w', pady=(0, 6))
    length_container = ttk.Frame(form_card, style='Card.TFrame')
    length_container.grid(row=3, column=1, sticky='w', pady=(0, 6))

    length_var = tk.IntVar(value=1)
    length_radio_16 = ttk.Radiobutton(length_container, text='16', variable=length_var, value=1, style='Card.TRadiobutton')
    length_radio_16.pack(side='left', padx=5)
    length_radio_12 = ttk.Radiobutton(length_container, text='12', variable=length_var, value=0, style='Card.TRadiobutton')
    length_radio_12.pack(side='left', padx=5)

    subscription_var = tk.IntVar()
    subscription_check = ttk.Checkbutton(form_card, text=translations[current_language]['subscription_active'],
                                         variable=subscription_var, style='Main.TCheckbutton')
    subscription_check.grid(row=4, column=0, columnspan=2, sticky='w', pady=(0, 6))

    generate_button = ttk.Button(form_card, text=translations[current_language]['generate_password'],
                                 style='Primary.TButton', command=generate_and_save_password)
    generate_button.grid(row=5, column=0, columnspan=2, sticky='ew', pady=(10, 0))

    list_card = ttk.Frame(container, style='Card.TFrame', padding=20)
    list_card.pack(fill='both', expand=True, pady=(10, 0))

    saved_label = ttk.Label(list_card, text=translations[current_language]['saved_passwords'], style='Section.TLabel')
    saved_label.pack(anchor='w')

    password_frame = ttk.Frame(list_card, style='Card.TFrame')
    password_frame.pack(fill='both', expand=True, pady=(12, 0))

    update_password_list()

    main_window.bind("<F11>", toggle_fullscreen)
    main_window.bind("<Escape>", end_fullscreen)
    main_window.bind("<Return>", lambda event: (generate_and_save_password(), 'break'))

    refresh_symbol_mode_options()
    update_language()

    main_window.mainloop()

def show_master_password_window():
    """
    Opens a window to prompt the user to enter or create the master password.
    """
    global master_window, master_entry, confirm_master_entry

    master_window = tk.Tk()
    master_window.title(translations[current_language]['confirm_password'])
    center_window(master_window, 420, 320)
    master_window.configure(bg="#0f172a")
    initialize_styles()
    master_window.protocol("WM_DELETE_WINDOW", on_closing)

    container = ttk.Frame(master_window, style='App.TFrame', padding=20)
    container.pack(fill='both', expand=True)

    card = ttk.Frame(container, style='Card.TFrame', padding=20)
    card.pack(fill='both', expand=True)

    try:
        if os.path.exists("passwords.enc"):
            master_label = ttk.Label(card, text=translations[current_language]['confirm_password'], style='Section.TLabel')
            master_label.pack(pady=(0, 15))

            master_entry = ttk.Entry(card, show="*", width=30, style='Modern.TEntry')
            master_entry.pack(fill='x', pady=(0, 15))
            master_entry.focus_set()

            master_button = ttk.Button(card, text=translations[current_language]['confirm'],
                                       style='Primary.TButton', command=verify_master_password)
            master_button.pack(pady=(5, 0))
        else:
            create_label_text = translations[current_language]['create_master_password']
            confirm_label_text = translations[current_language]['confirm_password']

            master_label = ttk.Label(card, text=create_label_text, style='Section.TLabel')
            master_label.pack(pady=(0, 12))

            master_entry = ttk.Entry(card, show="*", width=30, style='Modern.TEntry')
            master_entry.pack(fill='x', pady=(0, 12))
            master_entry.focus_set()

            confirm_master_label = ttk.Label(card, text=confirm_label_text, style='Card.TLabel')
            confirm_master_label.pack(pady=(0, 8), anchor='w')

            confirm_master_entry = ttk.Entry(card, show="*", width=30, style='Modern.TEntry')
            confirm_master_entry.pack(fill='x', pady=(0, 12))

            warning_text = (
                "Attention : mémorisez bien votre mot de passe !\n"
                "Sinon, les mots de passe générés seront irrécupérables."
                if current_language == 'fr' else
                "Warning: Remember your password carefully!\n"
                "Otherwise, the generated passwords will be unrecoverable."
            )
            warning_label = ttk.Label(card, text=warning_text, style='Warning.TLabel')
            warning_label.pack(pady=(0, 12))

            master_button = ttk.Button(card, text=translations[current_language]['confirm'],
                                       style='Primary.TButton', command=verify_master_password)
            master_button.pack(pady=(5, 0))

    except Exception as e:
        messagebox.showerror(translations[current_language]['error'], f"Unexpected error: {str(e)}")

    master_window.bind('<Return>', lambda event: (verify_master_password(), 'break'))
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

if __name__ == "__main__":
    current_language = load_language()
    show_master_password_window()
