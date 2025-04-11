import os
import logging
from flask import Flask, jsonify
from dotenv import load_dotenv
from coda_api import CodaAPI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Coda API configuration
CODA_API_TOKEN = os.getenv('CODA_API_TOKEN')
MAIN_DOC_URL = os.getenv('MAIN_DOC_URL')
STUDENT_DOC_URL = os.getenv('STUDENT_DOC_URL')

# Extract document and table IDs from URLs
def extract_ids(url):
    # Extract document ID and table ID from Coda URL
    doc_id = url.split('/d/')[1].split('/')[0]
    table_id = url.split('#')[1].split('_')[1]
    return doc_id, table_id

def get_coda_data(doc_id, table_id):
    """Fetch data from a Coda table"""
    url = f"https://coda.io/apis/v1/docs/{doc_id}/tables/{table_id}/rows"
    headers = {
        "Authorization": f"Bearer {CODA_API_TOKEN}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data from Coda: {str(e)}")
        raise

def update_coda_data(doc_id, table_id, data):
    """Update data in a Coda table"""
    url = f"https://coda.io/apis/v1/docs/{doc_id}/tables/{table_id}/rows"
    headers = {
        "Authorization": f"Bearer {CODA_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error updating data in Coda: {str(e)}")
        raise

def update_coda_row(doc_id, table_id, row_id, values):
    """Update a specific row in a Coda table"""
    url = f"https://coda.io/apis/v1/docs/{doc_id}/tables/{table_id}/rows/{row_id}"
    headers = {
        "Authorization": f"Bearer {CODA_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Convert values dict to cells array format
    cells = [{"column": col_id, "value": value} for col_id, value in values.items()]
    
    try:
        response = requests.put(url, headers=headers, json={"row": {"cells": cells}})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error updating row in Coda: {str(e)}")
        raise

@app.route('/update', methods=['POST'])
def update_data():
    try:
        # Get student document data
        student_doc_id, student_table_id = extract_ids(STUDENT_DOC_URL)
        student_data = get_coda_data(student_doc_id, student_table_id)
        
        # Get main document data
        main_doc_id, main_table_id = extract_ids(MAIN_DOC_URL)
        main_data = get_coda_data(main_doc_id, main_table_id)
        
        # Process and update data
        # This is a simple implementation - you can add more complex merging logic here
        update_data = {
            "rows": student_data.get('items', [])
        }
        
        result = update_coda_data(main_doc_id, main_table_id, update_data)
        
        return jsonify({
            "status": "success",
            "message": "Data updated successfully",
            "details": result
        })
        
    except Exception as e:
        logger.error(f"Error in update process: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/test-student-data', methods=['GET'])
def test_student_data():
    try:
        # Get student document data
        student_doc_id, student_table_id = extract_ids(STUDENT_DOC_URL)
        student_data = get_coda_data(student_doc_id, student_table_id)
        
        return jsonify({
            "status": "success",
            "data": student_data
        })
        
    except Exception as e:
        logger.error(f"Error fetching student data: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/test-specific-table', methods=['GET'])
def test_specific_table():
    try:
        # Use the specific IDs provided
        doc_id = "9omNdUhI4j"
        table_id = "grid-PZqFjHZRk_"
        
        # Get the data
        table_data = get_coda_data(doc_id, table_id)
        
        return jsonify({
            "status": "success",
            "data": table_data
        })
        
    except Exception as e:
        logger.error(f"Error fetching specific table data: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/update-row', methods=['POST'])
def update_row():
    try:
        doc_id = "9omNdUhI4j"
        table_id = "grid-PZqFjHZRk_"
        
        # First, get the table data to find the row ID
        table_data = get_coda_data(doc_id, table_id)
        if not table_data.get('items'):
            return jsonify({"status": "error", "message": "No rows found in table"}), 404
            
        # Get the first row's ID
        row_id = table_data['items'][0]['id']
        
        # Update the row with new values
        values = {
            "c-B5jqLzoe_x": "Tom",  # Name
            "c-jJ9R5VVvz0": "69",   # Number of sentences
            "c-JfGAyru56_": "",     # Other fields
            "c-oN98cuRpc1": "",
            "c-_WlEd-pWCg": "Gauthier"
        }
        
        result = update_coda_row(doc_id, table_id, row_id, values)
        
        return jsonify({
            "status": "success",
            "message": "Row updated successfully",
            "data": result
        })
        
    except Exception as e:
        logger.error(f"Error in update process: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/sync-student-data', methods=['POST'])
def sync_student_data():
    try:
        # Student's table details
        student_doc_id = "IVSZ0d1Fva"
        student_table_id = "grid-5NNVioJykj"
        
        # Main table details
        main_doc_id = "9omNdUhI4j"
        main_table_id = "grid-PZqFjHZRk_"
        
        # Get student table data
        student_data = get_coda_data(student_doc_id, student_table_id)
        if not student_data.get('items'):
            return jsonify({"status": "error", "message": "No data found in student table"}), 404
            
        # Count the number of rows in student table
        num_sentences = len(student_data['items'])
        
        # Get the first row from main table to update
        main_table_data = get_coda_data(main_doc_id, main_table_id)
        if not main_table_data.get('items'):
            return jsonify({"status": "error", "message": "No rows found in main table"}), 404
            
        row_id = main_table_data['items'][0]['id']
        
        # Update the row with the new data
        values = {
            "c-B5jqLzoe_x": "Tom",  # first_name
            "c-_WlEd-pWCg": "Gauthier",  # last_name
            "c-jJ9R5VVvz0": str(num_sentences),  # num_sentences
            "c-JfGAyru56_": f"https://coda.io/d/{student_doc_id}",  # doc_id
            "c-oN98cuRpc1": student_table_id  # sentences_table_id
        }
        
        # Convert values dict to cells array format
        cells = [{"column": col_id, "value": value} for col_id, value in values.items()]
        
        # Update the row
        result = update_coda_row(main_doc_id, main_table_id, row_id, values)
        
        return jsonify({
            "status": "success",
            "message": "Data synced successfully",
            "details": {
                "num_sentences": num_sentences,
                "update_result": result
            }
        })
        
    except Exception as e:
        logger.error(f"Error in sync process: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

def main():
    """Main function to run the app"""
    try:
        # Initialize Coda API client
        coda = CodaAPI(os.getenv('CODA_API_TOKEN'))
        
        # Main table details
        main_doc_id = "9omNdUhI4j"
        main_table_id = "grid-PZqFjHZRk_"
        
        # Run the sync
        result = coda.sync_student_data(main_doc_id, main_table_id)
        
        if result['status'] == 'success':
            logger.info(f"Sync completed successfully")
            logger.info(f"Updated {len(result['details'])} rows")
        else:
            logger.error(f"Sync failed: {result['message']}")
            
    except Exception as e:
        logger.error(f"Error in sync process: {str(e)}")

if __name__ == '__main__':
    main() 