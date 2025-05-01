---
# Fireworks Images Sorter

The **Fireworks Images Sorter** is a Python-based utility designed to help you efficiently organize your fireworks images. Using a dedicated sorting algorithm and a user-friendly graphical interface, this tool allows users to automatically categorize images into designated folders. Whether you're a photography enthusiast or handling a large database of images, this project streamlines the process of managing your media.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Command-Line Usage](#command-line-usage)
  - [Graphical User Interface (GUI)](#graphical-user-interface-gui)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Overview

The Fireworks Images Sorter is built to automate the categorization of your fireworks photos. It decouples the core sorting logic from the user interface, making it both a robust backend tool and an engaging application for end users. In this version, a simple yet effective GUI is implemented using Tkinter, allowing users to select source and target directories, preview images, and execute the sorting process with a click of a button.

Below is a detailed breakdown of the provided code in Markdown format:

---

# Code Breakdown

This Python script is designed to detect fireworks in images, sort them into corresponding folders based on detection results, and provide a simple GUI to run the process. The code makes use of the OpenCV library for image processing and Tkinter for the graphical user interface.

---

## 1. Importing Libraries

```python
import cv2
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
```

- **cv2**: This is the OpenCV library used for image processing (reading images, color conversions, applying filters, etc.).
- **os**: Provides functions for interacting with the operating system, such as file and directory operations.
- **shutil**: Used for copying files between directories.
- **tkinter**: The standard Python library for GUI development.
- **filedialog & messagebox**: Tkinter modules for file and directory selection dialogs, and for showing pop-up messages.

---

## 2. Fireworks Detection Function

### Function Definition

```python
def detect_fireworks(image_path):
```

This function takes in an `image_path` and returns a boolean indicating whether fireworks are detected in the image.

### Detailed Steps Inside `detect_fireworks`

1. **Load the Image:**

   ```python
   img = cv2.imread(image_path)
   ```

   - Reads the image from the filesystem using OpenCV. The image is loaded into a variable called `img`.

2. **Convert the Image to HSV Color Space:**

   ```python
   hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
   ```

   - OpenCV reads images in BGR format by default. Converting the image to HSV (Hue, Saturation, Value) simplifies the process of filtering out specific colors.

3. **Define the Color Range for Fireworks:**

   The following code block demonstrates the intended adjustment of the HSV range:

   ```python
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
   ```

   - `lower_color` and `upper_color` specify the lower and upper bounds for the HSV values. These ranges help isolate the color (or range of colors) typical for fireworks.

4. **Create a Mask to Extract the Specified Color Range:**

   ```python
   mask = cv2.inRange(hsv, lower_color, upper_color)
   ```

   - This creates a binary mask where pixels within the specified HSV range are white (255) and those outside are black (0).

5. **Reduce Noise with Morphological Operations:**

   ```python
   kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
   mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
   mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
   ```

   - **`cv2.getStructuringElement`**: Defines an elliptical kernel (a 5x5 matrix) that will be used for morphological operations.
   - **`cv2.morphologyEx`**: Applies an opening operation (erosion followed by dilation) to remove small noise, and a closing operation (dilation followed by erosion) to close small holes in the detected regions.

6. **Find Contours in the Mask:**

   ```python
   contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   ```

   - **`cv2.findContours`** locates the boundaries (contours) in the binary mask. The method `cv2.RETR_EXTERNAL` retrieves only the external contours, and `cv2.CHAIN_APPROX_SIMPLE` compresses horizontal, vertical, and diagonal segments.

7. **Return Detection Result:**

   ```python
   return bool(contours)
   ```

   - Converts the list of detected contours to a boolean value (`True` if any contour exists, indicating that fireworks are detected; otherwise `False`).

---

## 3. Processing Images Function

### Function Definition

```python
def process_images():
```

This function handles folder selection and the processing of images by detecting fireworks and copying them into respective subfolders.

### Detailed Steps Inside `process_images`

1. **Select the Base Folder:**

   ```python
   base_path = filedialog.askdirectory(title="Select Base Folder (Images folder)")
   if not base_path:
       return
   ```

   - **`filedialog.askdirectory`**: Opens a directory selection dialog. If the user cancels, the function exits early.

2. **Define Folder Paths:**

   ```python
   source_directory_path = os.path.join(base_path, 'Source')
   detected_directory_path = os.path.join(base_path, 'Detected')
   undetected_directory_path = os.path.join(base_path, 'Undetected')
   ```

   - Constructs file paths for the `Source`, `Detected`, and `Undetected` folders based on the base folder.

3. **Check and Create Folder Structure if Needed:**

   ```python
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
   ```

   - Checks if the `Source` folder exists. If not, it prompts the user to create the folder structure.
   - Uses `os.makedirs` to create the folders. The `exist_ok=True` parameter avoids errors if the folder already exists.
   - If the folder structure is missing, the process ends after creating the folders.

4. **Process Each Image in the Source Folder:**

   ```python
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
   ```

   - **Iterate Over Files:** Loops through files in the `Source` folder and filters based on image file extensions.
   - **Detection:** For each image, it calls `detect_fireworks` to check for fireworks.
   - **Copying Files:** 
     - If fireworks are detected, copies the image into the `Detected` folder.
     - Otherwise, copies the image into the `Undetected` folder.
   - **Logging:** Adds a log entry for each processed image to record the action taken.

5. **Display Process Completion or No Images Found:**

   ```python
   if not log_lines:
       messagebox.showinfo("No Images", "No images found in the 'Source' folder.")
   else:
       # Clear and update the text log in the GUI
       log_text.delete("1.0", tk.END)
       for line in log_lines:
           log_text.insert(tk.END, line + "\n")
       messagebox.showinfo("Process Complete", "Image sorting process completed.")
   ```

   - If no images were processed, a message is shown informing the user.
   - Otherwise, the GUI log (a Tkinter `Text` widget) is updated with the processing details.

---

## 4. GUI Setup

### Initialize the Main Window

```python
root = tk.Tk()
root.title("Fireworks Image Sorter")
root.geometry("600x400")
```

- **`tk.Tk()`**: Initializes the root window.
- **`title()`**: Sets the window title.
- **`geometry()`**: Specifies the window size (600x400 pixels).

### Adding Widgets to the GUI

1. **Title Label:**

   ```python
   title_label = tk.Label(root, text="Fireworks Image Sorter", font=("Arial", 16))
   title_label.pack(pady=10)
   ```

   - A `Label` widget is created and packed into the window with vertical padding.

2. **Instruction Label:**

   ```python
   instruction_label = tk.Label(
       root,
       text="Select a folder containing the image structure (Source, Detected, Undetected)."
   )
   instruction_label.pack(pady=5)
   ```

   - Provides instructions to the user regarding folder selection.

3. **Process Button:**

   ```python
   process_button = tk.Button(
       root,
       text="Select Folder and Process Images",
       command=process_images,
       font=("Arial", 12)
   )
   process_button.pack(pady=10)
   ```

   - A button is provided to trigger the `process_images` function when clicked.
   - The button is styled and placed with some padding.

4. **Log Text Widget:**

   ```python
   log_text = tk.Text(root, height=10, width=70)
   log_text.pack(pady=10)
   ```

   - A `Text` widget is added to display log messages. This logs the steps and outcomes of the image processing.

### Start the GUI Event Loop

```python
root.mainloop()
```

- **`mainloop()`**: Starts the Tkinter event loop that waits continuously for user actions (like clicking the button).

---

## Conclusion

The script integrates image processing with a straightforward GUI to:

- Detect fireworks in images using HSV color filtering and morphological operations.
- Organize images into separate folders (`Detected` and `Undetected`).
- Provide an interface to choose the folder structure, execute the image sorting process, and view a log of the operation.

This modular design allows you to expand the functionality further (e.g., better image previews or additional processing features) while keeping the core logic separate from the user interface.

---

## Features

- **Automatic Sorting:** Organizes images based on defined characteristics.
- **Graphical User Interface:** User-friendly GUI built with Tkinter for effortless navigation.
- **Image Preview:** Displays file names of images found in the source directory.
- **Customizable Logic:** Easily extend or modify the sorting algorithm to suit specific needs.
- **Cross-Platform:** Developed in Python and compatible with major operating systems.

## Installation

### Prerequisites

- **Python 3.6+**: Make sure you have Python installed.
- **Tkinter:** Usually included with Python. If missing, please install it for your specific platform.
- (Optional) **Pillow:** For future enhancements with image preview capabilities.
- **Other Dependencies:** Listed in `requirements.txt` (if applicable).

### Cloning the Repository

Open your terminal and run:

```bash
git clone https://github.com/Nathan-Busse/Fireworks-images-sorter-ai-agent.git
cd Fireworks-images-sorter
```

### Installing Dependencies

If you've provided a `requirements.txt`, install the dependencies by running:

```bash
pip install -r requirements.txt
```

If you are using a virtual environment, be sure to activate it before installing.

## Usage

### Command-Line Usage

For users who prefer the terminal, you can execute the sorting function directly. For example:

```bash
python sorter.py --source /path/to/input/images --output /path/to/sorted/images
```

*Note:* Adjust the script and parameters as needed to align with your sorting logic.

### Graphical User Interface (GUI)

To launch the GUI version of the Fireworks Images Sorter:

1. **Run the GUI Script**

   ```bash
   python gui.py
   ```

2. **Select Folders**

   - **Source Folder:** Click the "Select Image Folder" button to pick the folder containing your fireworks images. The application will display the found images in a list box.
   - **Output Folder:** Click the "Select Output Folder" button to choose where the sorted images should be placed.

3. **Sort the Images**

   After both directories have been set, click the "Sort Images" button. The application will call the core sorting function (`sort_images()`), process the images, and then move or copy them to the output folder according to your criteria.

4. **Feedback**

   Upon completion, a confirmation message will appear. Any errors or issues will be displayed via dialog boxes for ease of troubleshooting.

## Configuration

- **Sorting Logic:** Modify the `sort_images()` function in the core module (e.g., `sorter.py`) to refine how images are categorized.
- **GUI Customizations:** The user interface is built in `gui.py`. Here, you can add widgets such as progress bars, image previews (with Pillow), or more advanced file selection dialogs.
- **Logging:** For deeper insight into operations, consider implementing logging to track the sorting process and errors.

## Troubleshooting

- **Tkinter Errors:** If you encounter issues running the GUI, ensure that Tkinter is correctly installed and configured with your Python distribution.
- **Permission Issues:** Verify read/write permissions for the selected directories.
- **Missing Dependencies:** Revisit the `requirements.txt` or error messages for guidance on installing any missing packages.
- **Script Failures:** Use Python’s interactive mode to debug errors within `sort_images()` and other functions.

## Contributing

Contributions are warmly welcomed! Here’s how you can help improve the project:

1. **Fork the Repository:** Create your own fork on GitHub.
2. **Create a Branch:** Develop your feature or bug fix in a separate branch.
3. **Submit a Pull Request:** Provide a detailed explanation of your improvements.
4. **Follow Coding Standards:** Adhere to the established style and add comments where necessary.

For any major changes, please open an issue first to discuss your ideas.

## License

This project is licensed under the MIT License. Please see the [LICENSE](LICENSE) file for full details.

## Acknowledgements

- Special thanks to the open-source community for their contributions and inspiration.
- A nod to the Tkinter and Python documentation for providing such robust tools for development.
- Gratitude to all contributors who engage in making this project better!

---

Thank you for using the Fireworks Images Sorter. We hope this tool helps you manage and enjoy your collections of fireworks images more efficiently. For further enhancements and ideas, feel free to file issues or join our contributor community on GitHub.

---

### Further Enhancements

- **Advanced Image Previews:** Consider integrating the Pillow library to generate thumbnails in the GUI.
- **Dynamic Filtering:** Add options to sort images based on additional criteria such as brightness, color, or captured metadata.
- **Progress Indicators:** Implement progress bars during long sorting operations using `ttk.Progressbar`.
- **Cross-Platform Packaging:** Look into packaging solutions (like PyInstaller) to distribute the GUI as a standalone application.

Though this is a final for submition, it will be worked on once the winners are announced...



