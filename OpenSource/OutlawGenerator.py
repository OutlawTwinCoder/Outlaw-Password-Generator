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
        'include_symbols': "Inclure des symboles",
        'symbol_mode': "Style de symboles :",
        'symbol_none': "Sans symboles",
        'symbol_simple': "Symboles standard",
        'symbol_complex': "Symboles avancés",
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
        'saved_passwords': "Mots de passe enregistrés",
        'no_passwords': "Aucun mot de passe enregistré pour le moment.",
        'regenerate_password': "Générer un nouveau mot de passe",
        'edit_password': "Modifier le mot de passe",
        'regenerate_success': "Un nouveau mot de passe a été généré.",
        'update_success': "Mot de passe mis à jour avec succès.",
        'cancel': "Annuler",
        'save_changes': "Enregistrer",
        'password_label': "Mot de passe :"
    },
    'en': {
        'title': "Outlaw Password Manager",
        'generate_password': "Generate Password",
        'app_name': "Application Name:",
        'username': "Username:",
        'subscription_active': "Active Subscription",
        'include_symbols': "Include Symbols",
        'symbol_mode': "Symbol style:",
        'symbol_none': "No Symbols",
        'symbol_simple': "Standard Symbols",
        'symbol_complex': "Extended Symbols",
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
        'saved_passwords': "Saved Passwords",
        'no_passwords': "No passwords saved yet.",
        'regenerate_password': "Generate New Password",
        'edit_password': "Edit Password",
        'regenerate_success': "A new password has been generated.",
        'update_success': "Password updated successfully.",
        'cancel': "Cancel",
        'save_changes': "Save Changes",
        'password_label': "Password:"
    }
}

# Current language variable
current_language = 'en'


def apply_modern_style(window):
    """Applies a refreshed style to the Tkinter widgets for a more modern look."""
    style = ttk.Style()
    try:
        style.theme_use('clam')
    except tk.TclError:
        pass

    background_color = '#0f172a'
    card_color = '#1f2937'
    accent_color = '#3b82f6'
    text_color = '#e2e8f0'

    window.configure(bg=background_color)

    style.configure('Main.TFrame', background=background_color)
    style.configure('Card.TFrame', background=card_color, relief='flat')
    style.configure('Header.TLabel', background=background_color, foreground='#f8fafc', font=('Segoe UI', 20, 'bold'))
    style.configure('Main.TLabel', background=background_color, foreground=text_color, font=('Segoe UI', 12))
    style.configure('CardTitle.TLabel', background=card_color, foreground='#f8fafc', font=('Segoe UI', 14, 'bold'))
    style.configure('CardText.TLabel', background=card_color, foreground=text_color, font=('Segoe UI', 11))
    style.configure('Accent.TButton', background=accent_color, foreground='#ffffff', font=('Segoe UI', 11, 'bold'), padding=8)
    style.map('Accent.TButton', background=[('active', '#2563eb')])
    style.configure('Secondary.TButton', background='#334155', foreground=text_color, font=('Segoe UI', 10), padding=6)
    style.map('Secondary.TButton', background=[('active', '#1e293b')])
    style.configure('Main.TEntry', fieldbackground='#111827', foreground=text_color)
    style.configure('Main.TCombobox', fieldbackground='#111827', foreground=text_color)
    style.configure('Switch.TCheckbutton', background=card_color, foreground=text_color, font=('Segoe UI', 10))


def parse_password_line(line):
    """Returns a tuple of (app_name, encrypted_username, encrypted_password, is_active)."""
    parts = line.strip().split("||")
    if not parts or all(not part for part in parts):
        return None
    while len(parts) < 4:
        parts.append('0')
    return parts[0], parts[1], parts[2], parts[3]


def format_password_line(app_name, encrypted_username, encrypted_password, is_active):
    """Formats the stored password line."""
    return f"{app_name}||{encrypted_username}||{encrypted_password}||{is_active}"

def get_symbol_mode_labels(language):
    """Returns the localized labels for the available symbol modes."""
    return {
        'none': translations[language]['symbol_none'],
        'simple': translations[language]['symbol_simple'],
        'complex': translations[language]['symbol_complex'],
    }


