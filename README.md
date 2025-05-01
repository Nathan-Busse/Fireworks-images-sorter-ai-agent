This Python script designed for detecting fireworks in images and sorting them into different directories based on whether fireworks are detected or not. Let's go through the code step by step:

1. **Importing Libraries:**
   ```python
   import cv2
   import os
   import shutil
   ```
   - `cv2`: OpenCV library for computer vision tasks.
   - `os`: Provides a way of using operating system-dependent functionality.
   - `shutil`: High-level file operations.

2. **`detect_fireworks` Function:**
   ```python
   def detect_fireworks(image_path):
   ```
   - This function takes the path to an image as input.

   ```python
       img = cv2.imread(image_path)
   ```
   - Reads the image using OpenCV.

   ```python
       hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
   ```
   - Converts the image to the HSV (Hue, Saturation, Value) color space.

   ```python
       lower_color = (0, 100, 100)
       upper_color = (20, 255, 255)
   ```
   - Defines a color range in HSV for detecting fireworks.

   ```python
       mask = cv2.inRange(hsv, lower_color, upper_color)
   ```
   - Creates a mask to extract the specified color range.

   ```python
       kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
       mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
       mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
   ```
   - Applies morphological operations (opening and closing) to reduce noise in the mask.

   ```python
       contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   ```
   - Finds contours in the mask using the specified retrieval mode and approximation method.

   ```python
       if contours:
           return True
       return False
   ```
   - If contours are found, it indicates the presence of fireworks, so the function returns `True`. Otherwise, it returns `False`.

3. **`main` Function:**
   ```python
   def main():
   ```
   - The main function that orchestrates the entire image processing workflow.

   ```python
       current_script_path = os.path.dirname(os.path.abspath(__file__))
       base_path = os.path.join(current_script_path, '..')
   ```
   - Obtains the current script's directory and moves one level up to the parent directory.

   ```python
       images_directory_path = os.path.join(base_path, 'Images')
   ```
   - Defines the path for the 'Images' directory.

   ```python
       # ... (directory creation logic)
   ```
   - Checks and creates the 'Images' directory along with subdirectories 'Source', 'Detected', and 'Undetected' if they don't exist.

   ```python
       source_directory_path = os.path.join(images_directory_path, 'Source')
       detected_directory_path = os.path.join(images_directory_path, 'Detected')
       undetected_directory_path = os.path.join(images_directory_path, 'Undetected')
   ```
   - Defines paths for source, detected, and undetected image directories.

   ```python
       for filename in os.listdir(source_directory_path):
           if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
               image_path = os.path.join(source_directory_path, filename)
   ```
   - Iterates through files in the source directory, considering only image files (with specified extensions).

   ```python
               if detect_fireworks(image_path):
                   shutil.copy(image_path, os.path.join(detected_directory_path, filename))
                   print(f"Fireworks detected in: {filename}. Image copied to detected directory.")
               else:
                   shutil.copy(image_path, os.path.join(undetected_directory_path, filename))
                   print(f"No fireworks detected in: {filename}. Image copied to undetected directory.")
   ```
   - Calls `detect_fireworks` function for each image and copies the image to either the 'Detected' or 'Undetected' directory based on the result.

   ```python
   if __name__ == "__main__":
       main()
   ```
   - Executes the `main` function if the script is run as the main program.