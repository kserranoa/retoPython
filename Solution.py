import os
import csv
import re


def identify_scranton_sales_reports(folder_path):
    """
    Identifies the Scranton Sales reports and move them to a separate folder.
    """
    # Create Scranton sales reports folder
    scranton_folder = 'Scranton_Sales_Reports'

    #exist_ok= true, is a flag to skip any error if the folder already exists.
    os.makedirs(scranton_folder, exist_ok=True)

    #Number of scranton files
    scranton_files=0

    # Iterate over all files in the specified folder
    for filename in os.listdir(folder_path):

        # Check if the file is related to a salesman.
        if re.match(r'^.+_salesman\.csv$', filename):

            # Get the full path of the file
            file_path = os.path.join(folder_path, filename)

            # Extract the location information from the CSV file
            if is_scranton_sales_report(file_path):

                #Count Scranton File
                scranton_files +=1

                # Move the file to the Scranton sales reports folder
                move_file(file_path, os.path.join(scranton_folder, filename))

    print(scranton_files ,"->> Scranton reports identified \n")


def move_file(src, dest):
    """
    Moves a file from the source path to the destination path.
    """
    with open(src, 'rb') as source_file, open(dest, 'wb') as destination_file:
        destination_file.write(source_file.read())
    os.remove(src)


def is_scranton_sales_report(file_path):
    """
    Check if the sales report comes from Scranton Team.
    """
    # Check the location for each csv file.
    salesman_location = 'Scranton'

    with open(file_path, 'r') as file:

        # Read the CSV file
        reader = csv.DictReader(file)

        for row in reader:

            # Check if the 'Location' column matches the target location
            if row['Location'] == salesman_location:
                return True

    return False



def calculate_total_sales(scranton_folder):

    """
    It summarizes all the sales from Scranton and write the result in a new file.
    """

    #Initialize the variable for the total of sales.
    total_sales = 0
    # Create a new file to store the total sales
    total_sales_file = 'total_sales.txt'

    # Iterate over all files in the Scranton sales reports folder
    for filename in os.listdir(scranton_folder):

        # Get the full path of the file
        file_path = os.path.join(scranton_folder, filename)

        # Open the CSV file for reading
        with open(file_path, 'r') as file:

            # Read the CSV file
            reader = csv.DictReader(file)

            for row in reader:

                # Extract the sales value from the row (assuming it's stored in a 'Sales' column)
                sales = float(row['Sales'])

                # Add the sales value to the total
                total_sales += sales


    # Open the total_sales_file.
    with open(total_sales_file, 'w') as file:

        # Write the total sales to the file
        file.write(str(total_sales))


def get_scranton_reports():

  #Define reports path
  folder_path = '/content/Sales'

  #Extract only scranton reports
  print("Getting scranton reports...")
  identify_scranton_sales_reports(folder_path)

  #Calculate total of sales.
  print("Calculating total of sales...")
  calculate_total_sales('Scranton_Sales_Reports')

  print("Done")


get_scranton_reports()