def update_language():
    """
    Updates the text labels and button names according to the current language setting.
    It pulls the translated strings from the 'translations' dictionary based on the current language.
    """
    if 'title_label' in globals() and title_label:
        title_label.config(text=translations[current_language]['title'])
    if 'generate_button' in globals() and generate_button:
        generate_button.config(text=translations[current_language]['generate_password'])
    if 'app_label' in globals() and app_label:
        app_label.config(text=translations[current_language]['app_name'])
    if 'user_label' in globals() and user_label:
        user_label.config(text=translations[current_language]['username'])
    if 'subscription_check' in globals() and subscription_check:
        subscription_check.config(text=translations[current_language]['subscription_active'])
    if 'length_label' in globals() and length_label:
        length_label.config(text=translations[current_language]['length'])
    if 'language_button' in globals() and language_button:
        language_button.config(text=translations[current_language]['language_button'])
    if 'symbol_mode_label' in globals() and symbol_mode_label:
        symbol_mode_label.config(text=translations[current_language]['symbol_mode'])
    if 'symbol_mode_menu' in globals() and symbol_mode_menu:
        labels = get_symbol_mode_labels(current_language)
        symbol_mode_menu['values'] = list(labels.values())
        if 'symbol_mode_menu_var' in globals() and symbol_mode_menu_var:
            symbol_mode_menu_var.set(labels[symbol_mode_var.get()])
    if 'saved_label' in globals() and saved_label:
        saved_label.config(text=translations[current_language]['saved_passwords'])
    update_password_list()


def on_symbol_mode_selected(event=None):
    """Updates the internal symbol mode variable when the combobox selection changes."""
    if 'symbol_mode_menu_var' not in globals() or not symbol_mode_menu_var:
        return
    labels = get_symbol_mode_labels(current_language)
    selection = symbol_mode_menu_var.get()
    for mode, label in labels.items():
        if label == selection:
            symbol_mode_var.set(mode)
            break

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

def generate_password(length=16, symbol_mode='simple'):
    """
    Generates a random password using letters, digits, and optional symbols.

    Parameters:
    - length (int): The length of the generated password. Defaults to 16.
    - symbol_mode (str): The symbol complexity to use ('none', 'simple', or 'complex').

    Returns:
    - str: The generated password.
    """
    chars = string.ascii_letters + string.digits
    if symbol_mode == 'simple':
        chars += '!@#$%&*?-'
    elif symbol_mode == 'complex':
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
        file.write(
            format_password_line(
                application,
                encrypted_username.decode(),
                encrypted_password.decode(),
                is_active,
            )
            + "\n"
        )
    
    messagebox.showinfo(translations[current_language]['save_success'], 
                        f"{translations[current_language]['save_success']} {application} et l'utilisateur {username}.")
    update_password_list()

def generate_and_save_password(event=None):
    """
    Generates a password based on the user’s selected options (length and symbol inclusion),
    then saves the generated password along with application and username details.
    """
    application = app_entry.get()
    username = user_entry.get()

    if not application or not username:
        messagebox.showwarning(translations[current_language]['error'], translations[current_language]['fill_fields'])
        return

    length = 16 if length_var.get() == 1 else 12
    symbol_mode = symbol_mode_var.get()

    password = generate_password(length=length, symbol_mode=symbol_mode)
    is_active = 1 if subscription_var.get() == 1 else 0

    try:
        save_password(application, username, password, is_active)
    except InvalidToken:
        messagebox.showerror(translations[current_language]['error'], translations[current_language]['master_password_error'])
        return

    app_entry.delete(0, tk.END)
    user_entry.delete(0, tk.END)
    subscription_var.set(0)


def handle_generate_shortcut(event=None):
    """Triggers password generation via the Enter key."""
    generate_and_save_password()
    return "break"


def handle_master_shortcut(event=None):
    """Submits the master password form with the Enter key."""
    verify_master_password()
    return "break"

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
            parsed = parse_password_line(line)
            if not parsed:
                continue
            applications.append(parsed)

    return applications

def toggle_display(app_frame, button):
    """
    Toggles between showing and hiding the username and password for a specific application in the UI.
    """
    if button.cget("text") == translations[current_language]['show']:
        button.username_label.config(text=app_frame.real_username)
        button.password_label.config(text=app_frame.real_password)
        button.config(text=translations[current_language]['hide'])
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
            parsed = parse_password_line(line)
            if not parsed:
                continue
            stored_app, stored_username, stored_password, is_active = parsed
            if stored_app == app_name and stored_username == encrypted_username:
                continue
            file.write(format_password_line(stored_app, stored_username, stored_password, is_active) + "\n")

    update_password_list()

