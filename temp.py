import cv2
from tkinter import Tk, filedialog, Toplevel, simpledialog, messagebox
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
    if file_path:
        image = cv2.imread(file_path)
        show_image(image)

def capture_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    ret, frame = cap.read()
    cap.release()
    if ret:
        show_image(frame)
    else:
        print("Error: Could not capture image.")

def show_image(image):
    global current_image, panel_original
    current_image = image.copy()
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(image_rgb)
    imgtk = ImageTk.PhotoImage(image=img)
    if panel_original is None:
        panel_original = tk.Label(image=imgtk)
        panel_original.image = imgtk
        panel_original.pack(side="left", padx=10, pady=10)
    else:
        panel_original.configure(image=imgtk)
        panel_original.image = imgtk

def show_channel(channel):
    if current_image is not None:
        b, g, r = cv2.split(current_image)
        if channel == "red":
            image = np.zeros_like(current_image)
            image[:, :, 2] = r
        elif channel == "green":
            image = np.zeros_like(current_image)
            image[:, :, 1] = g
        elif channel == "blue":
            image = np.zeros_like(current_image)
            image[:, :, 0] = b
        show_processed_image(image)

def show_processed_image(image):
    processed_window = Toplevel()
    processed_window.title("Обработанное изображение")
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(image_rgb)
    imgtk = ImageTk.PhotoImage(image=img)
    
    panel_processed = tk.Label(processed_window, image=imgtk)
    panel_processed.image = imgtk
    panel_processed.pack()

def resize_image():
    if current_image is not None:
        width = simpledialog.askinteger("Ввод", "Введите новую ширину:")
        height = simpledialog.askinteger("Ввод", "Введите новую высоту:")
        if width and height:
            resized_image = cv2.resize(current_image, (width, height))
            show_processed_image(resized_image)

def rotate_image():
    if current_image is not None:
        angle = simpledialog.askfloat("Ввод", "Введите угол поворота:")
        if angle is not None:
            (h, w) = current_image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            rotated_image = cv2.warpAffine(current_image, M, (w, h))
            show_processed_image(rotated_image)

def draw_line():
    if current_image is not None:
        input_window = Toplevel(root)
        input_window.title("Параметры линии")
        
        tk.Label(input_window, text="x1:").grid(row=0, column=0)
        x1_entry = tk.Entry(input_window)
        x1_entry.grid(row=0, column=1)

        tk.Label(input_window, text="y1:").grid(row=1, column=0)
        y1_entry = tk.Entry(input_window)
        y1_entry.grid(row=1, column=1)

        tk.Label(input_window, text="x2:").grid(row=2, column=0)
        x2_entry = tk.Entry(input_window)
        x2_entry.grid(row=2, column=1)

        tk.Label(input_window, text="y2:").grid(row=3, column=0)
        y2_entry = tk.Entry(input_window)
        y2_entry.grid(row=3, column=1)

        tk.Label(input_window, text="Толщина:").grid(row=4, column=0)
        thickness_entry = tk.Entry(input_window)
        thickness_entry.grid(row=4, column=1)
        
        def submit_line_params():
            try:
                x1 = int(x1_entry.get())
                y1 = int(y1_entry.get())
                x2 = int(x2_entry.get())
                y2 = int(y2_entry.get())
                thickness = int(thickness_entry.get())
                line_image = current_image.copy()
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), thickness)
                show_processed_image(line_image)
                input_window.destroy()
            except ValueError:
                messagebox.showerror("Некорректный ввод", "Введите корректные целые числа для координат и толщины.")
        
        submit_button = tk.Button(input_window, text="Применить", command=submit_line_params)
        submit_button.grid(row=5, columnspan=2)

current_image = None
panel_original = None

root = Tk()
root.title("Приложение для обработки изображений")

btn_select_image = tk.Button(root, text="Выбрать изображение", command=select_image)
btn_select_image.pack(side="top", padx=10, pady=10)

btn_capture_image = tk.Button(root, text="Сделать снимок с веб-камеры", command=capture_image)
btn_capture_image.pack(side="top", padx=10, pady=10)

btn_red_channel = tk.Button(root, text="Показать красный канал", command=lambda: show_channel("red"))
btn_red_channel.pack(side="top", padx=10, pady=10)

btn_green_channel = tk.Button(root, text="Показать зеленый канал", command=lambda: show_channel("green"))
btn_green_channel.pack(side="top", padx=10, pady=10)

btn_blue_channel = tk.Button(root, text="Показать синий канал", command=lambda: show_channel("blue"))
btn_blue_channel.pack(side="top", padx=10, pady=10)

btn_resize_image = tk.Button(root, text="Изменить размер", command=resize_image)
btn_resize_image.pack(side="top", padx=10, pady=10)

btn_rotate_image = tk.Button(root, text="Повернуть изображение", command=rotate_image)
btn_rotate_image.pack(side="top", padx=10, pady=10)

btn_draw_line = tk.Button(root, text="Нарисовать линию", command=draw_line)
btn_draw_line.pack(side="top", padx=10, pady=10)

root.mainloop()
