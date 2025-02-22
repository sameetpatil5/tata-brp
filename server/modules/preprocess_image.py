import cv2 as cv
import numpy as np
import requests
from io import BytesIO
from PIL import Image
import logging

logger = logging.getLogger(__name__)

def load_image(image_path: str) -> np.ndarray:
    """
    Fetches an image from a URL and loads it into a numpy array.
    
    Args:
        image_path (str): URL of the image to preprocess.
    
    Returns:
        np.ndarray: The loaded image in OpenCV BGR format.
    """

    try:
        if "http" not in image_path:
            image_cv = cv.imread(image_path)
            if image_cv is None:
                logger.info(f"Failed to load image from local path")
                logger.error(f"Failed to load image from local path: {image_path}")
            else:
                logger.info(f"Loaded image from local file path")
                logger.debug(f"Loaded image from local file path: {image_path}")
            return image_cv
        
        response = requests.get(image_path)
        response.raise_for_status()
        logger.info(f"Fetched image from URL")
        logger.debug(f"Fetched image from URL: {image_path}")

        image_pil = Image.open(BytesIO(response.content))
        image_array = np.array(image_pil)
        image_cv = cv.cvtColor(image_array, cv.COLOR_RGB2BGR)
        return image_cv
    except requests.RequestException as e:
        logger.error(f"Error fetching image from URL: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in load_image: {e}")
    return None

def save_image(processed_image: np.ndarray, output_path: str) -> None:
    """
    Saves the processed image to a given path.
    """
    try:
        if processed_image is not None:
            cv.imwrite(output_path, processed_image)
            # Logic to save the processed image on Cloud
            logger.info(f"Image saved successfully")
            logger.debug(f"Image saved successfully at: {output_path}")
        else:
            logger.warning("No processed image to save.")
    except Exception as e:
        logger.error(f"Failed to save image: {e}")

def reorder_corner_points(points: np.ndarray) -> np.ndarray:
    """
    Reorders the four corner points into a consistent order: 
    [Top-left, Top-right, Bottom-left, Bottom-right].

    Args:
        points (numpy.ndarray): Unordered four corner points.

    Returns:
        numpy.ndarray: Reordered points.
    """
    try:
        if points is None or points.shape != (4, 1, 2):
            logger.error("Invalid shape for points input, expected (4,1,2)")
            raise ValueError("Error: Expected input shape (4, 1, 2) for reorder.")

        points = points.reshape((4, 2))
        reordered = np.zeros((4, 1, 2), dtype=np.int32)
        add = points.sum(axis=1)
        diff = np.diff(points, axis=1)
        reordered[0] = points[np.argmin(add)]
        reordered[3] = points[np.argmax(add)]
        reordered[1] = points[np.argmin(diff)]
        reordered[2] = points[np.argmax(diff)]
        logger.info("Corner points reordered successfully.")
        return reordered
    except Exception as e:
        logger.error(f"Error in reorder_corner_points: {e}")
    return points

def find_biggest_contour(contours: list) -> tuple[np.ndarray, int]:
    """
    Finds the biggest 4-point contour from a list of contours.

    Args:
        contours (list): List of contours.

    Returns:
        tuple: (Biggest contour as a numpy array, its area).
    """
    try:
        biggest_contour = np.array([])
        max_area = 0
        min_area = 5000

        for contour in contours:
            area = cv.contourArea(contour)
            if area > min_area:
                peri = cv.arcLength(contour, True)
                approx = cv.approxPolyDP(contour, 0.02 * peri, True)
                if len(approx) == 4 and area > max_area:
                    biggest_contour = approx
                    max_area = area
        if biggest_contour.size == 0:
            logger.warning("No suitable contour found.")
        else:
            logger.info(f"Found biggest contour with area: {max_area}")
        return biggest_contour, max_area
    except Exception as e:
        logger.error(f"Error in find_biggest_contour: {e}")
    return np.array([]), 0

def deskew_image(image: np.ndarray, height: float, width: float) -> np.ndarray:
    """
    Deskews an image to improve OCR accuracy.
    
    Args:
        image (numpy.ndarray): Input image.
        height (float): Height of the image.
        width (float): Width of the image.
    
    Returns:
        numpy.ndarray: Deskewed image.
    """
    try:
        # Define the A4 expected area range (for 300 DPI)
        A4_MAX_AREA = 8_700_000  # Upper limit 
        A4_MIN_AREA = 4_000_000  # Lower limit 

        image_blur = cv.GaussianBlur(image, (5, 5), 1)
        image_canny = cv.Canny(image_blur, 100, 100)
        image_dial = cv.dilate(image_canny, np.ones((5, 5)), iterations=2)
        image_erode = cv.erode(image_dial, np.ones((5, 5)), iterations=1)

        contours, _ = cv.findContours(image_erode, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        biggest_contour, max_area = find_biggest_contour(contours)

        logger.info(f"Contour Detected, Area of biggest contour: {max_area}")

        if biggest_contour.size != 0 and A4_MIN_AREA <= max_area <= A4_MAX_AREA:
            logger.info("Deskewing image using biggest contour.")
            # Reorder the biggest contour
            contourReordered = reorder_corner_points(biggest_contour)
            # Perspective transformation/ Deskew Image
            pts1 = np.float32(contourReordered)
            pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
            matrix = cv.getPerspectiveTransform(pts1, pts2)
            image_warped = cv.warpPerspective(image, matrix, (width, height))
            logger.info("Image deskewed successfully.")
            return image_warped
        else:
            logger.warning("Skipping deskewing as no valid contour found.")
    except Exception as e:
        logger.error(f"Error in deskew_image: {e}")
    return image

def increase_contrast(image: np.ndarray) -> np.ndarray:
    """
    Increases contrast in an image.
    
    Args:
        image (numpy.ndarray): Input image.
    
    Returns:
        numpy.ndarray: Image with increased contrast.
    """
    try:
        # Apply adaptive threshold
        image_adaptive_threshold = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 15, 5)
        image_adaptive_threshold = cv.bitwise_not(image_adaptive_threshold)
        image_adaptive_threshold = cv.medianBlur(image_adaptive_threshold, 3)
        image_adaptive_threshold = cv.bitwise_not(image_adaptive_threshold)

        # Add filter
        image_filtered = cv.bilateralFilter(image_adaptive_threshold, d=9, sigmaColor=75, sigmaSpace=75)
        return image_filtered
    except Exception as e:
        logger.error(f"Error while increasing contrast: {e}")
    return image

