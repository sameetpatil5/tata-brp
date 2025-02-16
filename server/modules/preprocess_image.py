import cv2 as cv
import numpy as np
import requests
from io import BytesIO
from PIL import Image

def load_image(image_path: str) -> np.ndarray:
    """
    Fetches an image from a URL and loads it into a numpy array.
    
    Args:
        image_path (str): URL of the image to preprocess.
    
    Returns:
        np.ndarray: The loaded image in OpenCV BGR format.
    """

    if "http" not in image_path:
        return cv.imread(image_path)

    response = requests.get(image_path) # Fetch image
    image_pil = Image.open(BytesIO(response.content))  # Open with PIL
    image_array = np.array(image_pil) # Convert to OpenCV format
    image_cv = cv.cvtColor(image_array, cv.COLOR_RGB2BGR) # Convert RGB to BGR

    return image_cv

def save_image(processed_image: np.ndarray, output_path: str):
    """
    Saves the processed image to a given path.
    """
    if processed_image is not None:
        cv.imwrite(output_path, processed_image)
        # Logic to store image to google clould
    else:
        print("No processed image to save.")

def reorder_corner_points(points: np.ndarray) -> np.ndarray:
    """
    Reorders the four corner points into a consistent order: 
    [Top-left, Top-right, Bottom-left, Bottom-right].

    Args:
        points (numpy.ndarray): Unordered four corner points.

    Returns:
        numpy.ndarray: Reordered points.
    """
    if points is None or points.shape != (4, 1, 2):
        raise ValueError("Error: Expected input shape (4, 1, 2) for reorder.")

    points = points.reshape((4, 2))  # Convert to 4x2 shape
    reordered = np.zeros((4, 1, 2), dtype=np.int32)

    add = points.sum(axis=1)  # Sum of (x + y) coordinates
    diff = np.diff(points, axis=1)  # Difference (x - y)

    reordered[0] = points[np.argmin(add)]  # Top-left (smallest sum)
    reordered[3] = points[np.argmax(add)]  # Bottom-right (largest sum)
    reordered[1] = points[np.argmin(diff)]  # Top-right (smallest difference)
    reordered[2] = points[np.argmax(diff)]  # Bottom-left (largest difference)

    return reordered

def findBiggestContour(contours):
    """
    Finds the biggest 4-point contour from a list of contours.

    Args:
        contours (list): List of contours.

    Returns:
        tuple: (Biggest contour as a numpy array, its area).
    """
    biggest = np.array([])
    max_area = 0

    for contour in contours:
        area = cv.contourArea(contour)
        if area > 5000:  # Ignore small noise
            peri = cv.arcLength(contour, True)
            approx = cv.approxPolyDP(contour, 0.02 * peri, True)

            if len(approx) == 4 and area > max_area:  # Ensure it's a quadrilateral
                biggest = approx
                max_area = area

    return biggest, max_area

def noise_removal(image):
    """
    Removes small noise from the image using morphological operations.
    
    Args:
        image (numpy.ndarray): Input binary/grayscale image.
    
    Returns:
        numpy.ndarray: Denoised image.
    """
    if len(image.shape) == 3:
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)  # Convert to grayscale if needed

    kernel = np.ones((1, 1), np.uint8)

    # Morphological operations to remove small noise
    image = cv.dilate(image, kernel, iterations=2)  # Expands white regions
    image = cv.erode(image, kernel, iterations=2)   # Shrinks white regions back to original size
    image = cv.morphologyEx(image, cv.MORPH_CLOSE, kernel)  # Fills small holes

    # Apply median blur for smoother noise removal
    image = cv.medianBlur(image, 3)

    return image

