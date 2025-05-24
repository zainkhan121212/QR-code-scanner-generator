import tkinter as tk
from tkinter import ttk

# Main Window
root = tk.Tk()
root.title("QR Code Tool")
root.geometry("600x400")  # Start with a larger size
root.configure(bg='#f0f0f0')

# Fonts
heading_font = ("Arial", 16, "bold")
label_font = ("Arial", 12)
button_font = ("Arial", 11)

# Tab Control Styling
style = ttk.Style()
style.theme_use('default')
style.configure('TNotebook.Tab', background='#d9d9d9', padding=[10, 5])
style.map('TNotebook.Tab', background=[('selected', '#4a90e2')],
          foreground=[('selected', 'white')])

tab_control = ttk.Notebook(root)

# Use tk.Frame for background color support
generate_tab = tk.Frame(tab_control, bg='white')
scan_tab = tk.Frame(tab_control, bg='white')

tab_control.add(generate_tab, text='Generate QR')
tab_control.add(scan_tab, text='Scan QR')
tab_control.pack(expand=1, fill='both')

# ---------- Generate QR Tab ----------
generate_heading = tk.Label(generate_tab, text="Generate QR Code", font=heading_font, bg='white', fg='#333')
generate_heading.pack(pady=15)

generate_label = tk.Label(generate_tab, text="Enter text to generate QR:", font=label_font, bg='white', fg='#333')
generate_label.pack(pady=5)

generate_entry = tk.Entry(generate_tab, font=label_font, width=40)
generate_entry.pack(pady=5)

generate_button = tk.Button(generate_tab, text="Generate QR", font=button_font, bg='#4a90e2', fg='white')
generate_button.pack(pady=15)

# ---------- Scan QR Tab ----------
scan_heading = tk.Label(scan_tab, text="Scan QR Code", font=heading_font, bg='white', fg='#333')
scan_heading.pack(pady=20)

scan_label = tk.Label(scan_tab, text="Scan QR code using webcam:", font=label_font, bg='white', fg='#333')
scan_label.pack(pady=5)

scan_button = tk.Button(scan_tab, text="Scan QR", font=button_font, bg='#4a90e2', fg='white')
scan_button.pack(pady=15)

# Run the App
root.mainloop()
#paste ur work here..
