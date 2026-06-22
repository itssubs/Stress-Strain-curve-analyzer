import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import sys
#input validation
def get_validated_input(prompt, cast_type, condition, error_msg ):
    while True:
        try:
            value = cast_type(input(prompt))
            if condition(value):
                return value
            else:
                print(error_msg)
                continue
        except ValueError:
            print(f"Please enter a valid {cast_type.__name__}.")

#define stress and strain
strain = []
stress = []
#Checking for the existance of file creating one if not found
if not os.path.exists("Stress-Strain_data.csv"):
    print("The file cannot be found.")
    while True:
        choice = input("Do you want to create the file (Y/N)?: ")
        if choice.lower() == 'y':
            no_of_data = get_validated_input("Enter the number of data to be inserted: ", int, lambda v: v >= 10, "Enter number greater than or equals to 10")
            with open("Stress-Strain_data.csv", 'w', newline = '')as file:
                writer = csv.writer(file)
                writer.writerow(['Data Point', 'Extension (mm)', 'Load (kN)'])
                for i in range(no_of_data):
                    extension = get_validated_input("Enter the extension in mm: ", float, lambda v: v >= 0, "Enter number greater than or equals to 0")
                    load = get_validated_input("Enter the load in kN: ", float, lambda v: v >= 0, "Enter number greater than or equals to 0")
                    writer.writerow([i+1, extension, load])
            break
        elif choice.lower() == 'n':
            print("Program Terminated")
            sys.exit()
        else: 
            print("Please only enter y or n")
        

with open("Stress-Strain_data.csv", 'r')as file:
    next(file)
    content = csv.reader(file)
    diameter = get_validated_input("Enter the diameter of the specimen in mm: ", float, lambda v: v > 0, "Enter number greater than 0")
    area = (np.pi * (diameter ** 2)) / 4
    length = get_validated_input("Enter the length of the specimen in mm: ", float, lambda v: v > 0, "Enter number greater than 0")
    for row in content:
        row[1] = float(row[1]) #Conversion of extension from string to float 
        row[2] = float(row[2]) #Conversion of load from string to float 
        strain.append(row[1] / length)
        stress.append(row[2]*1000 / area)
    #Conversion to numpy array
    strain = np.array(strain)
    stress = np.array(stress)

    #Calculation of slope for proportionality limit
    slope = np.diff(stress) / np.diff(strain)
    ref_slope = np.mean(slope[:3])
    tol = 0.05 #5% tolerance for proportionality index
    limit_index = np.where(np.abs(slope - ref_slope) / ref_slope > tol)[0][0] + 1
    limit_strain = strain[limit_index]
    limit_stress = stress[limit_index]
    
    #Calculation of modulus of elasticity
    elastic_strain = strain[:limit_index]
    elastic_stress = stress[:limit_index]
    coeff = np.polyfit(
        elastic_strain,
        elastic_stress,
        1
    )
    E = coeff[0] #modulus of elasticity
    print(f"Modulus of Elasticity: {E:.2f} MPa")
    
    #Calculation for yield point
    offset_stress = E * (strain - 0.002) + coeff[1]
    difference = stress - offset_stress
    yield_index = np.where(np.diff(np.sign(difference)))[0][0]
    yield_strain = strain[yield_index]
    yield_stress = stress[yield_index]

    #Fracture point
    fracture_strain = strain[-1]
    fracture_stress = stress[-1]

    #Graph plots
    plt.plot(strain,stress, color = "#FBFF04", linewidth = 2, label = "Stress Strain Curve") #Main Stress Strain curve
    plt.plot(limit_strain, limit_stress, 'bo', label = "Proportional Limit")
    plt.plot(yield_strain, yield_stress, 'go', markersize = 8, label = 'Yield Point')
    plt.plot(strain[5:yield_index + 2], offset_stress[5:yield_index + 2], linestyle = ":", color = 'orange', label = '0.2% Offset')
    plt.axhline(stress.max(), color = 'green', linestyle = ':', label = "Ultimate Strength")
    plt.plot(fracture_strain, fracture_stress, 'rx', markersize = 10, markeredgewidth = 2, label = "Fracture Point")
    plt.xlabel("Strain")
    plt.ylabel("Stress in MPa")
    plt.title("Stress-Strain Curve") 
    plt.legend()
    plt.grid(True)
    plt.savefig(r"Stress Strain Curve.png", dpi = 300, bbox_inches = 'tight')
    plt.show()
    
    