def thick_font(image):
    """
    Makes text thicker in a binary image to improve OCR readability.
    
    Args:
        image (numpy.ndarray): Input binary image (black text on white background).
    
    Returns:
        numpy.ndarray: Image with thickened font.
    """
    if len(image.shape) == 3:
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)  # Convert to grayscale if needed

    # Ensure the image is binary
    _, image = cv.threshold(image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    # Invert the image (to make text white and background black)
    image = cv.bitwise_not(image)

    # Apply dilation to thicken the text
    kernel = np.ones((2, 2), np.uint8)
    image = cv.dilate(image, kernel, iterations=1)

    # Invert back to original format
    image = cv.bitwise_not(image)

    return image

def deskew_image(image, height, width):
    """
    Deskews an image to improve OCR accuracy.
    
    Args:
        image (numpy.ndarray): Input image.
    
    Returns:
        numpy.ndarray: Deskewed image.
    """

    # Apply Gaussian blur
    imageBlur = cv.GaussianBlur(image, (5, 5), 1)
    # Apply Canny edge detection
    imageCanny = cv.Canny(imageBlur, 100, 100)
    # Image Dilation
    imageDial = cv.dilate(imageCanny, np.ones((5, 5)), iterations=2)
    # Image Erosion
    imageErode = cv.erode(imageDial, np.ones((5, 5)), iterations=1)

    # Find contours
    contours, _ = cv.findContours(imageErode, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Find the biggest contour
    imageContours = image.copy()
    biggestContour, maxArea = findBiggestContour(contours)

    print(f"Detected Contour Area: {maxArea}")

    # Define the A4 expected area range (for 300 DPI)
    A4_MAX_AREA = 8_700_000  # Upper limit for A4 paper
    A4_MIN_AREA = 4_000_000  # Lower limit to filter noise/small objects

    if biggestContour.size != 0 and A4_MIN_AREA <= maxArea <= A4_MAX_AREA:

        # Reorder the biggest contour
        contourReordered = reorder_corner_points(biggestContour)
        cv.drawContours(imageContours, contourReordered, -1, (0, 255, 0), 20)
        
        # Perspective transformation/ Deskew Image
        pts1 = np.float32(contourReordered)
        pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        matrix = cv.getPerspectiveTransform(pts1, pts2)
        imageWarpped = cv.warpPerspective(image, matrix, (width, height))

        return imageWarpped
    else:
        return image

def increase_contrast(image):
    """
    Increases contrast in an image.
    
    Args:
        image (numpy.ndarray): Input image.
    
    Returns:
        numpy.ndarray: Image with increased contrast.
    """
    # Apply adaptive threshold
    imageAdaptiveThreshold = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 15, 5)
    imageAdaptiveThreshold = cv.bitwise_not(imageAdaptiveThreshold)
    imageAdaptiveThreshold = cv.medianBlur(imageAdaptiveThreshold, 3)
    imageAdaptiveThreshold = cv.bitwise_not(imageAdaptiveThreshold)

    # Add filter
    imageFiltered = cv.bilateralFilter(imageAdaptiveThreshold, d=9, sigmaColor=75, sigmaSpace=75)

    return imageFiltered

def denoise_image(image):
    """
    Denoises an image.
    
    Args:
        image (numpy.ndarray): Input image.
    
    Returns:
        numpy.ndarray: Denoised image.
    """
    # Remove Noise
    kernel = np.ones((1, 1), np.uint8)

    # Morphological operations to remove small noise
    imageNoiseOut = cv.dilate(image, kernel, iterations=2)  # Expands white regions
    imageNoiseOut = cv.erode(image, kernel, iterations=2)   # Shrinks white regions back to original size
    imageNoiseOut = cv.morphologyEx(image, cv.MORPH_CLOSE, kernel)  # Fills small holes

    # Apply median blur for smoother noise removal
    imageNoiseOut = cv.medianBlur(image, 3)

    # Apply Otsu Threshold
    _, ImageOtsuThreshold = cv.threshold(imageNoiseOut, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    
    return ImageOtsuThreshold

def adjust_borders(image, height, width, borderSize):
    """
    Adjusts the borders of an image to improve OCR accuracy.
    
    Args:
        image (numpy.ndarray): Input image.
    
    Returns:
        numpy.ndarray: Image with adjusted borders.
    """
    # Adjust Borders and resize
    imageBorderAdjust = image[borderSize:image.shape[0]-borderSize, borderSize:image.shape[1]-borderSize]
    imageBorderAdjust = cv.resize(imageBorderAdjust, (width, height))
    imageBorderAdjust = cv.copyMakeBorder(imageBorderAdjust, borderSize, borderSize, borderSize, borderSize, cv.BORDER_CONSTANT, value=(255, 255, 255))
    imageBorderAdjust = cv.resize(imageBorderAdjust, (width, height))
    return imageBorderAdjust

def emphasize_text(image):
    """
    Makes text more visible in an image.
    
    Args:
        image (numpy.ndarray): Input image.
    
    Returns:
        numpy.ndarray: Image with emphasized text.
    """
    # Ensure the image is binary
    _, image = cv.threshold(image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    # Invert the image (to make text white and background black)
    image = cv.bitwise_not(image)

    # Apply dilation to thicken the text
    kernel = np.ones((2, 2), np.uint8)
    image = cv.dilate(image, kernel, iterations=1)

    # Invert back to original format
    image = cv.bitwise_not(image)

    return image


def preprocess_image(image: np.ndarray) -> np.ndarray:
    """
    Preprocesses an image for OCR.
    
    Args:
        image (np.ndarray): Input Image
    
    Returns:
        numpy.ndarray: Preprocessed image.
    """
    BORDER_SIZE = 20

    # Load Image
    image = load_image(image_path)
    # Get image dimensions
    height, width, channels = image.shape
    # Resize image
    imageResized = cv.resize(image, (width, height))
    # Convert to grayscale
    imageGrayed = cv.cvtColor(imageResized, cv.COLOR_BGR2GRAY)
    # Deskew Image
    imageDeskewed = deskew_image(imageGrayed, height, width)
    # Increase contrast
    imageContrasted = increase_contrast(imageDeskewed)
    # Denoise Image
    imageDenoise = denoise_image(imageContrasted)
    # Adjust borders
    imageBordered = adjust_borders(imageDenoise, height, width, BORDER_SIZE)
    # Emphasize text
    imageEmphasized = emphasize_text(imageBordered)

    return imageEmphasized

if __name__ == "__main__":
    image_path = "E:/SAM ENGINEERINGs/TATA BRP/tests/image.jpg"
    image = load_image(image_path)
    processed_image = preprocess_image(image)
    save_image(processed_image, "E:/SAM ENGINEERINGs/TATA BRP/tests/new_processed_image.jpg")
