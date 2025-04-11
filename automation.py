import os
import time
import logging
from datetime import datetime
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

def run_sync():
    """Run the sync process for all student data"""
    try:
        # Initialize Coda API client
        coda = CodaAPI(os.getenv('CODA_API_TOKEN'))
        
        # Main table details
        main_doc_id = "9omNdUhI4j"
        main_table_id = "grid-PZqFjHZRk_"
        
        # Run the sync
        result = coda.sync_student_data(main_doc_id, main_table_id)
        
        if result['status'] == 'success':
            logger.info(f"Sync completed successfully at {datetime.now()}")
            logger.info(f"Updated {len(result['details'])} rows")
        else:
            logger.error(f"Sync failed: {result['message']}")
            
    except Exception as e:
        logger.error(f"Error in sync process: {str(e)}")

def main():
    """Main function to run the automation"""
    logger.info("Starting automation service")
    
    while True:
        try:
            run_sync()
            # Wait for 15 minutes before next run
            time.sleep(15 * 60)
        except KeyboardInterrupt:
            logger.info("Automation service stopped by user")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            # Wait for 1 minute before retrying in case of error
            time.sleep(60)

if __name__ == '__main__':
    main() 