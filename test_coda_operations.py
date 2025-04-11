import os
import unittest
from dotenv import load_dotenv
from codaio import Coda, Document, Cell

class TestCodaOperations(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        load_dotenv()
        self.coda = Coda(os.getenv('CODA_API_TOKEN'))
        self.doc_id = "9omNdUhI4j"
        self.table_id = "grid-PZqFjHZRk_"
        self.doc = Document(self.doc_id, self.coda)
        self.table = self.doc.get_table(self.table_id)

    def test_get_table_data(self):
        """Test if we can get data from a table."""
        try:
            # Get rows from the table
            rows = self.table.rows()
            
            # Print first row data for verification
            if rows:
                first_row = rows[0]
                print("\nFirst row data:")
                print(f"Row ID: {first_row.id}")
                print("Values:", first_row.values)
                
                # Assert that we got some data
                self.assertIsNotNone(first_row.id)
                self.assertIsNotNone(first_row.values)
            else:
                print("No rows found in the table")
                
        except Exception as e:
            self.fail(f"Failed to get table data: {str(e)}")

    def test_update_table_data(self):
        """Test if we can update data in a table."""
        try:
            # Get the first row
            rows = self.table.rows()
            if not rows:
                self.fail("No rows found to test update operation")
            
            first_row = rows[0]
            
            # Create a test update
            test_value = "69"  # Test value
            cells = [
                Cell("c-_WlEd-pWCg", test_value)  # Number of sentences column
            ]
            
            # Perform the update
            update_result = self.table.update_row(first_row.id, cells)
            
            print("\nUpdate operation result:")
            print(update_result)
            
            # Verify the update
            updated_rows = self.table.rows()
            updated_first_row = updated_rows[0]
            
            print("\nUpdated row data:")
            print(f"Row ID: {updated_first_row.id}")
            print("Values:", updated_first_row.values)
            
            # Assert that the update was successful
            self.assertIsNotNone(update_result)
            
        except Exception as e:
            self.fail(f"Failed to update table data: {str(e)}")

if __name__ == '__main__':
    unittest.main() 