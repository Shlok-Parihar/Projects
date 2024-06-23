from tkinter import *
import tkinter.filedialog
import tkinter.messagebox as tmsg
from PIL import Image
from PIL import ImageTk
import cv2
from predictions import detection
from predictions import draw_bounding_boxes
import time
import os

# Define the threshold for categorizing potholes
THRESHOLD_AREA = 0.001 # Example threshold area, you can adjust this


def print_path():
    global f
    f = tkinter.filedialog.askopenfilename(
        parent=root,
        initialdir='',
        title='Select file',
        filetypes=[('JPG Image', '.jpg'), ('MP4 Video', '.mp4')]
    )
    img1 = cv2.imread(f)
    newimg = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    newimg = cv2.resize(newimg, (512, 512))
    img = Image.fromarray(newimg)
    imgtk = ImageTk.PhotoImage(image=img)
    x.imgtk = imgtk
    x.configure(image=imgtk)

def categorize_potholes(co_ords):
    major_count = 0
    minor_count = 0
    for co_ord in co_ords:
        if len(co_ord) == 3:  # Assuming the coordinates format is (x, y, area)
            _, _, area = co_ord
            if area >= THRESHOLD_AREA:
                major_count += 1
            else:
                minor_count += 1
        else:
            print("Unexpected coordinate format:", co_ord)
    return major_count, minor_count

def detect_objects():
    if f.endswith('.jpg'):
        img = cv2.imread(f)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        co_ords = detection(img)
        pothole_count = len(co_ords) if co_ords else 0
        major_count, minor_count = categorize_potholes(co_ords)
        count_label.config(text=f"Detected Potholes: {pothole_count}")
        major_minor_label.config(text=f"Major: {major_count}, Minor: {minor_count}")
        img_new = img.copy()
        detected_img = draw_bounding_boxes(co_ords, img_new)
        detected_img = cv2.resize(detected_img, (512, 512))
        img = Image.fromarray(detected_img)
        imgtk = ImageTk.PhotoImage(image=img)
        x.imgtk = imgtk
        x.configure(image=imgtk)

    if f.endswith('.mp4'):
        cap = cv2.VideoCapture(f)
        total_potholes = 0
        total_major = 0
        total_minor = 0

        while True:
            current_time = time.localtime()
            formatted_time = time.strftime("%Y-%m-%d %H-%M-%S", current_time)
            ret, frame = cap.read()
            if not ret:
                break
            co_ords = detection(frame)
            total_potholes += len(co_ords) if co_ords else 0
            major_count, minor_count = categorize_potholes(co_ords)
            total_major += major_count
            total_minor += minor_count
            img_new = frame.copy()
            detected_img = draw_bounding_boxes(co_ords, img_new)
            detected_img = cv2.resize(detected_img, (512, 512))
            if co_ords:
                if not os.path.exists('screenshots'):
                    os.makedirs('screenshots')
                cv2.imwrite(f'screenshots/{formatted_time}.jpg', detected_img)
            img = Image.fromarray(cv2.cvtColor(detected_img, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)
            x.imgtk = imgtk
            x.configure(image=imgtk)
            x.update()

        count_label.config(text=f"Total Detected Potholes: {total_potholes}")
        major_minor_label.config(text=f"Major: {total_major}, Minor: {total_minor}")

def login_page():
    global main_window
    login_window = Tk()
    login_window.geometry("800x600")
    login_window.title("Pothole Detection/Login")

    username_label = Label(login_window, text="Username:")
    username_label.pack(pady=5)
    username_entry = Entry(login_window)
    username_entry.pack(pady=5)

    password_label = Label(login_window, text="Password:")
    password_label.pack(pady=5)
    password_entry = Entry(login_window, show="*")
    password_entry.pack(pady=5)

    def validate_login():
        if username_entry.get() == "admin" and password_entry.get() == "admin":
            login_window.destroy()
            root.deiconify()
        else:
            tmsg.showerror("Login Failed", "Invalid username or password")

    login_button = Button(login_window, text="Login", command=validate_login)
    login_button.pack(pady=10)

    login_window.mainloop()

def live_detection():
    cap = cv2.VideoCapture(0)
    total_potholes = 0
    total_major = 0
    total_minor = 0

    while True:
        current_time = time.localtime()
        formatted_time = time.strftime("%Y-%m-%d %H-%M-%S", current_time)
        ret, frame = cap.read()
        if not ret:
            break
        co_ords = detection(frame)
        total_potholes += len(co_ords) if co_ords else 0
        major_count, minor_count = categorize_potholes(co_ords)
        total_major += major_count
        total_minor += minor_count
        img_new = frame.copy()
        detected_img = draw_bounding_boxes(co_ords, img_new)
        detected_img = cv2.resize(detected_img, (512, 512))
        if co_ords:
            if not os.path.exists('screenshots'):
                os.makedirs('screenshots')
            cv2.imwrite(f'screenshots/{formatted_time}.jpg', detected_img)
        img = Image.fromarray(cv2.cvtColor(detected_img, cv2.COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(image=img)
        x.imgtk = imgtk
        x.configure(image=imgtk)
        x.update()

    count_label.config(text=f"Total Detected Potholes: {total_potholes}")
    major_minor_label.config(text=f"Major: {total_major}, Minor: {total_minor}")

root = Tk()
root.geometry("800x800")
root.title("Pothole Detection")
root.resizable(0, 0)
im = None

MF = Frame(root, bd=8, bg="lightgray", relief=GROOVE)
MF.place(x=0, y=0, height=50, width=800)

menu_label = Label(MF, text="Pothole Detection", font=("times new roman", 20, "bold"), bg="lightgray", fg="black", pady=0)
menu_label.pack(side=TOP, fill="x")

x = Label(root, image=im)
x.grid(row=1, column=0, padx=5, pady=50)

# Create a frame for buttons
button_frame = Frame(root)
button_frame.grid(row=2, column=0, columnspan=2, pady=10)

# "Select Image" button
b1 = Button(button_frame, font=("times new roman", 20, "bold"), text='Select Image/Video', command=print_path)
b1.grid(row=0, column=0, padx=10)

# "Detect" button
b2 = Button(button_frame, font=("times new roman", 20, "bold"), text='Detect', command=detect_objects)
b2.grid(row=0, column=1, padx=10)

# Live button
b3 = Button(button_frame, font=("times new roman", 20, "bold"), text='Live', command=live_detection)
b3.grid(row=0, column=2, padx=10)

# Label to show count of detected potholes
count_label = Label(root, font=("times new roman", 20, "bold"), text="Detected Potholes: 0")
count_label.grid(row=3, column=0, pady=10)

# Label to show count of major and minor potholes
major_minor_label = Label(root, font=("times new roman", 20, "bold"), text="Major: 0, Minor: 0")
major_minor_label.grid(row=4, column=0, pady=10)

# Hide the main window initially
root.withdraw()

# Show the login page
login_page()

root.mainloop()