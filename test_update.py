import os
import unittest
from dotenv import load_dotenv
from coda_api import CodaAPI

# Load environment variables
load_dotenv()

class TestCodaAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize the Coda API client once for all tests."""
        cls.coda = CodaAPI()
    
    def test_get_table_data(self):
        """Test pulling data from the table."""
        # Get table data
        table_data = self.coda.get_table_data()
        
        # Verify we got data
        self.assertIsNotNone(table_data, "Table data should not be None")
        self.assertIsInstance(table_data, list, "Table data should be a list")
        
        if table_data:
            # Print first row for debugging
            print("\nFirst row data:")
            for key, value in table_data[0].items():
                print(f"  {key}: {value}")
            
            # Basic data validation
            first_row = table_data[0]
            self.assertIsInstance(first_row, dict, "Each row should be a dictionary")
            self.assertTrue(len(first_row) > 0, "Row should have at least one column")
            self.assertIn('id', first_row, "Row should have an ID")
    
    def test_update_row(self):
        """Test updating a row in the table."""
        # First, get the table data to find a row to update
        table_data = self.coda.get_table_data()
        self.assertIsNotNone(table_data, "Should be able to get table data")
        
        if not table_data:
            self.fail("No data in table to test update")
        
        # Get the first row's ID
        first_row = table_data[0]
        row_id = first_row['id']
        self.assertIsNotNone(row_id, "Row should have an ID")
        
        # Get the column IDs from the first row
        column_ids = [key for key in first_row.keys() if key != 'id']
        self.assertTrue(len(column_ids) > 0, "Row should have columns")
        
        # Choose a column to update (preferably a numeric one)
        # For testing, we'll update the first column that isn't 'id'
        update_column = column_ids[0]
        self.assertIsNotNone(update_column, "Should find a column to update")
        
        # Get the current value
        current_value = first_row[update_column]
        
        # Update the value (increment if numeric, otherwise set to test value)
        try:
            new_value = str(int(current_value) + 1) if str(current_value).isdigit() else "test_value"
        except (ValueError, AttributeError):
            new_value = "test_value"
        
        # Perform the update
        update_result = self.coda.update_row(row_id, {update_column: new_value})
        self.assertTrue(update_result, "Update should succeed")
        
        # Verify the update
        updated_data = self.coda.get_table_data()
        updated_row = next((row for row in updated_data if row['id'] == row_id), None)
        self.assertIsNotNone(updated_row, "Should find the updated row")
        self.assertEqual(updated_row[update_column], new_value, "Value should be updated")
        
        # Print update results for debugging
        print(f"\nUpdate test results:")
        print(f"Column updated: {update_column}")
        print(f"Old value: {current_value}")
        print(f"New value: {new_value}")
        print(f"Update successful: {update_result}")

if __name__ == '__main__':
    unittest.main() 