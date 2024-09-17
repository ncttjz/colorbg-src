import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import winreg
import ctypes

def get_img():
    file_path = filedialog.askopenfilename(
        title='Choose image',
        filetypes=[('Image files', '*.jpg *.png *.jpeg')]
    )

    if file_path:
        # Show box confirm
        confirm = messagebox.askyesno("Confirm", "Do you want to set this image as your desktop background?")
        if confirm:
            # Change Background
            set_wallpaper(file_path)
        else:
            print("User chose not to set the image.")

def set_wallpaper(file_path):
    try:
        # Use Window API to change Background
        ctypes.windll.user32.SystemParametersInfoW(20, 0, file_path, 3)
        messagebox.showinfo("Success", "Background changed successfully!")
    except Exception as e:
        print(f"Error setting wallpaper: {e}")
        messagebox.showerror("Failed", "Failed to change background, try run tool as Administrator.")

def get_current_theme():
    """Lấy trạng thái theme hiện tại từ Windows registry."""
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
        use_light_theme, _ = winreg.QueryValueEx(reg_key, "AppsUseLightTheme")
        winreg.CloseKey(reg_key)
        return "light" if use_light_theme == 1 else "dark"
    except Exception as e:
        return "light"  # If cant read Registry, set light is default

def apply_theme():
    selected_theme = theme_var.get()

    # Set theme
    if selected_theme == "light":
        command = '''New-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" -Name "AppsUseLightTheme" -Value 1 -PropertyType DWORD -Force'''
        subprocess.run(["powershell", "-Command", command], shell=True)
        status_label.config(text="Light Color: ON")
    elif selected_theme == "dark":
        command = '''New-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize" -Name "AppsUseLightTheme" -Value 0 -PropertyType DWORD -Force'''
        subprocess.run(["powershell", "-Command", command], shell=True)
        status_label.config(text="Dark Color: ON")

# Application
root = tk.Tk()
root.title("ColorBG 1.0")
root.geometry("300x150")  # Size
root.iconbitmap('icon.ico')

# Current theme
current_theme = get_current_theme()

theme_var = tk.StringVar(value=current_theme)

# Button
light_color_rb = ttk.Radiobutton(root, text="Light Color", variable=theme_var, value="light", command=apply_theme)
dark_color_rb = ttk.Radiobutton(root, text="Dark Color", variable=theme_var, value="dark", command=apply_theme)

# Position
light_color_rb.grid(column=0, row=0, sticky=tk.W, padx=10, pady=5)
dark_color_rb.grid(column=0, row=1, sticky=tk.W, padx=10, pady=5)

# Theme Status
status_label = tk.Label(root, bg="SystemButtonFace")
status_label.grid(column=0, row=3, sticky=tk.W, padx=10, pady=10)

# Current Status
status_label.config(text=f"{current_theme.capitalize()} Color: ON")

# Change Background Button
change_img_button = tk.Button(root, text='Change Desktop Background', command=get_img)
change_img_button.grid(column=0, row=2, sticky=tk.W, padx=10, pady=10)

# Loop
root.mainloop()
