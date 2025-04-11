import os
import logging
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
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

# Initialize Flask app
app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})

@app.route('/sync', methods=['POST'])
def sync_data():
    """Endpoint to trigger data synchronization."""
    try:
        coda = CodaAPI(api_token=os.getenv('CODA_API_TOKEN'))
        result = coda.sync_clients_sentence_counts()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error during sync: {str(e)}")
        return jsonify({"error": str(e)}), 500

# New Coda API endpoints
@app.route('/api/column/<doc_id>/<table_id>/<column_id>', methods=['GET'])
def get_column(doc_id, table_id, column_id):
    """Get column details."""
    try:
        coda = CodaAPI(api_token=os.getenv('CODA_API_TOKEN'))
        result = coda.coda.get_column(doc_id, table_id, column_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting column: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/control/<doc_id>/<control_id>', methods=['GET'])
def get_control(doc_id, control_id):
    """Get control details."""
    try:
        coda = CodaAPI(api_token=os.getenv('CODA_API_TOKEN'))
        result = coda.coda.get_control(doc_id, control_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting control: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/doc/<doc_id>', methods=['GET'])
def get_doc(doc_id):
    """Get document details."""
    try:
        coda = CodaAPI(api_token=os.getenv('CODA_API_TOKEN'))
        result = coda.coda.get_doc(doc_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting doc: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/folder/<doc_id>/<folder_id>', methods=['GET'])
def get_folder(doc_id, folder_id):
    """Get folder details."""
    try:
        coda = CodaAPI(api_token=os.getenv('CODA_API_TOKEN'))
        result = coda.coda.get_folder(doc_id, folder_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting folder: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/formula/<doc_id>/<formula_id>', methods=['GET'])
def get_formula(doc_id, formula_id):
    """Get formula details."""
    try:
        coda = CodaAPI(api_token=os.getenv('CODA_API_TOKEN'))
        result = coda.coda.get_formula(doc_id, formula_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting formula: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/row/<doc_id>/<table_id>/<row_id>', methods=['GET'])
def get_row(doc_id, table_id, row_id):
    """Get row details."""
    try:
        coda = CodaAPI(api_token=os.getenv('CODA_API_TOKEN'))
        result = coda.coda.get_row(doc_id, table_id, row_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting row: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/section/<doc_id>/<section_id>', methods=['GET'])
def get_section(doc_id, section_id):
    """Get section details."""
    try:
        coda = CodaAPI(api_token=os.getenv('CODA_API_TOKEN'))
        result = coda.coda.get_section(doc_id, section_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting section: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/table/<doc_id>/<table_id>', methods=['GET'])
def get_table(doc_id, table_id):
    """Get table details."""
    try:
        coda = CodaAPI(api_token=os.getenv('CODA_API_TOKEN'))
        result = coda.coda.get_table(doc_id, table_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting table: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/row/<doc_id>/<table_id>/<row_id>', methods=['PUT'])
def update_row(doc_id, table_id, row_id):
    """Update a row."""
    try:
        coda = CodaAPI(api_token=os.getenv('CODA_API_TOKEN'))
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        result = coda.coda.update_row(doc_id, table_id, row_id, data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error updating row: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/row/upsert/<doc_id>/<table_id>', methods=['POST'])
def upsert_row(doc_id, table_id):
    """Upsert rows."""
    try:
        coda = CodaAPI(api_token=os.getenv('CODA_API_TOKEN'))
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        result = coda.coda.upsert_row(doc_id, table_id, data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error upserting row: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True) 