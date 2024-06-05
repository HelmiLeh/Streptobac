import csv
import argparse
import sys
import os

def parse_arguments():
    if "-h" in sys.argv or "--help" in sys.argv:
        print_help_message()
        sys.exit()

    parser = argparse.ArgumentParser(description="Process data from input file and export to CSV.")
    parser.add_argument("-i", "--input", type=str, help="Input file name", required=True)
    return parser.parse_args()

def print_help_message():
    help_message = """
    Usage: python extract_ncbi2table.py -i input_file
    Description: Process data from NCBI database and export to CSV.
    
    Author - Helmi Husaini Zainal Fithri
    Arguments:
      -i, --input   Input file name
    """
    print(help_message)

def preprocess_file(input_file):
    temp_file = "temp.txt"
    with open(input_file, "r") as f_in, open(temp_file, "w") as f_out:
        for line in f_in:
            if "Accession:" in line and "ID:" in line:
                f_out.write(line.replace("ID:", "\nID:"))
            else:
                f_out.write(line)
    return temp_file

def main():
    args = parse_arguments()

    # Preprocess the input file
    temp_file = preprocess_file(args.input)

    # Read data from preprocessed file
    with open(temp_file, "r") as file:
        data = file.read()

    # Split the data into individual samples
    samples = data.strip().split("\n\n")

    # Open out.csv for writing
    with open("out.csv", "w", newline='') as csvfile:
        # Create a CSV writer object
        csvwriter = csv.writer(csvfile)
        
        # Write header row
        csvwriter.writerow(["Accession", "Host", "Host Description", "Host Disease", "Host Sex", "Geographic Location", "Isolate", "Strain", "Isolation Source", "Serotype"])
        
        # Loop through each sample and extract required information
        for sample in samples:
            host = ""
            host_description = ""
            host_disease = ""
            host_sex = ""
            geographic_location = ""
            isolate = ""
            accession = ""  
            strain = ""
            isolation_source = ""
            serotype = ""
            
            lines = sample.strip().split("\n")
            for line in lines:
                if line.startswith("Accession:"):
                    accession_info = line.split(":")[1].strip()
                    accession = accession_info.split()[0].strip()
                elif line.startswith("    /host="):
                    host = line.split("=")[1].strip('"')
                elif line.startswith("    /host description="):
                    host_description = line.split("=")[1].strip('"')
                elif line.startswith("    /host disease="):
                    host_disease = line.split("=")[1].strip('"')
                elif line.startswith("    /host sex="):
                    host_sex = line.split("=")[1].strip('"')
                elif line.startswith("    /geographic location="):
                    geographic_location = line.split("=")[1].strip('"')
                elif line.startswith("    /isolate="):
                    isolate = line.split("=")[1].strip('"')
                elif line.startswith("    /strain="):
                    strain = line.split("=")[1].strip('"')  
                elif line.startswith("    /isolation source="):
                    isolation_source = line.split("=")[1].strip('"')  
                elif line.startswith("    /serotype="):
                    serotype = line.split("=")[1].strip('"')
            
            # Write extracted information to out.csv
            csvwriter.writerow([accession, host, host_description, host_disease, host_sex, geographic_location, isolate, strain, isolation_source, serotype])

    # Remove the temporary file
    os.remove(temp_file)

if __name__ == "__main__":
    main()

