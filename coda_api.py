import os
from dotenv import load_dotenv
from codaio import Coda
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CodaAPI:
    def __init__(self, api_token):
        self.coda = Coda(api_key=api_token)
        
        # Constants for the main Clients table
        self.MAIN_DOC_ID = "9omNdUhI4j"           # Main document ID containing the Clients table
        self.CLIENTS_TABLE_ID = "grid-PZqFjHZRk_"   # Clients table ID

        # Column IDs for the Clients table
        self.COL_FIRST_NAME = "c-B5jqLzoe_x"
        self.COL_LAST_NAME = "c-_WlEd-pWCg"
        self.COL_CLIENT_DOC_ID = "c-jJ9R5VVvz0"  # The student's document ID
        self.COL_SENTENCES_TABLE = "c-oN98cuRpc1"  # The student's sentences table ID
        self.COL_NUM_SENTENCES = "c-JfGAyru56_"  # The column to update with the count
        self.COL_DOC_URL = "c-5b3Ye-Mf5S"   # The URL to the student's document (not used here)

    def sync_clients_sentence_counts(self):
        """Sync sentence counts for all clients."""
        try:
            # Retrieve the main Clients table data
            clients_data = self.coda.list_rows(doc_id=self.MAIN_DOC_ID, table_id_or_name=self.CLIENTS_TABLE_ID)
            
            results = {
                'total_rows_processed': 0,
                'rows_updated': 0,
                'errors': 0,
                'details': []
            }

            # Iterate through each row in the Clients table
            for row in clients_data.get("items", []):
                row_id = row.get("id")
                values = row.get("values", {})
                results['total_rows_processed'] += 1

                # Get the student's document ID and their sentences table ID from the row values.
                student_doc_id = values.get(self.COL_CLIENT_DOC_ID)
                sentences_table_id = values.get(self.COL_SENTENCES_TABLE)

                if not sentences_table_id:
                    results['errors'] += 1
                    results['details'].append({
                        'row_id': row_id,
                        'error': 'Missing sentences_table_id'
                    })
                    continue

                if not student_doc_id:
                    results['errors'] += 1
                    results['details'].append({
                        'row_id': row_id,
                        'error': 'Missing client_doc_id'
                    })
                    continue

                try:
                    # Fetch the student's sentences table data from their document
                    sentences_data = self.coda.list_rows(doc_id=student_doc_id, table_id_or_name=sentences_table_id)
                    
                    # Count the number of rows (each row represents a sentence)
                    sentence_count = len(sentences_data.get("items", []))

                    # Prepare the payload to update the 'num_sentences' column in the Clients table
                    update_payload = {
                        "row": {
                            "cells": [
                                {"column": self.COL_NUM_SENTENCES, "value": sentence_count}
                            ]
                        }
                    }

                    # Update the client's row in the main Clients table
                    self.coda.update_row(
                        doc_id=self.MAIN_DOC_ID,
                        table_id_or_name=self.CLIENTS_TABLE_ID,
                        row_id_or_name=row_id,
                        data=update_payload
                    )
                    
                    results['rows_updated'] += 1
                    results['details'].append({
                        'row_id': row_id,
                        'student_doc_id': student_doc_id,
                        'sentence_count': sentence_count
                    })

                except Exception as e:
                    results['errors'] += 1
                    results['details'].append({
                        'row_id': row_id,
                        'error': str(e)
                    })

            return results

        except Exception as e:
            return {
                'error': str(e),
                'total_rows_processed': results.get('total_rows_processed', 0),
                'rows_updated': results.get('rows_updated', 0),
                'errors': results.get('errors', 0) + 1,
                'details': results.get('details', [])
            }



