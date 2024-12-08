import gc  # Import garbage collection module to manage memory
import re  # Import regular expressions for text processing
import fitz  # Import PyMuPDF for PDF processing
from bisect import bisect_left  # Import bisect for binary search in sorted lists

# Function to extract text, images, and tables from a PDF file
def exact_info(file_path):
    """
    Extracts text, images, and table information from a PDF file.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        tuple: A tuple containing lists of text paragraphs, images, and tables.
               - texts: List of text paragraphs with metadata.
               - images: List of image metadata including description.
               - tables: List of tables with metadata and content.
    """
    # Open the PDF file
    doc = fitz.open(file_path)

    texts = []  # List to store extracted text paragraphs
    images = []  # List to store extracted image metadata
    tables = []  # List to store extracted table information

    # Iterate through all pages in the PDF
    for page_id in range(len(doc)):
        page = doc[page_id]  # Get the current page

        # Extract text blocks from the page
        blocks = page.get_text("blocks")
        height = page.rect.height  # Get the height of the page

        text_paragraphs = []  # List to store text paragraphs on the page

        cnt = 0  # Counter for paragraph IDs
        for block in blocks:
            block = list(block)  # Convert block to a mutable list
            text = block[4]  # Extract text content
            if text.strip() != '':  # Skip empty blocks
                top = block[1]  # Top coordinate of the block
                bottom = block[3]  # Bottom coordinate of the block
                # Filter out headers/footers outside the main content area
                if bottom > height * 0.05 and top < height * (1 - 0.05):
                    # Clean up text by removing excessive whitespace
                    result = re.sub(r'\s+', ' ', text)
                    text = result.replace('\t', ' ').replace('\n', ' ')
                    block[5] = cnt  # Assign paragraph ID
                    block[4] = text  # Update block text
                    block[6] = page_id  # Add page ID to the metadata
                    text_paragraphs.append(tuple(block))  # Add block as a tuple
                    cnt += 1
        # Sort text paragraphs by their top coordinate (Y-axis)
        text_paragraphs = sorted(text_paragraphs, key=lambda x: x[1])
        text_bottoms = [item[3] for item in text_paragraphs]  # Bottom Y-coordinates of text blocks

        del blocks  # Delete blocks to free memory
        gc.collect()  # Run garbage collection

        # Extract images from the page
        image_items = []  # List to store image metadata
        image_list = page.get_images(full=True)  # Get all images on the page

        for i, _ in enumerate(image_list):
            image_top = image_list[i][2]  # Top coordinate of the image
            index = bisect_left(text_bottoms, image_top)  # Find the nearest text block above the image
            # Assign description from the nearest text block
            if index > 0:  
                image_desp = text_paragraphs[index - 1][4]
            else:
                image_desp = text_paragraphs[0][4]
            # Store image description, ID, and page ID
            image_items.append(tuple([image_desp, i, page_id]))

        del image_list  # Delete image list to free memory
        gc.collect()  # Run garbage collection

        # Extract tables from the page
        table_items = []  # List to store table metadata
        table_list = page.find_tables().tables  # Get all tables on the page

        for i, _ in enumerate(table_list):
            table_top = table_list[i].bbox[1]  # Top coordinate of the table
            index = bisect_left(text_bottoms, table_top)  # Find the nearest text block above the table
            table_content = table_list[i].extract()  # Extract table content
            # Assign description from the nearest text block
            if index > 0: 
                table_desp = text_paragraphs[index - 1][4]
            else:
                table_desp = text_paragraphs[0][4]
            # Store table content, description, ID, and page ID
            table_items.append(tuple([table_content, table_desp, i, page_id]))

        del table_list  # Delete table list to free memory
        gc.collect()  # Run garbage collection

        # Append the extracted data to the overall lists
        texts.extend(text_paragraphs)
        images.extend(image_items)
        tables.extend(table_items)

    # Return extracted text, image, and table information
    return texts, images, tables

# Function to format and display extracted results
def format_output(text_res, img_res, tbl_res):
    """
    Formats and prints the extracted text, image, and table information.

    Args:
        text_res (list): List of text paragraphs with metadata.
        img_res (list): List of image metadata.
        tbl_res (list): List of table information with metadata.
    """
    ftxt = []  # Formatted text result
    fimg = []  # Formatted image result
    ftbl = []  # Formatted table result

    # Format text results
    for text in text_res:
        ftxt.append({'text': text[4], 'page': text[6], 'paragraph': text[5]})
    # Format image results
    for img in img_res:
        fimg.append({'description': img[0], 'page': img[2], 'image_no': img[1]})
    # Format table results
    for tbl in tbl_res:
        ftbl.append({'table': tbl[0], 'description': tbl[1], 'page': tbl[3], 'table_no': tbl[2]})

    # Print formatted results
    print('_____________Text Result_______________\n')
    for txt in ftxt:
        print(txt)
    print('_____________Table Result_______________\n')
    for tbl in ftbl:
        print(tbl)
    print('_____________Image Result_______________\n')
    for img in fimg:
        print(img)

# Main entry point for testing
if __name__ == '__main__':
    # Example PDF file path
    file = 'example.pdf'

    # Extract text, image, and table information from the file
    text_res, img_res, tbl_res = exact_info(file)

    # Format and display the extracted results
    format_output(text_res, img_res, tbl_res)
