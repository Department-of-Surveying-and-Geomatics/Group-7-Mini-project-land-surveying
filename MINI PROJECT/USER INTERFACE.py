import csv
import math
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt

class TraverseAnalyzerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Traverse Analyzer")
        
        # File Selection
        self.file_label = tk.Label(master, text="Select Traverse Data File:")
        self.file_label.grid(row=0, column=0, padx=10, pady=5)
        self.file_entry = tk.Entry(master, width=50, state='disabled')
        self.file_entry.grid(row=0, column=1, padx=10, pady=5)
        self.browse_button = tk.Button(master, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, padx=10, pady=5)
        
        # Points Selection
        self.point1_label = tk.Label(master, text="Select Point 1:")
        self.point1_label.grid(row=1, column=0, padx=10, pady=5)
        self.point1_entry = tk.Entry(master, width=10)
        self.point1_entry.grid(row=1, column=1, padx=10, pady=5)
        
        self.point2_label = tk.Label(master, text="Select Point 2:")
        self.point2_label.grid(row=2, column=0, padx=10, pady=5)
        self.point2_entry = tk.Entry(master, width=10)
        self.point2_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # Buttons
        self.analyze_button = tk.Button(master, text="Analyze", command=self.analyze_traverse)
        self.analyze_button.grid(row=3, column=1, padx=10, pady=5)
        
    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.file_entry.config(state='normal')
            self.file_entry.delete(0, 'end')
            self.file_entry.insert(0, file_path)
            self.file_entry.config(state='disabled')
    
    def read_traverse_data(self, file_path):
        traverse_data = []
        try:
            with open(file_path, 'r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Skip header if present
                for row in csv_reader:
                    try:
                        point_number = int(row[0])
                        easting = float(row[1])
                        northing = float(row[2])
                        traverse_data.append((point_number, easting, northing))
                    except (IndexError, ValueError) as e:
                        print(f"Error parsing line: {row}, skipping...")
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found.")
        return traverse_data
    
    def analyze_traverse(self):
        file_path = self.file_entry.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a file.")
            return
        point1 = self.point1_entry.get()
        point2 = self.point2_entry.get()
        if not point1 or not point2:
            messagebox.showerror("Error", "Please enter both point numbers.")
            return
        point1 = int(point1)
        point2 = int(point2)
        traverse_data = self.read_traverse_data(file_path)
        if traverse_data:
            try:
                point1_data = next(data for data in traverse_data if data[0] == point1)
                point2_data = next(data for data in traverse_data if data[0] == point2)
                distance, bearing = self.calculate_distance_bearing(point1_data, point2_data)
                messagebox.showinfo("Traverse Analysis", f"Distance: {distance:.2f}, Bearing: {bearing:.2f} degrees")
                self.plot_traverse(traverse_data)
            except StopIteration:
                messagebox.showerror("Error", "One or both points not found in traverse data.")
        
    def calculate_distance_bearing(self, point1, point2):
        easting1, northing1 = point1[1], point1[2]
        easting2, northing2 = point2[1], point2[2]

        # Calculate distance
        distance = math.sqrt((easting2 - easting1)**2 + (northing2 - northing1)**2)

        # Calculate bearing
        delta_easting = easting2 - easting1
        delta_northing = northing2 - northing1
        bearing_rad = math.atan2(delta_easting, delta_northing)
        bearing_deg = math.degrees(bearing_rad)
        bearing = (bearing_deg + 360) % 360  # Convert bearing to range [0, 360)
        
        return distance, bearing
    
    def plot_traverse(self, traverse_data):
        eastings = [point[1] for point in traverse_data]
        northings = [point[2] for point in traverse_data]
        point_numbers = [point[0] for point in traverse_data]

        plt.figure(figsize=(8, 6))
        plt.scatter(eastings, northings)
        for i, txt in enumerate(point_numbers):
            plt.annotate(txt, (eastings[i], northings[i]))
        plt.xlabel('Easting')
        plt.ylabel('Northing')
        plt.title('Traverse Plot')
        plt.grid(True)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

def main():
    root = tk.Tk()
    app = TraverseAnalyzerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