def update_password_list():
    """
    Clears and updates the UI list of saved applications, showing the encrypted usernames and masked passwords.
    """
    if 'password_frame' not in globals() or not password_frame:
        return

    for widget in password_frame.winfo_children():
        widget.destroy()

    apps = list_applications()
    if not apps:
        empty_label = ttk.Label(password_frame, text=translations[current_language]['no_passwords'], style='Main.TLabel')
        empty_label.pack(pady=20)
        return

    for app_name, encrypted_username, encrypted_password, is_active in apps:
        card = ttk.Frame(password_frame, style='Card.TFrame', padding=12)
        card.pack(fill='x', padx=10, pady=6)

        header_frame = ttk.Frame(card, style='Card.TFrame')
        header_frame.pack(fill='x')

        title = ttk.Label(header_frame, text=app_name, style='CardTitle.TLabel')
        title.pack(side='left', anchor='w')

        delete_btn = ttk.Button(header_frame,
                                text=translations[current_language]['delete'],
                                style='Secondary.TButton',
                                command=lambda a=app_name, u=encrypted_username: confirm_delete_password(a, u))
        delete_btn.pack(side='right')

        info_frame = ttk.Frame(card, style='Card.TFrame')
        info_frame.pack(fill='x', pady=(10, 0))

        username_title = ttk.Label(info_frame, text=translations[current_language]['username'], style='CardText.TLabel')
        username_title.grid(row=0, column=0, sticky='w')
        username_label = ttk.Label(info_frame, text='****', style='CardText.TLabel')
        username_label.grid(row=1, column=0, sticky='w', pady=(2, 8))

        password_title = ttk.Label(info_frame, text=translations[current_language]['password_label'], style='CardText.TLabel')
        password_title.grid(row=0, column=1, sticky='w', padx=(20, 0))
        password_label = ttk.Label(info_frame, text='****', style='CardText.TLabel')
        password_label.grid(row=1, column=1, sticky='w', padx=(20, 0), pady=(2, 8))

        try:
            real_username = decrypt_message(encrypted_username.encode(), key)
            real_password = decrypt_message(encrypted_password.encode(), key)
        except InvalidToken:
            messagebox.showerror(translations[current_language]['error'], translations[current_language]['master_password_error'])
            return

        view_button = ttk.Button(info_frame,
                                 text=translations[current_language]['show'],
                                 style='Secondary.TButton')
        view_button.username_label = username_label
        view_button.password_label = password_label
        view_button.grid(row=1, column=2, padx=(20, 0))

        card.real_username = real_username
        card.real_password = real_password
        card.encrypted_username = encrypted_username
        card.encrypted_password = encrypted_password

        view_button.config(command=lambda f=card, b=view_button: toggle_display(f, b))

        buttons_frame = ttk.Frame(card, style='Card.TFrame')
        buttons_frame.pack(fill='x')

        copy_button = ttk.Button(buttons_frame,
                                 text=translations[current_language]['copy'],
                                 style='Secondary.TButton',
                                 command=lambda f=card: copy_to_clipboard(f.real_password, main_window))
        copy_button.pack(side='right', padx=(10, 0))

        regenerate_button = ttk.Button(buttons_frame,
                                       text=translations[current_language]['regenerate_password'],
                                       style='Accent.TButton',
                                       command=lambda a=app_name, u=encrypted_username: regenerate_existing_password(a, u))
        regenerate_button.pack(side='left', pady=(10, 0))

        edit_button = ttk.Button(buttons_frame,
                                 text=translations[current_language]['edit_password'],
                                 style='Secondary.TButton',
                                 command=lambda a=app_name, u=encrypted_username, p=encrypted_password: open_edit_window(a, u, p))
        edit_button.pack(side='left', padx=10, pady=(10, 0))

        subscription_var_local = tk.IntVar(value=int(is_active))
        subscription_check = ttk.Checkbutton(buttons_frame,
                                             text=translations[current_language]['subscription_active'],
                                             style='Switch.TCheckbutton',
                                             variable=subscription_var_local,
                                             command=lambda a=app_name, u=encrypted_username, v=subscription_var_local: update_subscription_status(a, u, v.get()))
        subscription_check.pack(side='left', padx=(20, 0), pady=(10, 0))


