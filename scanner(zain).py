import cv2
import numpy as np
from pyzbar import pyzbar
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox
#hhh
class QRCodeScanner:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Scanner")
        self.setup_ui()
        self.cap = None
        self.scanning = False

    def setup_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.camera_label = ttk.Label(main_frame)
        self.camera_label.pack(pady=5)

        self.result_text = tk.StringVar()
        result_entry = ttk.Entry(main_frame, textvariable=self.result_text, width=40, state='readonly')
        result_entry.pack(pady=5)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Start Scanning", command=self.start_scanning).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Stop Scanning", command=self.stop_scanning).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Copy Result", command=self.copy_result).pack(side=tk.LEFT, padx=5)

    def start_scanning(self):
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Camera not accessible!")
                return
            self.scanning = True
            self.update_camera()
        except Exception as e:
            messagebox.showerror("Error", f"Camera error: {str(e)}")

    def stop_scanning(self):
        self.scanning = False
        if self.cap and self.cap.isOpened():
            self.cap.release()
        self.camera_label.config(image='')  # Clear camera view

    def copy_result(self):
        result = self.result_text.get()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            messagebox.showinfo("Copied", "QR Code result copied to clipboard!")

    def update_camera(self):
        if self.scanning and self.cap.isOpened():
            ret, frame = self.cap.read()

            if not ret:
                messagebox.showerror("Error", "Failed to read camera frame!")
                self.stop_scanning()
                return

            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            decoded_objects = pyzbar.decode(gray)

            for obj in decoded_objects:
                points = obj.polygon
                if len(points) > 4:
                    hull = cv2.convexHull(np.array([p for p in points], dtype=np.int32))
                    cv2.polylines(frame, [hull], True, (0, 255, 0), 2)
                else:
                    pts = np.array([[p.x, p.y] for p in points], np.int32)
                    pts = pts.reshape((-1, 1, 2))
                    cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

                if obj.data:
                    self.result_text.set(obj.data.decode("utf-8"))
                    self.stop_scanning()
                    break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)

            self.camera_label.imgtk = imgtk
            self.camera_label.configure(image=imgtk)

            self.root.after(10, self.update_camera)

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeScanner(root)
    root.mainloop()
