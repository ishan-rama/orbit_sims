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
    base_directory = "C:\\Users\\ishan\\Documents\\APSS\\Kessler\\Orbit Simulations\\gmat-sims\\400km" #Change this to your own directory of where your files are located
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


    # Combine the values and indices into a single iterable
    combined = zip(eclipse_times, indicies)

    # Sort the combined iterable based on the values
    sorted_combined = sorted(combined, reverse= True)

    # Separate the sorted values and indices
    sorted_values, sorted_indices = zip(*sorted_combined)

    print(eclipse_vals[indicies[max_index]])
    print(f"Maximum eclipse times: {max_eclipse_times}")
    print(eclipse_vals[indicies[min_index]])
    print(f"Minimum eclipse times: {min_eclipse_times}\n")


def get_cut_off_date(number):
    '''
    Finds max umbra eclipse and prints the time 
    '''
    file_links = get_links(number)
    RAAN = file_links[0]["raan"]
    [report_headers, report_vals] = get_report_data(file_links[3])

    for index, val in enumerate(report_vals):
        if float(val[6]) < 350:
            print(RAAN)
            print(report_vals[index])
            return report_vals[index]
        

def min_eclipse_time(number, cutoff):
    file_links = get_links(number)
    RAAN = file_links[0]["raan"]
    [eclipse_headers, eclipse_vals] = get_eclipse_data(file_links[2])

    cutoff_day = int(cutoff[0])
    allowable_months = ['Jan', 'Feb', 'Mar', 'Apr']

    max_eclipse_val = 0 
    max_eclipse_time = 0
    ##START HERE< GO THROUGH EACH VAL AND FIND MIN THAT MEETS REQUIREMENT THAT IT IS BEFORE CUT OFF
    for val in eclipse_vals:
        if (val[10] == "Umbra") and (float(val[8]) > max_eclipse_time) and (val[1] in allowable_months) and (int(val[0]) <= cutoff_day):
            max_eclipse_val = val
            max_eclipse_time = float(val[8])
        
    print(RAAN)
    print(max_eclipse_val)

    return


numbers = list(range(1,13))
cut_off_dates = []

for num in numbers:
    cut_off_dates.append(get_cut_off_date(num))

for index, num in enumerate(numbers):
    min_eclipse_time(num, cut_off_dates[index])

'''

################################################################
#RESULTS
################################################################

RAAN value: 105
['06', 'Apr', '2022', '23:49:54.273', '07', 'Apr', '2022', '00:25:49.352', '2155.0787509', 'Earth', 'Umbra', '1502', '2171.4381114']
Maximum eclipse times: 2155.0787509

Altitude = 362km
Beta angle = -4.3

RAAN value: 30
['25', 'Jan', '2022', '23:17:59.945', '25', 'Jan', '2022', '23:18:26.301', '26.356574753', 'Earth', 'Umbra', '390', '401.85484984']
Minimum eclipse times: 26.356574753

Altitude = 395km
Beta angle = 70.11

'''




