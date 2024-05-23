import csv
import os
import math
import matplotlib.pyplot as plt

def read_traverse_data(file_path):
    data = []
    
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"Error: The file {file_path} does not exist.")
        return data

    try:
        # Read the CSV file
        with open(file_path, mode='r', newline='') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Read the header row
            
            # Validate the CSV file format
            if len(header) != 3 or header != ['Point', 'Easting', 'Northing']:
                print("Error: CSV file format is incorrect. Expected columns: 'Point', 'Easting', 'Northing'.")
                return data
            
            # Parse the data
            for row in csv_reader:
                try:
                    point_number = int(row[0])
                    easting = float(row[1])
                    northing = float(row[2])
                    data.append((point_number, easting, northing))
                except ValueError as e:
                    print(f"Error: Invalid data format in row: {row}. Error: {e}")
    except Exception as e:
        print(f"Error: An error occurred while reading the file. Error: {e}")
    
    return data

def calculate_traverse_characteristics(data):
    if not data:
        return None
    
    num_points = len(data)
    eastings = [point[1] for point in data]
    northings = [point[2] for point in data]
    
    min_easting = min(eastings)
    max_easting = max(eastings)
    min_northing = min(northings)
    max_northing = max(northings)
    
    return num_points, min_easting, max_easting, min_northing, max_northing

def distance_and_bearing(point1, point2):
    delta_easting = point2[1] - point1[1]
    delta_northing = point2[2] - point1[2]
    
    distance = math.sqrt(delta_easting**2 + delta_northing**2)
    
    if delta_northing == 0:
        bearing = 90 if delta_easting > 0 else (270 if delta_easting < 0 else None)
    else:
        angle = math.degrees(math.atan(abs(delta_easting / delta_northing)))
        if delta_easting >= 0 and delta_northing > 0:
            bearing = angle
        elif delta_easting >= 0 and delta_northing < 0:
            bearing = 180 - angle
        elif delta_easting < 0 and delta_northing < 0:
            bearing = 180 + angle
        else:
            bearing = 360 - angle
    
    return distance, bearing

def visualize_traverse(data):
    if not data:
        print("No data to visualize.")
        return
    
    # Extract coordinates and point numbers
    point_numbers = [point[0] for point in data]
    eastings = [point[1] for point in data]
    northings = [point[2] for point in data]
    
    # Create scatter plot
    plt.figure(figsize=(8, 6))
    plt.scatter(eastings, northings, c='b', marker='o')
    
    # Annotate each point with its corresponding point number
    for i, point in enumerate(data):
        plt.annotate(point[0], (point[1], point[2]), textcoords="offset points", xytext=(0,5), ha='center')
    
    plt.title('Traverse Visualization')
    plt.xlabel('Easting')
    plt.ylabel('Northing')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    file_path = 'traverse_data.csv'  # Replace with the path to your CSV file
    traverse_data = read_traverse_data(file_path)
    
    if traverse_data:
        print("Traverse data successfully read:")
        for point in traverse_data:
            print(point)
        
        num_points, min_easting, max_easting, min_northing, max_northing = calculate_traverse_characteristics(traverse_data)
        print(f"\nTotal number of points: {num_points}")
        print(f"Minimum Easting: {min_easting}")
        print(f"Maximum Easting: {max_easting}")
        print(f"Minimum Northing: {min_northing}")
        print(f"Maximum Northing: {max_northing}")
        
        visualize_traverse(traverse_data)
    else:
        print("No valid data found.")

if __name__ == "__main__":
    main()
