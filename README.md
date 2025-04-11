# SOLV-API

A Flask API for syncing sentence counts between Coda documents.

## Features

- RESTful API endpoints for Coda document operations
- Automated sentence count synchronization
- Scheduled tasks for regular updates
- CORS support for cross-origin requests

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SOLV-API.git
cd SOLV-API
```

2. Create a virtual environment and activate it:
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
CODA_API_TOKEN=your_api_token_here
MAIN_DOC_URL=your_main_doc_url
STUDENT_DOC_URL=your_student_doc_url
```

## Running Locally

1. Start the Flask server:
```bash
python app.py
```

2. Start the automation runner:
```bash
python automation_runner.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /health` - Health check
- `POST /sync` - Trigger manual sync
- `GET /api/table/{doc_id}/{table_id}` - Get table details
- `GET /api/row/{doc_id}/{table_id}/{row_id}` - Get row details
- `PUT /api/row/{doc_id}/{table_id}/{row_id}` - Update a row
- `POST /api/row/upsert/{doc_id}/{table_id}` - Upsert rows

## Deployment

### Heroku

1. Create a new Heroku app:
```bash
heroku create your-app-name
```

2. Set environment variables:
```bash
heroku config:set CODA_API_TOKEN=your_api_token_here
heroku config:set MAIN_DOC_URL=your_main_doc_url
heroku config:set STUDENT_DOC_URL=your_student_doc_url
```

3. Deploy to Heroku:
```bash
git push heroku main
```

### GitHub Actions

The repository includes a GitHub Actions workflow for automatic deployment to Heroku. Make sure to set up the following secrets in your GitHub repository:

- `HEROKU_API_KEY`
- `HEROKU_APP_NAME`
- `CODA_API_TOKEN`
- `MAIN_DOC_URL`
- `STUDENT_DOC_URL`

## License

MIT 