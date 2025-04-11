import os
import time
import schedule
import logging
from dotenv import load_dotenv
from coda_api import CodaAPI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_automation():
    """Run the sentence count sync automation."""
    try:
        logger.info("Starting automation run...")
        coda = CodaAPI(os.getenv('CODA_API_TOKEN'))
        result = coda.sync_clients_sentence_counts()
        logger.info(f"Automation completed. Results: {result}")
    except Exception as e:
        logger.error(f"Error in automation run: {str(e)}")

def main():
    """Main function to run the scheduled automation."""
    # Load environment variables
    load_dotenv()
    
    # Schedule the automation to run every minute
    schedule.every(1).minutes.do(run_automation)
    
    # Run the automation immediately on startup
    run_automation()
    
    logger.info("Automation scheduler started. Running every minute...")
    
    # Keep the script running
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Automation scheduler stopped by user")
            break
        except Exception as e:
            logger.error(f"Error in scheduler: {str(e)}")
            time.sleep(60)  # Wait a minute before retrying

if __name__ == '__main__':
    main() 