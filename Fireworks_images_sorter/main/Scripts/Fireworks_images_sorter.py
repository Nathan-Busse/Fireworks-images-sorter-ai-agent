import cv2
import os
import shutil

# Function to detect fireworks in an image
def detect_fireworks(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Convert the image to the HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #-----------------------------------------------------------------------------------#
    #           | Define a refined colour range for fireworks|                          #
    #           | ___________________________________________|                          #
    #                                                                                   #
    #              H   S    V            Key:                                           #
    #              |   |    |            ----                                           #
    #              |   |    |                                                           #
    #             \ / \ /  \ /                                                          #
    lower_color = (0, 90, 100)      #   H = Hue (0-179)                                #
    #              |   |    |                                                           #
    #              |   |    |            S = Saturation (0-255)                         #
    #             \ / \ /  \ /                                                          #
    upper_color = (15, 255, 255)     #   V = Value (0-255)                              #
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
    if contours:
        return True
    return False

# Main function
def main():
    current_script_path = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(current_script_path, '..')  # Moves up one level to the Fireworks_images_sorter folder

    # Define the path for the 'Images' directory
    images_directory_path = os.path.join(base_path, 'Images')

    # Create 'Images' directory if it doesn't exist
    if not os.path.exists(images_directory_path):
        os.makedirs(images_directory_path)
        # Create subfolders 'Source', 'Detected', 'Undetected'
        os.makedirs(os.path.join(images_directory_path, 'Source'))
        os.makedirs(os.path.join(images_directory_path, 'Detected'))
        os.makedirs(os.path.join(images_directory_path, 'Undetected'))
    else:
        # Check and create subfolders 'Source', 'Detected', 'Undetected' if they don't exist
        for subdir in ['Source', 'Detected', 'Undetected']:
            subdir_path = os.path.join(images_directory_path, subdir)
            if not os.path.exists(subdir_path):
                os.makedirs(subdir_path)

    # Define the paths for directories
    source_directory_path = os.path.join(images_directory_path, 'Source')
    detected_directory_path = os.path.join(images_directory_path, 'Detected')
    undetected_directory_path = os.path.join(images_directory_path, 'Undetected')

    # Iterate through files in the source directory
    for filename in os.listdir(source_directory_path):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):  # Adjust the image formats as needed
            image_path = os.path.join(source_directory_path, filename)

            # Check if fireworks are detected in the image
            if detect_fireworks(image_path):
                # Copy the image to the detected directory
                shutil.copy(image_path, os.path.join(detected_directory_path, filename))
                print(f"Fireworks detected in: {filename}. Image copied to detected directory.")
            else:
                # Copy the image to the undetected directory
                shutil.copy(image_path, os.path.join(undetected_directory_path, filename))
                print(f"No fireworks detected in: {filename}. Image copied to undetected directory.")

if __name__ == "__main__":
    main()
    