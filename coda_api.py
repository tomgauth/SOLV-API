import os
import logging
import requests
from typing import Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CodaAPI:
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://coda.io/apis/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    def extract_ids(self, url: str) -> Tuple[str, str]:
        """Extract document ID and table ID from Coda URL"""
        doc_id = url.split('/d/')[1].split('/')[0]
        table_id = url.split('#')[1].split('_')[1]
        return doc_id, table_id

    def get_table_data(self, doc_id: str, table_id: str) -> Dict:
        """Fetch data from a Coda table"""
        url = f"{self.base_url}/docs/{doc_id}/tables/{table_id}/rows"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data from Coda: {str(e)}")
            raise

    def update_table_data(self, doc_id: str, table_id: str, data: Dict) -> Dict:
        """Update data in a Coda table"""
        url = f"{self.base_url}/docs/{doc_id}/tables/{table_id}/rows"
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error updating data in Coda: {str(e)}")
            raise

    def update_row(self, doc_id: str, table_id: str, row_id: str, values: Dict) -> Dict:
        """Update a specific row in a Coda table"""
        url = f"{self.base_url}/docs/{doc_id}/tables/{table_id}/rows/{row_id}"
        
        # Convert values dict to cells array format
        cells = [{"column": col_id, "value": value} for col_id, value in values.items()]
        
        try:
            response = requests.put(url, headers=self.headers, json={"row": {"cells": cells}})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error updating row in Coda: {str(e)}")
            raise

    def sync_student_data(self, main_doc_id: str, main_table_id: str) -> Dict:
        """Sync data from all student tables to the main table"""
        try:
            # Get all rows from main table
            main_table_data = self.get_table_data(main_doc_id, main_table_id)
            if not main_table_data.get('items'):
                return {"status": "error", "message": "No rows found in main table"}

            results = []
            for row in main_table_data['items']:
                # Extract student doc and table IDs from the row
                cells = {cell['column']: cell['value'] for cell in row['cells']}
                student_doc_id = cells.get('c-JfGAyru56_', '').split('/d/')[-1]
                student_table_id = cells.get('c-oN98cuRpc1', '')
                
                if not student_doc_id or not student_table_id:
                    logger.warning(f"Skipping row {row['id']} - missing doc_id or table_id")
                    continue

                # Get student table data
                student_data = self.get_table_data(student_doc_id, student_table_id)
                num_sentences = len(student_data.get('items', []))

                # Update the main table row
                values = {
                    "c-B5jqLzoe_x": cells.get('c-B5jqLzoe_x', ''),  # first_name
                    "c-_WlEd-pWCg": cells.get('c-_WlEd-pWCg', ''),  # last_name
                    "c-jJ9R5VVvz0": str(num_sentences),  # num_sentences
                    "c-JfGAyru56_": cells.get('c-JfGAyru56_', ''),  # doc_id
                    "c-oN98cuRpc1": cells.get('c-oN98cuRpc1', '')   # sentences_table_id
                }

                result = self.update_row(main_doc_id, main_table_id, row['id'], values)
                results.append({
                    "row_id": row['id'],
                    "num_sentences": num_sentences,
                    "update_result": result
                })

            return {
                "status": "success",
                "message": "Data synced successfully",
                "details": results
            }

        except Exception as e:
            logger.error(f"Error in sync process: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            } 