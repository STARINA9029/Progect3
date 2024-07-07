from tkinter import Tk, filedialog, Toplevel, simpledialog, messagebox
import numpy as np
from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
import cv2

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
    if file_path:
        image = Image.open(file_path)
        show_image(image)

def capture_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    ret, frame = cap.read()
    cap.release()
    if ret:
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        show_image(image)
    else:
        print("Error: Could not capture image.")

def show_image(image):
    global current_image, panel_original
    current_image = image.copy()
    imgtk = ImageTk.PhotoImage(image=image)
    if panel_original is None:
        panel_original = tk.Label(image=imgtk)
        panel_original.image = imgtk
        panel_original.pack(side="left", padx=10, pady=10)
    else:
        panel_original.configure(image=imgtk)
        panel_original.image = imgtk

def show_channel(color):
    if current_image is not None:
        r, g, b = current_image.split()

        if color == "red":
            image = Image.merge("RGB", [r, Image.new("L", r.size, 0), Image.new("L", r.size, 0)])
        elif color == "green":
            image = Image.merge("RGB", [Image.new("L", g.size, 0), g, Image.new("L", g.size, 0)])
        elif color == "blue":
            image = Image.merge("RGB", [Image.new("L", b.size, 0), Image.new("L", b.size, 0), b])

        show_processed_image(image)

def show_processed_image(image):
    processed_window = Toplevel()
    processed_window.title("Processed Image")

    imgtk = ImageTk.PhotoImage(image=image)

    panel_processed = tk.Label(processed_window, image=imgtk)
    panel_processed.image = imgtk
    panel_processed.pack()

def resize_image():
    if current_image is not None:
        width = simpledialog.askinteger("Input", "Enter new width:")
        height = simpledialog.askinteger("Input", "Enter new height:")
        if width and height:
            resized_image = current_image.resize((width, height))
            show_processed_image(resized_image)

def rotate_image():
    if current_image is not None:
        angle = simpledialog.askfloat("Input", "Enter rotation angle:")
        if angle is not None:
            rotated_image = current_image.rotate(angle, expand=True)
            show_processed_image(rotated_image)

def draw_line(color):
    if current_image is not None:
        x1 = simpledialog.askinteger("Input", "Enter x-coordinate of starting point:")
        y1 = simpledialog.askinteger("Input", "Enter y-coordinate of starting point:")
        x2 = simpledialog.askinteger("Input", "Enter x-coordinate of ending point:")
        y2 = simpledialog.askinteger("Input", "Enter y-coordinate of ending point:")
        thickness = simpledialog.askinteger("Input", "Enter line thickness:")

        if None not in [x1, y1, x2, y2, thickness]:
            image = current_image.copy()
            draw = ImageDraw.Draw(image)
            draw.line([(x1, y1), (x2, y2)], fill=color, width=thickness)
            show_processed_image(image)

def draw_green_line():
    draw_line("green")

def save_current_image():
    if current_image is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
        if file_path:
            current_image.save(file_path)
            messagebox.showinfo("Image Saved", "The image has been successfully saved.")
    else:
        messagebox.showerror("Error", "No image to save.")

current_image = None
panel_original = None

root = Tk()
root.title("Image Processing App")

btn_select_image = tk.Button(root, text="Select Image", command=select_image)
btn_select_image.pack(side="top", padx=10, pady=10)

btn_capture_image = tk.Button(root, text="Capture Image from Webcam", command=capture_image)
btn_capture_image.pack(side="top", padx=10, pady=10)

btn_red_channel = tk.Button(root, text="Show Red Channel", command=lambda: show_channel("red"))
btn_red_channel.pack(side="top", padx=10, pady=10)

btn_green_channel = tk.Button(root, text="Show Green Channel", command=lambda: show_channel("green"))
btn_green_channel.pack(side="top", padx=10, pady=10)

btn_blue_channel = tk.Button(root, text="Show Blue Channel", command=lambda: show_channel("blue"))
btn_blue_channel.pack(side="top", padx=10, pady=10)

btn_resize_image = tk.Button(root, text="Resize Image", command=resize_image)
btn_resize_image.pack(side="top", padx=10, pady=10)

btn_rotate_image = tk.Button(root, text="Rotate Image", command=rotate_image)
btn_rotate_image.pack(side="top", padx=10, pady=10)

btn_draw_line = tk.Button(root, text="Draw Line", command=lambda: draw_line("black"))
btn_draw_line.pack(side="top", padx=10, pady=10)

btn_draw_green_line = tk.Button(root, text="Draw Green Line", command=draw_green_line)
btn_draw_green_line.pack(side="top", padx=10, pady=10)

btn_save_current_image = tk.Button(root, text="Save Current Image", command=save_current_image)
btn_save_current_image.pack(side="top", padx=10, pady=10)

root.mainloop()
