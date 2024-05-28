import requests
import json
import csv
from lxml import html

# Function to get the abstract from Crossref API using XPath
def get_abstract(doi):
    base_url = 'https://api.crossref.org/works/'
    url = f'{base_url}{doi}'
    
    try:
        response = requests.get(url)
        data = json.loads(response.text)
        
        # Use XPath to extract the abstract
        abstract = data['message']['abstract']
        return abstract
    except Exception as e:
        print(f"Error fetching abstract for DOI {doi}: {e}")
        return None

# Function to read the CSV file and update with abstracts
def update_abstracts(input_csv, output_csv):
    with open(input_csv, 'r', encoding='utf-8') as infile, \
         open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['Abstract']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            doi = row['OriginalPaperDOI']
            abstract = get_abstract(doi)
            
            row['Abstract'] = abstract
            writer.writerow(row)

if __name__ == "__main__":
    input_csv_file = 'inputcss.csv'  # Update with your actual CSV file
    output_csv_file = 'outputcss.csv'  # Update with your desired output file name

    update_abstracts(input_csv_file, output_csv_file)
