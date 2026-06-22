# Stress-Strain-curve-analyzer
This project takes data for the extention of specimen and the load at which the extention occurs. It is useful for visualizing the data obtained from tensile testing of a specimen.
This program first scans for the file "Stress-Strain_data.csv" so if the data is present already one can convert it into a '.csv' file and store it as the name provided above. If not the file can be created in the program itself. The user is asked if they want to create a file. If yes the user is asked to enter the number of data to be inserted into the file. The number should be greater than 10 so as to capture the curve properly, and to calculate the Mechanical properties accurately. Then the user is asked to enter the diameter and the length of the specimen. The program then calculates the area, the modulus of elasticity and plots the stress, strain curve with the following points:
i. Proportionality limit
ii. Yield point
iii. Ultimate Strength
iv. Fracture Point
The graph is saved as a png file named Stress Strain Curve in the same folder where the initial file "Stress-Strain_data.csv" is created or found.
