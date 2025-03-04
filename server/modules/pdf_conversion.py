import os
import pymupdf

def extract_images_from_pdf(pdf_path: str) -> list[str]:
    """
    Extracts images from a PDF file and saves them in a folder named after the PDF.
    
    Args:
        pdf_path (str): Path to the input PDF file.
    
    Returns:
        list[str]: List of file paths to the extracted images.
    """
    # Ensure the PDF exists
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")
    
    # Load the PDF document
    with pymupdf.open(pdf_path) as doc:
        
        # Create a folder with the PDF name (without extension)
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_folder = os.path.join(os.path.dirname(pdf_path), pdf_name)
        os.makedirs(output_folder, exist_ok=True)
        
        image_paths = []
        
        # Iterate over each page
        for page_index in range(len(doc)):
            page = doc[page_index]
            image_list = page.get_images()
            
            if not image_list:
                print(f"No images found on page {page_index}")
                continue
            
            for image_index, img in enumerate(image_list, start=1):
                xref = img[0]
                pix = pymupdf.Pixmap(doc, xref)
                
                if pix.n - pix.alpha > 3:  # Convert CMYK to RGB if necessary
                    pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
                
                img_path = os.path.join(output_folder, f"page_{page_index+1}_image_{image_index}.png")
                pix.save(img_path)
                image_paths.append(img_path)
                pix = None  # Free memory
        
        image_paths = [os.path.normpath(path) for path in image_paths]

        return image_paths

if __name__ == "__main__":
    pdf_path = "./data/CBC_Images_tobe delivered/01Jan2025022615_11F2023007525.pdf"
    image_paths = extract_images_from_pdf(pdf_path)
    print(image_paths)