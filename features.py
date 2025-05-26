# qr_code_generator.py

import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
import qrcode
from PIL import Image, ImageTk
from reportlab.pdfgen import canvas
import os

# ----- CONFIG -----
DEFAULT_FOREGROUND = "black"
DEFAULT_BACKGROUND = "white"

class QRCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("500x600")

        self.fore_color = DEFAULT_FOREGROUND
        self.back_color = DEFAULT_BACKGROUND
        self.logo_path = None
        self.qr_image = None

        # Input Field
        tk.Label(root, text="Enter text or URL:").pack(pady=5)
        self.input_text = tk.Entry(root, width=40)
        self.input_text.pack(pady=5)

        # Buttons
        tk.Button(root, text="Choose Foreground Color", command=self.choose_foreground).pack(pady=5)
        tk.Button(root, text="Choose Background Color", command=self.choose_background).pack(pady=5)
        tk.Button(root, text="Upload Logo", command=self.upload_logo).pack(pady=5)
        tk.Button(root, text="Generate QR Code", command=self.generate_qr).pack(pady=10)

        # QR Display
        self.qr_display = tk.Label(root)
        self.qr_display.pack(pady=10)

        # Save Buttons
        tk.Button(root, text="Save as PNG", command=self.save_png).pack(pady=5)
        tk.Button(root, text="Save as PDF", command=self.save_pdf).pack(pady=5)

    # Color pickers
    def choose_foreground(self):
        color = colorchooser.askcolor(title="Choose Foreground Color")[1]
        if color:
            self.fore_color = color

    def choose_background(self):
        color = colorchooser.askcolor(title="Choose Background Color")[1]
        if color:
            self.back_color = color

    # Upload logo image
    def upload_logo(self):
        self.logo_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if self.logo_path:
            messagebox.showinfo("Logo Uploaded", "Logo successfully uploaded!")

    # Generate QR with logo and color
    def generate_qr(self):
        data = self.input_text.get()
        if not data:
            messagebox.showwarning("Input Required", "Please enter text or a URL.")
            return

        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color=self.fore_color, back_color=self.back_color).convert('RGB')

        if self.logo_path:
            logo = Image.open(self.logo_path)
            qr_width, qr_height = img.size
            logo_size = qr_width // 4
            logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
            pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)

        self.qr_image = img
        qr_tk = ImageTk.PhotoImage(img)
        self.qr_display.config(image=qr_tk)
        self.qr_display.image = qr_tk

    # Save as PNG
    def save_png(self):
        if self.qr_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
            if file_path:
                self.qr_image.save(file_path)
                messagebox.showinfo("Saved", f"QR code saved as PNG: {file_path}")
#yyy
    # Save as PDF
    def save_pdf(self):
        if self.qr_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
            if file_path:
                temp_png = "temp_qr.png"
                self.qr_image.save(temp_png)

                c = canvas.Canvas(file_path)
                c.drawImage(temp_png, 100, 500, width=300, height=300)
                c.save()

                os.remove(temp_png)
                messagebox.showinfo("Saved", f"QR code saved as PDF: {file_path}")

# ---- Main Execution ----
if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeApp(root)
    root.mainloop()
