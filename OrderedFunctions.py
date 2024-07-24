#For image analysis
import cv2

#Easy handling for data
import pandas as pd

#For the analysis of h5-File
import h5py as h5py

class Image_stitching: 

    def __init__(self):

      
        self.name = "Image_Analysis"
        
        self.labels= []


    def _read_in_image(self, image_path):
        """
        Reads an image from the given path and returns it.
        The image is read differently based on its file extension.
        
        Parameters:
        - image_path (str): The path to the image file.
        
        Returns:
        - image: The image read from the file, or None if the format is unknown.
        """
        
        # Extract the file extension and convert it to lower case
        _, ext = os.path.splitext(image_path)
        ext = ext.lower()
        
        # Check if the file extension is 'png'
        if ext == ".png":
            # Read the image in grayscale mode
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        # Check if the file extension is 'tif'
        elif ext == ".tif":
            # Read the image without changing its original color format
            image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        
        # If the file extension is neither 'png' nor 'tif'
        else:
            # Print an error message indicating an unknown format
            print("Unknown format")
            image = None  # Set image to None to avoid returning an undefined variable
        
        # Return the read image
        return image
    
    def _read_in_h5(self, h5_path, time_index=49):
        """
        Reads images and labels from an HDF5 file and assigns the labels at a specific time index to an instance variable.
        
        Parameters:
        - h5_path (str): The path to the HDF5 file.
        - time_index (int): The index of the time step to extract the labels from (default is 49).
        
        Raises:
        - KeyError: If the expected keys are not found in the HDF5 file.
        - IndexError: If the time index is out of range.
        """
        
        # Open the HDF5 file for reading
        with h5py.File(h5_path, 'r') as f:
            # Check if 'images' and 'labels' datasets exist in the file
            if 'images' not in f or 'labels' not in f:
                raise KeyError("The HDF5 file does not contain 'images' or 'labels' datasets.")
            
            # Read the entire 'images' dataset
            images = f['images'][:]
            # Read the entire 'labels' dataset
            labels = f['labels'][:]
        
        # Check if the time_index is within the valid range
        if time_index >= len(labels):
            raise IndexError("The time index is out of range.")
        
        # Assign the labels at the specified time index to the instance variable 'labels'
        self.labels = labels[time_index]

    def _rescale_NanoSIMS_image(self, image, scaling_factor=0.6):
        """
        Rescales a NanoSIMS image by a given scaling factor.
        
        Parameters:
        - image (numpy.ndarray): The input image to be rescaled.
        - scaling_factor (float): The factor by which to rescale the image (default is 0.6).
        
        Returns:
        - resized (numpy.ndarray): The rescaled image.
        
        Raises:
        - ValueError: If the scaling factor is non-positive.
        """
        
        # Check if the scaling factor is valid
        if scaling_factor <= 0:
            raise ValueError("Scaling factor must be positive.")
        
        # Get the original dimensions of the image
        (y, x) = image.shape[:2]
        
        # Calculate the new dimensions based on the scaling factor
        y_resized, x_resized = int(y * scaling_factor), int(x * scaling_factor)
        
        # Resize the image using the specified interpolation method
        resized = cv2.resize(image, (x_resized, y_resized), interpolation=cv2.INTER_AREA)
        
        # Return the rescaled image
        return resized

    def rotate_image(self, image, angle, background_color=(0, 0, 0)):
        """
        Rotates an image by a given angle.
        
        Parameters:
        - image (numpy.ndarray): The input image to be rotated.
        - angle (float): The angle by which to rotate the image (in degrees).
        - background_color (tuple): The background color for uncovered areas (default is black).
        
        Returns:
        - rotated (numpy.ndarray): The rotated image.
        """

        """ 
            # Get the image's dimensions (height and width)
            (h, w) = image.shape[:2]
            
            # Compute the center of the image
            center = (w / 2, h / 2)
            
            # Generate the 2x3 rotation matrix
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            
            # Perform the rotation using the rotation matrix
            rotated = cv2.warpAffine(image, M, (w, h))
            
            # Return the rotated image
            return rotated
        """
        
        # Get the image's dimensions (height and width)
        (h, w) = image.shape[:2]
        
        # Compute the center of the image
        center = (w / 2, h / 2)
        
        # Generate the 2x3 rotation matrix
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        
        # Calculate the cosine and sine of the rotation angle
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])
        
        # Compute the new bounding dimensions of the image
        new_w = int((h * sin) + (w * cos))
        new_h = int((h * cos) + (w * sin))
        
        # Adjust the rotation matrix to take into account the translation
        M[0, 2] += (new_w / 2) - center[0]
        M[1, 2] += (new_h / 2) - center[1]
        
        # Perform the rotation using the rotation matrix and the new dimensions
        rotated = cv2.warpAffine(image, M, (new_w, new_h), borderValue=background_color)
        
        # Return the rotated image
        return rotated

    def _divide_image(self, image):
        """
        Divides an image into smaller overlapping images and returns them along with their relative positions.

        Parameters:
            image (ndarray): The input image to be divided.

        Returns:
            small_images (list of ndarray): A list of the smaller overlapping images.
            relative_positions (list of list): A list of relative positions of each smaller image in the format [[y_start, y_end], [x_start, x_end]].
        """

        # Get the image's dimensions
        h, w = image.shape[:2]

        # Calculate the dimensions of the smaller images
        small_w = w // 2
        small_h = h // 2

        # Lists to hold the smaller images and their relative positions
        small_images = []
        relative_positions = []

        # Extract each small image
        for i in range(3):
            for j in range(3):
                x_start, x_end = j * small_w // 2, (j + 2) * small_w // 2
                y_start, y_end = i * small_h // 2, (i + 2) * small_h // 2

                small_img = image[y_start:y_end, x_start:x_end]
                small_images.append(small_img)
                relative_positions.append([[y_start, y_end], [x_start, x_end]])

        return small_images, relative_positions
        