def regenerate_existing_password(app_name, encrypted_username):
    """Regenerates the password for an existing entry using the selected options."""
    try:
        username = decrypt_message(encrypted_username.encode(), key)
    except InvalidToken:
        messagebox.showerror(translations[current_language]['error'], translations[current_language]['master_password_error'])
        return

    length = 16 if length_var.get() == 1 else 12
    symbol_mode = symbol_mode_var.get()
    new_password = generate_password(length=length, symbol_mode=symbol_mode)

    update_password_entry(app_name, encrypted_username, app_name, username, new_password)
    messagebox.showinfo(translations[current_language]['generate_password'], translations[current_language]['regenerate_success'])
    update_password_list()


def update_password_entry(app_name, original_encrypted_username, new_app_name, new_username, new_password, is_active=None):
    """Updates the stored information for a given password entry."""
    if not os.path.exists("passwords.enc"):
        return

    encrypted_username = encrypt_message(new_username, key).decode()
    encrypted_password = encrypt_message(new_password, key).decode()

    with open("passwords.enc", "r") as file:
        lines = file.readlines()

    with open("passwords.enc", "w") as file:
        for line in lines:
            parsed = parse_password_line(line)
            if not parsed:
                continue
            stored_app, stored_username, stored_password, stored_active = parsed
            if stored_app == app_name and stored_username == original_encrypted_username:
                active_value = stored_active if is_active is None else str(is_active)
                file.write(format_password_line(new_app_name, encrypted_username, encrypted_password, active_value) + "\n")
            else:
                file.write(format_password_line(stored_app, stored_username, stored_password, stored_active) + "\n")


