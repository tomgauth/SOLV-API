# SOLV-API

A Python application that syncs student data between Coda tables.

## Features

- Automated synchronization of student data
- REST API endpoints for manual updates
- Scheduled automation running every 15 minutes
- Comprehensive error handling and logging

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SOLV-API.git
cd SOLV-API
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your Coda API token:
```
CODA_API_TOKEN=your_coda_api_token
```

## Usage

### Running the API Server
```bash
python app.py
```

### Running the Automation Script
```bash
python automation.py
```

## API Endpoints

- `GET /health` - Health check endpoint
- `GET /test-student-data` - Test student data retrieval
- `GET /test-specific-table` - Test specific table data retrieval
- `POST /update` - Update student data
- `POST /update-row` - Update a specific row
- `POST /sync-student-data` - Sync student data

## License

MIT 