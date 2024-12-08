from qdrant_client import QdrantClient  # Import QdrantClient for handling the vector database
from pdf_info_exact import exact_info  # Import a custom module to extract information from PDF files

# Function to build the database
def build_database(file_path):
    """
    Extracts information from a PDF file and stores it in a Qdrant database.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        QdrantClient: A Qdrant client instance operating in memory.
    """
    # Initialize the Qdrant client in memory mode
    client = QdrantClient(":memory:")

    # Extract text, image, and table information from the PDF file
    txt_res, img_res, tbl_res = exact_info(file_path)

    # Process text information
    docs = [tx[4] for tx in txt_res]  # Extract the text content
    metadata = []  # Initialize the metadata list
    for tx in txt_res:
        # Create metadata for each text segment, including paragraph ID and page ID
        metadata.append({"para_id": tx[5], "page_id": tx[6]})
    ids = list(range(len(txt_res)))  # Generate unique IDs for each text segment

    # Add the text data to a collection named "txt_collection"
    client.add(
        collection_name="txt_collection",
        documents=docs,
        metadata=metadata,
        ids=ids
    )

    # Process image information
    docs = [im[0] for im in img_res]  # Extract the image content
    metadata = []  # Initialize the metadata list
    for im in img_res:
        # Create metadata for each image, including image ID and page ID
        metadata.append({"para_id": im[1], "page_id": im[2]})
    ids = list(range(len(img_res)))  # Generate unique IDs for each image

    # Add the image data to a collection named "img_collection"
    client.add(
        collection_name="img_collection",
        documents=docs,
        metadata=metadata,
        ids=ids
    )

    # Process table information
    docs = [tb[1] for tb in tbl_res]  # Extract the table content
    metadata = []  # Initialize the metadata list
    for tb in tbl_res:
        # Create metadata for each table, including table ID and page ID
        metadata.append({"para_id": tb[2], "page_id": tb[3]})
    ids = list(range(len(tbl_res)))  # Generate unique IDs for each table

    # Add the table data to a collection named "tbl_collection"
    client.add(
        collection_name="tbl_collection",
        documents=docs,
        metadata=metadata,
        ids=ids
    )

    return client  # Return the Qdrant client instance

# Function to query the database
def db_query(client, type, query):
    """
    Queries the Qdrant database for a specific type of data and returns the result.

    Args:
        client (QdrantClient): The Qdrant client instance.
        type (str): Type of data to query ("txt", "img", or "tbl").
        query (str): Query string to search for.

    Returns:
        str: Query result formatted as a string.
    """
    # Query the specified collection in the database
    search_result = client.query(
        collection_name=f"{type}_collection",  # Collection name based on type
        query_text=query,  # Query text
        limit=1  # Limit to the top result
    )

    # Map the data type to a user-friendly output
    type2output = {'img': "image", 'tbl': "table", 'txt': "text paragraph"}
    coll = type2output[type]
    
    # Format and return the query result
    return f"Found the following information for you, on page {search_result[0].metadata['page_id'] + 1}, "\
           f"{coll} number {search_result[0].metadata['para_id'] + 1}:\n"\
           f"{search_result[0].document}\n"

# Main entry point
if __name__ == "__main__":
    # Example PDF file path
    file = 'example.pdf'

    # Build the database using the specified file
    client = build_database(file)

    # Example query
    query = 'a loop where you know the number of times it will run'
    result = db_query(query=query, type='txt', client=client)  # Perform the query
    
    # Print the result
    print(result)
