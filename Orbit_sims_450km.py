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
    base_directory = "C:\\Users\\ishan\\Documents\\APSS\\Kessler\\Orbit Simulations\\gmat-sims\\450km" # Change this to your own directory of where your files are located
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
['31', 'Dec', '2022', '22:40:01.198', '31', 'Dec', '2022', '23:15:48.161', '2146.9621701', 'Earth', 'Umbra', '5668', '2163.8448385']
Maximum eclipse times: 2146.9621701

Altitude = 342km
Beta angle = 12.13

RAAN value: 15
['25', 'Apr', '2022', '22:02:12.180', '25', 'Apr', '2022', '22:02:35.257', '23.076743481', 'Earth', 'Umbra', '26', '400.34304106']
Minimum eclipse times: 23.076743481

Altitude = 455km
Beta angle = 68.69

"""