def open_edit_window(app_name, encrypted_username, encrypted_password):
    """Opens a window allowing the user to edit an existing password entry."""
    try:
        current_username = decrypt_message(encrypted_username.encode(), key)
        current_password = decrypt_message(encrypted_password.encode(), key)
    except InvalidToken:
        messagebox.showerror(translations[current_language]['error'], translations[current_language]['master_password_error'])
        return

    edit_window = tk.Toplevel(main_window)
    edit_window.title(translations[current_language]['edit_password'])
    center_window(edit_window, 420, 320)
    apply_modern_style(edit_window)
    edit_window.grab_set()

    content = ttk.Frame(edit_window, style='Main.TFrame', padding=20)
    content.pack(fill='both', expand=True)

    app_var = tk.StringVar(value=app_name)
    username_var = tk.StringVar(value=current_username)
    password_var = tk.StringVar(value=current_password)
    password_visible = tk.BooleanVar(value=False)

    app_label_local = ttk.Label(content, text=translations[current_language]['app_name'], style='Main.TLabel')
    app_label_local.pack(anchor='w')
    app_entry_local = ttk.Entry(content, textvariable=app_var)
    app_entry_local.pack(fill='x', pady=(0, 10))

    username_label_local = ttk.Label(content, text=translations[current_language]['username'], style='Main.TLabel')
    username_label_local.pack(anchor='w')
    username_entry_local = ttk.Entry(content, textvariable=username_var)
    username_entry_local.pack(fill='x', pady=(0, 10))

    password_label_local = ttk.Label(content, text=translations[current_language]['password_label'], style='Main.TLabel')
    password_label_local.pack(anchor='w')

    password_frame = ttk.Frame(content, style='Main.TFrame')
    password_frame.pack(fill='x', pady=(0, 10))

    password_entry_local = ttk.Entry(password_frame, textvariable=password_var, show='*')
    password_entry_local.pack(side='left', fill='x', expand=True)

    def toggle_password_visibility():
        password_visible.set(not password_visible.get())
        if password_visible.get():
            password_entry_local.config(show='')
            toggle_button.config(text=translations[current_language]['hide'])
        else:
            password_entry_local.config(show='*')
            toggle_button.config(text=translations[current_language]['show'])

    toggle_button = ttk.Button(password_frame,
                               text=translations[current_language]['show'],
                               style='Secondary.TButton',
                               command=toggle_password_visibility)
    toggle_button.pack(side='left', padx=(10, 0))

    buttons_frame = ttk.Frame(content, style='Main.TFrame')
    buttons_frame.pack(fill='x', pady=(10, 0))

    def save_changes():
        new_app = app_var.get().strip()
        new_username = username_var.get().strip()
        new_password_value = password_var.get()

        if not new_app or not new_username or not new_password_value:
            messagebox.showwarning(translations[current_language]['error'], translations[current_language]['fill_fields'])
            return

        update_password_entry(app_name, encrypted_username, new_app, new_username, new_password_value)
        messagebox.showinfo(translations[current_language]['edit_password'], translations[current_language]['update_success'])
        edit_window.destroy()
        update_password_list()

    save_button = ttk.Button(buttons_frame,
                              text=translations[current_language]['save_changes'],
                              style='Accent.TButton',
                              command=save_changes)
    save_button.pack(side='right')

    cancel_button = ttk.Button(buttons_frame,
                                text=translations[current_language]['cancel'],
                                style='Secondary.TButton',
                                command=edit_window.destroy)
    cancel_button.pack(side='right', padx=(0, 10))

    def submit(event=None):
        save_changes()
        return "break"

    edit_window.bind('<Return>', submit)
    app_entry_local.focus_set()

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
            parsed = parse_password_line(line)
            if not parsed:
                continue
            stored_app, stored_username, stored_password, stored_active = parsed
            if stored_app == app_name and stored_username == encrypted_username:
                stored_active = str(is_active)
            file.write(format_password_line(stored_app, stored_username, stored_password, stored_active) + "\n")

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
    global app_entry
    global user_entry
    global symbol_mode_var
    global symbol_mode_label
    global symbol_mode_menu
    global symbol_mode_menu_var
    global saved_label

    main_window = tk.Tk()
    main_window.title(translations[current_language]['title'])
    center_window(main_window, 800, 600)
    apply_modern_style(main_window)

    content = ttk.Frame(main_window, style='Main.TFrame', padding=20)
    content.pack(fill='both', expand=True)

    header_frame = ttk.Frame(content, style='Main.TFrame')
    header_frame.pack(fill='x')

    title_label = ttk.Label(header_frame, text=translations[current_language]['title'], style='Header.TLabel')
    title_label.pack(side='left')

    language_button = ttk.Button(header_frame, text=translations[current_language]['language_button'], style='Secondary.TButton', command=toggle_language)
    language_button.pack(side='right')

    options_frame = ttk.Frame(content, style='Main.TFrame')
    options_frame.pack(fill='x', pady=(20, 10))

    symbol_mode_label = ttk.Label(options_frame, text=translations[current_language]['symbol_mode'], style='Main.TLabel')
    symbol_mode_label.grid(row=0, column=0, sticky='w')

    symbol_mode_var = tk.StringVar(value='simple')
    symbol_mode_menu_var = tk.StringVar()
    symbol_mode_menu = ttk.Combobox(options_frame, textvariable=symbol_mode_menu_var, state='readonly', width=22)
    symbol_mode_menu.configure(style='Main.TCombobox')
    symbol_mode_menu.grid(row=1, column=0, sticky='w', pady=(5, 0))
    symbol_mode_menu.bind('<<ComboboxSelected>>', on_symbol_mode_selected)

    length_label = ttk.Label(options_frame, text=translations[current_language]['length'], style='Main.TLabel')
    length_label.grid(row=0, column=1, sticky='w', padx=(40, 0))

    length_var = tk.IntVar(value=1)
    length_radio_frame = ttk.Frame(options_frame, style='Main.TFrame')
    length_radio_frame.grid(row=1, column=1, sticky='w', padx=(40, 0), pady=(5, 0))

    length_radio_16 = ttk.Radiobutton(length_radio_frame, text='16', variable=length_var, value=1)
    length_radio_16.pack(side='left', padx=(0, 10))
    length_radio_12 = ttk.Radiobutton(length_radio_frame, text='12', variable=length_var, value=0)
    length_radio_12.pack(side='left')

    options_frame.columnconfigure(2, weight=1)

    app_label = ttk.Label(content, text=translations[current_language]['app_name'], style='Main.TLabel')
    app_label.pack(anchor='w')
    app_entry = ttk.Entry(content, width=50, style='Main.TEntry')
    app_entry.pack(fill='x', pady=(0, 10))

    user_label = ttk.Label(content, text=translations[current_language]['username'], style='Main.TLabel')
    user_label.pack(anchor='w')
    user_entry = ttk.Entry(content, width=50, style='Main.TEntry')
    user_entry.pack(fill='x', pady=(0, 10))

    subscription_var = tk.IntVar()
    subscription_check = ttk.Checkbutton(content,
                                         text=translations[current_language]['subscription_active'],
                                         style='Switch.TCheckbutton',
                                         variable=subscription_var)
    subscription_check.pack(anchor='w', pady=(0, 15))

    generate_button = ttk.Button(content,
                                 text=translations[current_language]['generate_password'],
                                 style='Accent.TButton',
                                 command=generate_and_save_password)
    generate_button.pack(fill='x', pady=(0, 20))

    saved_label = ttk.Label(content, text=translations[current_language]['saved_passwords'], style='Main.TLabel')
    saved_label.pack(anchor='w', pady=(0, 8))

    password_frame = ttk.Frame(content, style='Main.TFrame')
    password_frame.pack(fill='both', expand=True)

    update_language()

    main_window.bind('<Return>', handle_generate_shortcut)
    main_window.bind('<F11>', toggle_fullscreen)
    main_window.bind('<Escape>', end_fullscreen)

    main_window.mainloop()

