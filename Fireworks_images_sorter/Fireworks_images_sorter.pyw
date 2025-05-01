import cv2
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to detect fireworks in an image
def detect_fireworks(image_path):
    # Load the image
    img = cv2.imread(image_path)
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #-----------------------------------------------------------------------------------#
    #           | Define a refined colour range for fireworks|                          #
    #           | ___________________________________________|                          #
    #                                                                                   #
    #              H   S    V            Key:                                           #
    #              |   |    |            ----                                           #
    #              |   |    |                                                           #
    #             \ / \ /  \ /                                                          #
    lower_color = (0, 90, 100)      #   H = Hue (0-179)
    #              |   |    |                                                           #
    #              |   |    |            S = Saturation (0-255)
    #             \ / \ /  \ /                                                          #
    upper_color = (15, 255, 255)     #   V = Value (0-255)
    #-----------------------------------------------------------------------------------#
    # Create a mask to extract the color range
    mask = cv2.inRange(hsv, lower_color, upper_color)
    # Apply morphological operations to reduce noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Check if fireworks are detected
    return bool(contours)

# Function to process images from the 'Source' folder
def process_images():
    # Ask the user to select a base folder (typically your Images folder)
    base_path = filedialog.askdirectory(title="Select Base Folder (Images folder)")
    if not base_path:
        return

    # Define subfolder paths
    source_directory_path = os.path.join(base_path, 'Source')
    detected_directory_path = os.path.join(base_path, 'Detected')
    undetected_directory_path = os.path.join(base_path, 'Undetected')

    # Check whether the 'Source' folder exists
    if not os.path.exists(source_directory_path):
        create_now = messagebox.askyesno(
            "Folder Structure Not Found", 
            "The selected folder doesn't have a 'Source' subfolder.\n"
            "Would you like to create the folder structure (Source, Detected, Undetected)?"
        )
        if create_now:
            os.makedirs(source_directory_path, exist_ok=True)
            os.makedirs(detected_directory_path, exist_ok=True)
            os.makedirs(undetected_directory_path, exist_ok=True)
            messagebox.showinfo(
                "Structure Created",
                "Folders created successfully.\n"
                "Please add your source images into the 'Source' folder and run the process again."
            )
        return
    else:
        # Ensure that 'Detected' and 'Undetected' folders exist
        os.makedirs(detected_directory_path, exist_ok=True)
        os.makedirs(undetected_directory_path, exist_ok=True)

    # Process each image within the 'Source' folder
    log_lines = []
    for filename in os.listdir(source_directory_path):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(source_directory_path, filename)
            if detect_fireworks(image_path):
                shutil.copy(image_path, os.path.join(detected_directory_path, filename))
                log_lines.append(f"Fireworks detected in: {filename}. Copied to 'Detected'.")
            else:
                shutil.copy(image_path, os.path.join(undetected_directory_path, filename))
                log_lines.append(f"No fireworks detected in: {filename}. Copied to 'Undetected'.")

    if not log_lines:
        messagebox.showinfo("No Images", "No images found in the 'Source' folder.")
    else:
        # Clear and update the text log in the GUI
        log_text.delete("1.0", tk.END)
        for line in log_lines:
            log_text.insert(tk.END, line + "\n")
        messagebox.showinfo("Process Complete", "Image sorting process completed.")

# Setting up the GUI window
root = tk.Tk()
root.title("Fireworks Image Sorter")
root.geometry("600x400")

# Title label
title_label = tk.Label(root, text="Fireworks Image Sorter", font=("Arial", 16))
title_label.pack(pady=10)

# Instruction label
instruction_label = tk.Label(
    root,
    text="Select a folder containing the image structure (Source, Detected, Undetected)."
)
instruction_label.pack(pady=5)

# Button to trigger the folder selection and processing
process_button = tk.Button(
    root,
    text="Select Folder and Process Images",
    command=process_images,
    font=("Arial", 12)
)
process_button.pack(pady=10)

# Text widget to display log messages from the processing run
log_text = tk.Text(root, height=10, width=70)
log_text.pack(pady=10)

root.mainloop()
