import os
from dotenv import load_dotenv
from codaio import Coda
from coda_api import CodaAPI

# Load environment variables
load_dotenv()

def test_connection():
    # Test basic Coda connection
    coda = Coda(api_key=os.getenv('CODA_API_TOKEN'))
    try:
        # Get account info to verify connection
        account = coda.account()
        print("Successfully connected to Coda API")
        print(f"Account info: {account}")
        return True
    except Exception as e:
        print(f"Error connecting to Coda API: {e}")
        return False

def test_document_access():
    # Test accessing the main document
    coda = CodaAPI(os.getenv('CODA_API_TOKEN'))
    try:
        # Get the main document
        doc = coda.coda.get_doc(doc_id=coda.MAIN_DOC_ID)
        print(f"Successfully accessed document: {doc.get('name', 'Unknown')}")
        return True
    except Exception as e:
        print(f"Error accessing document: {e}")
        return False

def test_table_access():
    # Test accessing the main table
    coda = CodaAPI(os.getenv('CODA_API_TOKEN'))
    try:
        # Get the main table
        table = coda.coda.get_table(doc_id=coda.MAIN_DOC_ID, table_id_or_name=coda.CLIENTS_TABLE_ID)
        print("Successfully accessed table.")
        print(f"Table info: {table}")
        
        # Get rows
        rows = coda.coda.list_rows(doc_id=coda.MAIN_DOC_ID, table_id_or_name=coda.CLIENTS_TABLE_ID)
        print(f"\nRows: {rows}")
        
        return True
    except Exception as e:
        print(f"Error accessing table: {e}")
        return False

if __name__ == '__main__':
    print("Testing Coda API connection...")
    if test_connection():
        print("\nTesting document access...")
        if test_document_access():
            print("\nTesting table access...")
            test_table_access() 