def denoise_image(image: np.ndarray) -> np.ndarray:
    """
    Denoises an image.
    
    Args:
        image (numpy.ndarray): Input image.
    
    Returns:
        numpy.ndarray: Denoised image.
    """
    try:
        kernel = np.ones((1, 1), np.uint8)

        image_denoised = cv.dilate(image, kernel, iterations=2)  
        image_denoised = cv.erode(image_denoised, kernel, iterations=2)   
        image_denoised = cv.morphologyEx(image_denoised, cv.MORPH_CLOSE, kernel)
        image_denoised = cv.medianBlur(image_denoised, 3)

        # Apply Otsu Threshold
        _, image_otsu_threshold = cv.threshold(image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        
        return image_otsu_threshold
    except Exception as e:
        logger.error(f"Error while Denoising Image: {e}")
    return image

def adjust_borders(image: np.ndarray, height: float, width: float, border_size: int) -> np.ndarray:
    """
    Adjusts the borders of an image to improve OCR accuracy.
    
    Args:
        image (numpy.ndarray): Input image.
        height (float): Height of the image.
        width (float): Width of the image.
        border_size (int): Size of the border to adjust.
    
    Returns:
        numpy.ndarray: Image with adjusted borders.
    """
    try:
        # Adjust Borders and resize
        image_border_adjusted = image[border_size:image.shape[0]-border_size, border_size:image.shape[1]-border_size]
        image_border_adjusted = cv.resize(image_border_adjusted, (width, height))
        image_border_adjusted = cv.copyMakeBorder(image_border_adjusted, border_size, border_size, border_size, border_size, cv.BORDER_CONSTANT, value=(255, 255, 255))
        image_border_adjusted = cv.resize(image_border_adjusted, (width, height))
        return image_border_adjusted
    except Exception as e:
        logger.error(f"Error while Adjusting Borders: {e}")
    return image

def emphasize_text(image: np.ndarray) -> np.ndarray:
    """
    Makes text more visible in an image.
    
    Args:
        image (numpy.ndarray): Input image.
    
    Returns:
        numpy.ndarray: Image with emphasized text.
    """
    try:
        kernel = np.ones((2, 2), np.uint8)

        _, image_emphasized_text = cv.threshold(image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        image_emphasized_text = cv.bitwise_not(image_emphasized_text)
        image_emphasized_text = cv.dilate(image, kernel, iterations=1)
        image_emphasized_text = cv.bitwise_not(image_emphasized_text)
        return image_emphasized_text
    except Exception as e:
        logger.error(f"Error while Emphasizing Text: {e}")
    return image


def preprocess_image(image_path: str) -> np.ndarray:
    """
    Preprocesses an image for OCR.
    
    Args:
        image (str): Path of input Image
    
    Returns:
        numpy.ndarray: Preprocessed image.
    """
    BORDER_SIZE = 20
    try:
        logger.info("Preprocessing image...")
        # Load Image
        image = load_image(image_path)
        # Get image dimensions
        height, width, channels = image.shape
        # Resize image
        image_resized = cv.resize(image, (width, height))
        # Convert to grayscale
        image_grayed = cv.cvtColor(image_resized, cv.COLOR_BGR2GRAY)
        # Deskew Image
        image_deskewed = deskew_image(image_grayed, height, width)
        # Increase contrast
        image_contrasted = increase_contrast(image_deskewed)
        # Denoise Image
        image_denoise = denoise_image(image_contrasted)
        # Adjust borders
        image_bordered = adjust_borders(image_denoise, height, width, BORDER_SIZE)
        # Emphasize text
        image_emphasized = emphasize_text(image_bordered)

        logger.info("Sucessfully preprocessed the image")

        return image_emphasized
    except Exception as e:
        logger.error(f"Error in preprocess_image: {e}")
    return image

if __name__ == "__main__":
    image_path = "E:/SAM ENGINEERINGs/TATA BRP/data/test_image.jpg"
    processed_image = preprocess_image(image_path)
    save_image(processed_image, "E:/SAM ENGINEERINGs/TATA BRP/data/test_new_processed_image.jpg")
