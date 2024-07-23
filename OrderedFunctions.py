class Image_stitching: 

    def __init__(self):

      
        self.name = "Image_Analysis"



  
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