def show_master_password_window():
    """
    Opens a window to prompt the user to enter or create the master password.
    """
    global master_window, master_entry, confirm_master_entry, current_language

    current_language = load_language()

    master_window = tk.Tk()
    master_window.title(translations[current_language]['confirm_password'])
    center_window(master_window, 350, 280)
    apply_modern_style(master_window)

    master_window.protocol("WM_DELETE_WINDOW", on_closing)

    container = ttk.Frame(master_window, style='Main.TFrame', padding=20)
    container.pack(fill='both', expand=True)

    confirm_master_entry = None

    try:
        if os.path.exists("passwords.enc"):
            master_label = ttk.Label(container, text=translations[current_language]['confirm_password'], style='Main.TLabel')
            master_label.pack(anchor='center', pady=(0, 10))

            master_entry = ttk.Entry(container, show="*", width=30, style='Main.TEntry')
            master_entry.pack(fill='x', pady=(0, 15))

            master_button = ttk.Button(container,
                                       text=translations[current_language]['confirm'],
                                       style='Accent.TButton',
                                       command=verify_master_password)
            master_button.pack(pady=(0, 10))
        else:
            create_label_text = translations[current_language]['create_master_password']
            confirm_label_text = translations[current_language]['confirm_password']

            master_label = ttk.Label(container, text=create_label_text, style='Main.TLabel')
            master_label.pack(anchor='center', pady=(0, 10))

            master_entry = ttk.Entry(container, show="*", width=30, style='Main.TEntry')
            master_entry.pack(fill='x', pady=(0, 10))

            confirm_master_label = ttk.Label(container, text=confirm_label_text, style='Main.TLabel')
            confirm_master_label.pack(anchor='center', pady=(0, 10))

            confirm_master_entry = ttk.Entry(container, show="*", width=30, style='Main.TEntry')
            confirm_master_entry.pack(fill='x', pady=(0, 10))

            warning_text = (
                "Attention : mémorisez bien votre mot de passe !\n"
                "Sinon, les mots de passe générés seront irrécupérables."
                if current_language == 'fr' else
                "Warning: Remember your password carefully!\n"
                "Otherwise, the generated passwords will be unrecoverable."
            )
            warning_label = ttk.Label(container, text=warning_text, style='Main.TLabel', foreground='#f87171')
            warning_label.pack(anchor='center', pady=(0, 10))

            master_button = ttk.Button(container,
                                       text=translations[current_language]['confirm'],
                                       style='Accent.TButton',
                                       command=verify_master_password)
            master_button.pack(pady=(0, 10))

    except Exception as e:
        messagebox.showerror(translations[current_language]['error'], f"Unexpected error: {str(e)}")

    master_entry.focus_set()
    master_window.bind('<Return>', handle_master_shortcut)
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

show_master_password_window()
