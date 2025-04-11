import os
import unittest
from datetime import datetime
from dotenv import load_dotenv
from codaio import Document, Cell
from automation import BaseAutomation, SentenceCountAutomation

class TestBaseAutomation(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        load_dotenv()
        self.automation = BaseAutomation("Test Automation", interval_minutes=1)
        
    def test_initialization(self):
        """Test if automation initializes correctly."""
        self.assertEqual(self.automation.name, "Test Automation")
        self.assertEqual(self.automation.interval_minutes, 1)
        self.assertIsNotNone(self.automation.coda)
        self.assertIsNone(self.automation.last_run)
        
    def test_stats_initialization(self):
        """Test if statistics are initialized correctly."""
        stats = self.automation.stats
        self.assertEqual(stats['total_runs'], 0)
        self.assertEqual(stats['successful_runs'], 0)
        self.assertEqual(stats['failed_runs'], 0)
        self.assertIsNone(stats['last_error'])

class TestSentenceCountAutomation(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        load_dotenv()
        self.automation = SentenceCountAutomation()
        
    def test_extract_doc_id(self):
        """Test document ID extraction from URL."""
        url = "https://coda.io/d/HFWT-30-90_d9omNdUhI4j/Data_suRar6rP"
        doc_id = self.automation._extract_doc_id(url)
        self.assertEqual(doc_id, "9omNdUhI4j")
        
    def test_get_table_data(self):
        """Test if we can get data from the clients table."""
        try:
            # Get the document and table using correct syntax
            doc = Document.from_environment(self.automation.doc_id)
            table = doc.get_table(self.automation.table_id)
            rows = table.rows(limit=10)  # Get first 10 rows
            
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
            
    def test_execute_success(self):
        """Test successful execution of sentence counting automation with real data."""
        try:
            result = self.automation._execute()
            
            # Print results for verification
            print("\nAutomation results:")
            print(f"Total rows processed: {result['total_rows_processed']}")
            print(f"Rows updated: {result['rows_updated']}")
            print(f"Errors: {result['errors']}")
            
            if result['details']:
                print("\nFirst row details:")
                print(result['details'][0])
            
            # Verify the result structure
            self.assertIsInstance(result, dict)
            self.assertIn('total_rows_processed', result)
            self.assertIn('rows_updated', result)
            self.assertIn('errors', result)
            self.assertIn('details', result)
            
        except Exception as e:
            self.fail(f"Failed to execute automation: {str(e)}")
            
    def test_update_row(self):
        """Test updating a row with real data."""
        try:
            # Get the document and table using correct syntax
            doc = Document.from_environment(self.automation.doc_id)
            table = doc.get_table(self.automation.table_id)
            rows = table.rows(limit=1)  # Get first row
            
            if not rows:
                self.skipTest("No rows found to test update")
                
            first_row = rows[0]
            
            # Create a test update using correct Cell syntax
            test_value = "69"  # Test value
            column = table.get_column_by_id("c-_WlEd-pWCg")  # Get column object
            cells = [
                Cell(column, test_value)  # Create cell with column object and value
            ]
            
            # Perform the update
            update_result = table.update_row(first_row.id, cells)
            
            print("\nUpdate operation result:")
            print(update_result)
            
            # Verify the update
            updated_rows = table.rows(limit=1)
            updated_first_row = updated_rows[0]
            
            print("\nUpdated row data:")
            print(f"Row ID: {updated_first_row.id}")
            print("Values:", updated_first_row.values)
            
            # Assert that the update was successful
            self.assertIsNotNone(update_result)
            
        except Exception as e:
            self.fail(f"Failed to update row: {str(e)}")
            
    def test_run_success(self):
        """Test successful run of the automation with real data."""
        try:
            result = self.automation.run()
            
            # Print statistics
            print("\nAutomation statistics:")
            print(f"Total runs: {self.automation.stats['total_runs']}")
            print(f"Successful runs: {self.automation.stats['successful_runs']}")
            print(f"Failed runs: {self.automation.stats['failed_runs']}")
            print(f"Last run: {self.automation.last_run}")
            
            # Verify statistics were updated
            self.assertEqual(self.automation.stats['total_runs'], 1)
            self.assertEqual(self.automation.stats['successful_runs'], 1)
            self.assertEqual(self.automation.stats['failed_runs'], 0)
            self.assertIsNotNone(self.automation.last_run)
            
        except Exception as e:
            self.fail(f"Failed to run automation: {str(e)}")

if __name__ == '__main__':
    unittest.main() 