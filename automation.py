import os
import time
from codaio import Coda  # Assuming you have installed codaio and set it up

# Initialize the coda client with your API token
CODA_API_TOKEN = os.getenv("CODA_API_TOKEN")
coda = Coda(api_key=CODA_API_TOKEN)

# Constants for the main Clients table
MAIN_DOC_ID = "9omNdUhI4j"           # Main document ID containing the Clients table
CLIENTS_TABLE_ID = "grid-PZqFjHZRk_"   # Clients table ID

# Column IDs for the Clients table
COL_FIRST_NAME          = "c-B5jqLzoe_x"
COL_LAST_NAME           = "c-_WlEd-pWCg"
COL_CLIENT_DOC_ID       = "c-jJ9R5VVvz0"  # The student's document ID
COL_SENTENCES_TABLE     = "c-oN98cuRpc1"  # The student's sentences table ID
COL_NUM_SENTENCES       = "c-JfGAyru56_"  # The column to update with the count
COL_DOC_URL             = "c-5b3Ye-Mf5S"   # The URL to the student's document (not used here)

def retry_with_backoff(func, max_retries=3, initial_delay=1):
    """Retry a function with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:  # Last attempt
                raise e
            delay = initial_delay * (2 ** attempt)  # Exponential backoff
            print(f"Attempt {attempt + 1} failed. Retrying in {delay} seconds...")
            time.sleep(delay)

def sync_clients_sentence_counts():
    # Retrieve the main Clients table data
    try:
        clients_data = retry_with_backoff(lambda: coda.get_table(doc_id=MAIN_DOC_ID, table_id_or_name=CLIENTS_TABLE_ID))
    except Exception as e:
        print(f"Error fetching Clients table after retries: {e}")
        return

    # Iterate through each row in the Clients table
    for row in clients_data.get("rows", []):
        row_id = row.get("id")
        values = row.get("values", {})

        # Get the student's document ID and their sentences table ID from the row values.
        student_doc_id = values.get(COL_CLIENT_DOC_ID)
        sentences_table_id = values.get(COL_SENTENCES_TABLE)

        if not sentences_table_id:
            print(f"Row {row_id} missing sentences_table_id. Skipping.")
            continue

        if not student_doc_id:
            print(f"Row {row_id} missing client_doc_id. Skipping.")
            continue

        # Fetch the student's sentences table data from their document
        try:
            sentences_data = retry_with_backoff(lambda: coda.get_table(doc_id=student_doc_id, table_id_or_name=sentences_table_id))
        except Exception as e:
            print(f"Row {row_id}: Error fetching sentences table for doc {student_doc_id}: {e}")
            continue

        # Count the number of rows (each row represents a sentence)
        sentence_count = len(sentences_data.get("rows", []))
        print(f"Row {row_id}: Found {sentence_count} sentences.")

        # Prepare the payload to update the 'num_sentences' column in the Clients table
        update_payload = {
            "row": {
                "cells": [
                    {"column": COL_NUM_SENTENCES, "value": sentence_count}
                ]
            }
        }

        # Update the client's row in the main Clients table
        try:
            retry_with_backoff(lambda: coda.update_row(
                doc_id=MAIN_DOC_ID,
                table_id_or_name=CLIENTS_TABLE_ID,
                row_id_or_name=row_id,
                data=update_payload
            ))
            print(f"Row {row_id} updated: num_sentences set to {sentence_count}.")
        except Exception as e:
            print(f"Row {row_id}: Error updating num_sentences: {e}")

# For a manual trigger, you might use the following function in a Flask endpoint.
def manual_update_trigger():
    sync_clients_sentence_counts()
    return {"status": "update complete"}

# Example: Run a manual update (or you could tie this to a route in your Flask app)
if __name__ == '__main__':
    manual_update_trigger() 