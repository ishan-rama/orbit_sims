import json
import os
from decimal import Decimal

def get_links(file_number):
    '''
    Returns links to param.json, contact, eclipse and report txt data files
    '''

    json_filename = f"param{file_number}.json"

    # Open the JSON file
    with open(json_filename) as json_file:
        data = json.load(json_file)  # Parse the JSON data

    # Extract the links from the JSON data
    contact_link = data['contact']
    eclipse_link = data['eclipse']
    report_link = data['report']

    contact_link = modify_link(contact_link)
    eclipse_link = modify_link(eclipse_link)
    report_link = modify_link(report_link)

    return [data, contact_link, eclipse_link, report_link]

def modify_link(link): 
    '''
    This function makes sure you can access the links based on the locations of files in your directory
    '''
    base_directory = "C:\\Users\\ishan\\Documents\\APSS\\Kessler\\Orbit Simulations\\gmat-sims\\500km" #Change this to your own directory of where your files are located
    link = link.replace('\\', '/')  # Replace backslashes with forward slashes
    new_link = os.path.join(base_directory, os.path.basename(link))

    return new_link

def get_eclipse_data(file_link):
    '''
    Returns a list of headers, and an array of values for eclipse.txt
    '''
    #Open the text file
    with open(file_link, 'r') as file:
        # Read the header line
        header = file.readline().split()
    
    # Skip the first three lines
        for _ in range(3):
            next(file)


    # Read the values
        values = []
        for line in file:
            line_values = line.split()
            values.append(line_values)

    # Remove the last 5 lines from the values list
    values = values[:-7]

    return [header, values]

def get_report_data(file_link):
    '''
    Returns a list of headers, and an array of values for report.txt
    '''
    #Open the text file
    with open(file_link, 'r') as file:
        # Read the header line
        header = file.readline().split()

    # Read the values
        values = []
        for line in file:
            line_values = line.split()
            values.append(line_values)

    return [header, values]

def get_max_eclipse(number):
    '''
    Finds max umbra eclipse and prints the time 
    '''
    file_links = get_links(number)
    RAAN = file_links[0]["raan"]
    [eclipse_headers, eclipse_vals] = get_eclipse_data(file_links[2])

    #get max and min eclipses
    eclipse_types = [row[10] for row in eclipse_vals]

    eclipse_times = []
    index = 0
    indicies = []

    for eclipse_type in eclipse_types:
        if eclipse_type == "Umbra":
            eclipse_times.append(float(eclipse_vals[index][8]))
            indicies.append(index)
        index += 1

    max_eclipse_times = max(eclipse_times)
    max_index = eclipse_times.index(max_eclipse_times)
    min_eclipse_times = min(eclipse_times)
    min_index = eclipse_times.index(min_eclipse_times)

    print(f"RAAN value: {RAAN}")
    print(eclipse_vals[indicies[max_index]])
    print(f"Maximum eclipse times: {max_eclipse_times}")
    print(eclipse_vals[indicies[min_index]])
    print(f"Minimum eclipse times: {min_eclipse_times}\n")


numbers = list(range(1,13))

for num in numbers:
    get_max_eclipse(num)

"""
################################################################
#RESULTS
################################################################

RAAN value: 90
['21', 'May', '2022', '01:47:38.587', '21', 'May', '2022', '02:23:01.836', '2123.2497949', 'Earth', 'Umbra', '2137', '2131.6070975']
Maximum eclipse times: 2123.2497949

Altitude = 520km
Beta angle = 7.94

RAAN value: 0
['19', 'Aug', '2022', '05:25:38.109', '19', 'Aug', '2022', '05:25:59.379', '21.270393895', 'Earth', 'Umbra', '1815', '389.88410910']
Minimum eclipse times: 21.270393895

Altitude = 502.5km
Beta angle = 67.67

"""







