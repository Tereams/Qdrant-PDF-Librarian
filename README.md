# Qdrant-PDF-Librarian

This project extracts text, images, and tables from PDF files, stores the data in a vector database (`Qdrant`), and allows querying the database for specific information.

---

## Features

1. **Extract Content from PDFs:**
   - Text paragraphs with metadata (page number, paragraph ID).
   - Images with descriptions based on nearby text.
   - Tables with content and associated metadata.

2. **Qdrant Vector Database Integration:**
   - Automatically stores the extracted data in an in-memory Qdrant database.
   - Allows querying specific types of data (text, images, or tables) with a user-friendly output.

3. **Customizable Queries:**
   - Retrieve specific data types by their descriptions or content.

---

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/pdf-content-extractor.git
   cd pdf-content-extractor

2. Install the required Python dependencies:

   ```bash
   pip install -r requirements.txt

## Usage
### Extracting and Viewing Content

1. Place the PDF file you want to process in the project directory.
2. Modify the file variable in the main section of extractor.py to the name of your PDF file:
   ```python
   client = build_database('example.pdf')

3. Run the script:

   ```bash
   python extractor.py

4. The script will extract and print the text, image, and table data in the terminal.

### Storing and Querying Data with Qdrant
1. Ensure the Qdrant client is properly installed:

    ```bash
    pip install qdrant-client
2. Use the build_database function to extract and store data from a PDF file into the Qdrant database:

    ```python
    client = build_database('example.pdf')
3. Query the database for specific information using db_query:

    ```python
    query = 'Count-controlled loop: a loop where you know the number of times it will run'
    result = db_query(query=query, type='txt', client=client)
    print(result)
Replace the query string with your desired search term and type with one of:
- 'txt' for text paragraphs
- 'img' for images
- 'tbl' for tables
4. Example query output:

    ```vbnet
    Found the following information for you, on page 9, text paragraph number 4:
    "This is the content of the matched paragraph."

## Output Format
### Extracted Data:
- Text:
    ```json
    {
    "text": "Extracted text paragraph content",
    "page": 1,
    "paragraph": 0
    }
- Image:

    ```json
    {
    "description": "Nearby text description of the image",
    "page": 2,
    "image_no": 1
    }
- Table:
    ```json
    {
    "table": "Table content in raw format",
    "description": "Nearby text description of the table",
    "page": 3,
    "table_no": 0
    }
### Query Result
- input
    ```vbnet
    query = 'a loop where you know the number of times it will run'
- output
    ```vbnet
    Found the following information for you, on page 2, text paragraph number 3:
    "Count-controlled loop: a loop where you know the number of times it will run. "

## Contributing
Contributions are welcome! If you find any bugs or have feature suggestions, feel free to open an issue or submit a pull request.
