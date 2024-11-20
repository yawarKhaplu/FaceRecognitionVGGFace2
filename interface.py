import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from collect_face_data import *
import os
from genrate_embendings import *
from recognize_face import *

color_options = ["Red", "Green", "Blue", "Yellow", "Purple", "Orange", "Pink", "Black", "White", "Gray"]
color_rgb_values = [
    (255, 0, 0),      # Red
    (0, 255, 0),      # Green
    (0, 0, 255),      # Blue
    (255, 255, 0),    # Yellow
    (128, 0, 128),    # Purple
    (255, 165, 0),    # Orange
    (255, 192, 203),  # Pink
    (0, 0, 0),        # Black
    (255, 255, 255),  # White
    (128, 128, 128)   # Gray
]

name_entry = None



def collect_faces(root, folder_name):
    print("Opning Camera ...")
    result = collect_face_from_cam(folder_name)
    # root.after(1, root.quit)  # Exits the main loop after 10 seconds
    if result:
        def on_button_click(response):
            if response == "yes":
                messagebox.showinfo("Embeddings", "Generating embeddings for the collected data...")
                root.destroy()
                genrate_embendings()

            elif response == "no":
                messagebox.showinfo("Embeddings", "Embeddings generation skipped.")
                root.destroy()
        # Create the main window
        root = tk.Tk()
        root.title("Face Data Collection")
        root.geometry("500x300")  # Window size
        root.resizable(False, False)

        # Canvas for the gradient effect (placed as background)
        canvas = tk.Canvas(root, width=500, height=300)
        canvas.place(x=0, y=0)

        # Create a gradient effect using lines
        for i in range(300):
            color = "#%02x%02x%02x" % (int(44 + (i * 0.1)), int(62 + (i * 0.1)), int(80 + (i * 0.1)))
            canvas.create_line(0, i, 500, i, fill=color)

        # Frame to hold the content (this will be above the canvas)
        frame = tk.Frame(root, bg='#2C3E50', bd=10)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Message Display
        message = tk.Label(frame, text="Data Collected Successfully!", font=("Helvetica", 18, "bold"),
                        fg="#ECF0F1", bg="#2C3E50")
        message.pack(pady=(0, 10))

        sub_message = tk.Label(frame, text="Would you like to generate embeddings for this data?", font=("Helvetica", 12),
                            fg="#ECF0F1", bg="#2C3E50")
        sub_message.pack(pady=(0, 20))

        # Buttons with hover effect (custom style)
        def on_enter(event):
            event.widget.config(bg="#16A085", fg="white")

        def on_leave(event):
            event.widget.config(bg="#1ABC9C", fg="white")

        # Yes Button
        yes_button = tk.Button(frame, text="Yes", font=("Helvetica", 14, "bold"), bg="#1ABC9C", fg="white", 
                            relief="flat", width=12, height=2, command=lambda: on_button_click("yes"))
        yes_button.pack(side="left", padx=20)
        yes_button.bind("<Enter>", on_enter)
        yes_button.bind("<Leave>", on_leave)

        # No Button
        no_button = tk.Button(frame, text="No", font=("Helvetica", 14, "bold"), bg="#E74C3C", fg="white", 
                            relief="flat", width=12, height=2, command=lambda: on_button_click("no"))
        no_button.pack(side="right", padx=20)
        no_button.bind("<Enter>", on_enter)
        no_button.bind("<Leave>", on_leave)

        # Start the main loop
        # root.mainloop()




# function to train face
def train_user(name_entry, root, color_b):
    global color_options;global color_rgb_values
    selected_color = color_b.get()
    selected_rgb = (0,255, 0)
    name = name_entry.get()
    name = name.capitalize()
    
    print("Selected Color: ", selected_color)

    
    try:
        # make folder of 
        os.makedirs("Images", exist_ok=True)

        names = os.listdir("Images")
        if name == "":
            messagebox.showerror("Requst", "Please Enter Your name")
            root.attributes("-topmost", True)

        elif name in names:
            messagebox.showerror("Oh", "Face Already Trained..")
            root.destroy()
            messagebox
        else:
            new_name = name + "_" +selected_color.replace(" ",'')
            folder_name = f"Images/{new_name}"
            os.makedirs(folder_name)
            collect_faces(root, folder_name)
            root.destroy()
    except Exception as e:
        pass
    
# Function to handle button click events
def train_new_face():
    global color_options
    entered_text = entry.get()

    train_data = tk.Tk()
    train_data.config(bg="#f0f0f0")
    title_label = tk.Label(train_data, text="Your Details", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#333")
    title_label.pack(pady=20)
    name_label = tk.Label(train_data, text="Your name!", font=("Arial", 14), bg="#f0f0f0", fg="#333")
    name_label.pack(pady=10)

    name_entry = tk.Entry(train_data, font=("Arial", 14), bd=2, relief="solid", width=25)
    name_entry.insert(0,entered_text)
    name_entry.pack(pady=10)

    # Favorite color label
    color_label = tk.Label(train_data, text="What's your favorite color?", font=("Arial", 14), bg="#f0f0f0", fg="#333")
    color_label.pack(pady=10)

    # Combobox for color selection
    color_combobox = ttk.Combobox(train_data, values=color_options, font=("Arial", 14), width=17, state="readonly")
    color_combobox.set("Select Color")  # Set a default value
    color_combobox.pack(pady=10)

    
    # print(color_combobox.get())
        

    # submit button
    submit_button = tk.Button(train_data, text="Submit", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", command = lambda:train_user(name_entry, train_data, color_combobox))
    submit_button.pack(pady=20)

    train_data.mainloop()

def recognize_face():
    entry.delete(0, tk.END)  # Clear the entry field
    # messagebox.showinfo("Button 1", f"We Are Working On this feature be Patient")
    print("Please Wait Opening Camera...")
    live_recongnize()




# ******************************************Main Program First Window**********************************************#
# Create the main window

root = tk.Tk()
root.title("Face Recognition")
root.geometry("600x300")
root.config(bg="#f0f0f0")  # Set a light gray background color

# Create a frame for better layout control
frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20)
frame.pack(padx=10, pady=10, fill="both", expand=True)

# Add a Label to the frame
label = tk.Label(frame, text="What is your Good Name?", font=("Helvetica", 14), bg="#ffffff")
label.pack(pady=10)

# Add an Entry widget for text input
entry = tk.Entry(frame, font=("Helvetica", 12), bd=2, relief="solid", width=25)
entry.pack(pady=10)

# Create a Frame for buttons to align them horizontally
button_frame = tk.Frame(frame, bg="#ffffff")
button_frame.pack(pady=20)

# Button 1 (Action)
button1 = tk.Button(button_frame, text="Add Face", font=("Helvetica", 12), fg="white", bg="#4CAF50", 
                    relief="raised", width=18, height=2, command=train_new_face)
button1.grid(row=0, column=0, padx=10)

# Button 2 (Clear)
button2 = tk.Button(button_frame, text="Start Recognition", font=("Helvetica", 12), fg="white", bg="#f44336", 
                    relief="raised", width=18, height=2, command=recognize_face)
button2.grid(row=0, column=1, padx=10)

# Run the Tkinter event loop
root.mainloop()
