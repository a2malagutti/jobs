import csv
import webbrowser
import requests
import os
from pathlib import Path

class URLProcessor:
    def __init__(self, csv_file, output_dir="downloads"):
        self.csv_file = csv_file
        self.output_dir = output_dir
        
        # Ensure the download directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def process_urls(self):
        try:
            with open(self.csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    url = row.get("Destination URL")
                    
                    if url:
                        print(f"Processing: {url}")
                        
                        # 1. Open in the default web browser
                        webbrowser.open(url)
                        
                        # 2. Save the content to disk
                        self._save_to_disk(url)
                    else:
                        print("Skipping row: 'Destination URL' column not found or empty.")
                        
        except FileNotFoundError:
            print(f"Error: The file '{self.csv_file}' was not found.")

    def _save_to_disk(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Create a filename from the URL (stripping special characters)
            filename = "".join(x for x in url if x.isalnum())[:50] + ".html"
            file_path = os.path.join(self.output_dir, filename)

            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Successfully saved to: {file_path}")

        except Exception as e:
            print(f"Failed to download {url}: {e}")

# --- Usage ---
if __name__ == "__main__":
    # Replace 'links.csv' with your actual filename
    processor = URLProcessor("links.csv")
    processor.process_urls()