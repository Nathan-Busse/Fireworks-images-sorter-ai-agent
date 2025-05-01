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
git clone https://github.com/Nathan-Busse/Fireworks-images-sorter.git
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
