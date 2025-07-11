import csv  # Import the csv module for reading and writing CSV files
import json  # Import the json module for working with JSON data

def csv_to_json(csv_file, json_file):
    try:
        data = []  # Initialize an empty list to store CSV rows as dictionaries
        with open(csv_file, mode='r', newline='', encoding='utf-8') as f:  # Open the CSV file for reading
            reader = csv.DictReader(f)  # Create a DictReader to read rows as dictionaries
            for row in reader:  # Iterate over each row in the CSV file
                data.append(row)  # Add each row (as a dictionary) to the data list
        with open(json_file, mode='w', encoding='utf-8') as f:  # Open the JSON file for writing
            json.dump(data, f, indent=4)  # Write the list of dictionaries to the JSON file with indentation
        print(f"Successfully converted {csv_file} to {json_file}")  # Print success message
    except FileNotFoundError:  # Handle the case where the CSV file does not exist
        print(f"Error: File {csv_file} not found.")  # Print error message
    except Exception as e:  # Handle any other exceptions
        print(f"An error occurred: {e}")  # Print the exception message

# Sample usage with sample data
def create_sample_csv(filename):
    sample_data = [  # Define a list of dictionaries as sample data
        {'name': 'Alice', 'age': '23', 'city': 'Austin'},  # First row of sample data
        {'name': 'Bob', 'age': '27', 'city': 'Dallas'},    # Second row of sample data
        {'name': 'Charlie', 'age': '22', 'city': 'Houston'}  # Third row of sample data
    ]
    with open(filename, mode='w', newline='', encoding='utf-8') as f:  # Open the CSV file for writing
        writer = csv.DictWriter(f, fieldnames=['name', 'age', 'city'])  # Create a DictWriter with fieldnames
        writer.writeheader()  # Write the header row to the CSV file
        writer.writerows(sample_data)  # Write all sample data rows to the CSV file

if __name__ == "__main__":  # Check if this script is being run directly
    sample_csv = 'sample.csv'  # Define the sample CSV file name
    sample_json = 'sample.json'  # Define the sample JSON file name
    create_sample_csv(sample_csv)  # Create a sample CSV file with sample data
    csv_to_json(sample_csv, sample_json)  # Convert the sample CSV file to a JSON file