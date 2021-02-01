# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 00:12:31 2021

@author: kartik
"""
from Drone_Design import *

Weight_Total =  4
Wing_Span = 2.5
Payload = 0.6
Altitude = 2500
Flight_Velocity = 16
Reynold_Number = 250000
Taper = 0.6

DD = DroneDesignToolbox(Weight_Total, Wing_Span, Payload, 
                        Altitude, Flight_Velocity, 
                        Reynold_Number, Taper)

Wing_Choice = pd.concat([DD.Calc_Dynamic_Pressure(), DD.Calc_Wing_Dimensions(), DD.Calc_Performance_Coefficients()], axis = 1)

b = Wing_Choice.iloc[:,5].values[0]*100 # Wing Span in cm
MAC = Wing_Choice.iloc[:,8].values[0]*100 
R = Wing_Choice.iloc[:,10].values[0]*100
T = Wing_Choice.iloc[:,11].values[0]*100
AC = Wing_Choice.iloc[:,13].values[0]*100

# Define Sweep and Static Margin
Sweep_Length = 10 # In cm
Static_Margin = 5 # As percentage

def Calculate_Frame_Coordinates(Sweep_Length, Static_Margin):
    
    Tail_Point = (0,0) #(XY) (All dimensions are calculated with this as start and in anticlockwise direction)
    L1 = (Tail_Point[1] + R - Sweep_Length - T)
    L2 = (Tail_Point[1] + R - Sweep_Length)
    X = [Tail_Point[0], b/2, b/2, Tail_Point[0], -b/2, -b/2, Tail_Point[0]]
    Y = [Tail_Point[0], L1, L2, (Tail_Point[1] + R), L2, L1, Tail_Point[0]]
    
    return X,Y

def Calculate_MAC_Coordinates(b, R, T, X_Frame, Y_Frame):
    
    # Using the line eqn y = mx + b we find intersecting points 
    # for the MAC to wing frame
    
    x = b/6*((R + 2*T)/(R + T)) # X coordinate (Centre Spanwise Location)
    U_R_Y = ((Y_Frame[3] - Y_Frame[2])/(X_Frame[3] - X_Frame[2]))*x + Y_Frame[3]
    L_R_Y = ((Y_Frame[0] - Y_Frame[1])/(X_Frame[0] - X_Frame[1]))*x + Y_Frame[0]
    U_L_Y = ((Y_Frame[3] - Y_Frame[4])/(X_Frame[3] - X_Frame[4]))*(-x) + Y_Frame[3]
    L_L_Y = ((Y_Frame[0] - Y_Frame[5])/(X_Frame[0] - X_Frame[5]))*(-x) + Y_Frame[0]
    
    Y_MAC_R = [U_R_Y, L_R_Y]
    Y_MAC_L = [U_L_Y, L_L_Y]
    
    X_MAC_R = [x, x]
    X_MAC_L = [-x, -x]
    return X_MAC_L, X_MAC_R, Y_MAC_L, Y_MAC_R

fig = plt.figure(figsize = (15, 10))
ax = fig.add_subplot(111, aspect = 'equal')

scale_x = b*0.6
scale_y = b*0.4
ax.set_xlim([-scale_x, scale_x])
ax.set_ylim([-scale_y*0.2, scale_y])

# Plot Wing Frame
X_Frame, Y_Frame = Calculate_Frame_Coordinates(Sweep_Length, Static_Margin)
plt.plot(X_Frame, Y_Frame, linewidth = 6, color = 'teal')

# Plot MAC
X_MAC_L, X_MAC_R, Y_MAC_L, Y_MAC_R = Calculate_MAC_Coordinates(b, R, T, X_Frame, Y_Frame)
plt.plot(X_MAC_L, Y_MAC_L, linewidth = 2, color = 'red', linestyle = 'dashed', label = f'Mean Aerodynamic Chord {round(MAC, 2)} cm @ {round(X_MAC_R[0], 2)} cm')
plt.plot(X_MAC_R, Y_MAC_R, linewidth = 2, color = 'red', linestyle = 'dashed')

# Plot Aerodynamic Centre and Centre of Gravity
Y_AC_Point = Y_Frame[3] - AC
X_AC = [X_MAC_L, X_MAC_R]
Y_AC = [Y_AC_Point, Y_AC_Point]
plt.plot(X_AC, Y_AC, linewidth = 2, color = 'black', linestyle = 'dashed')
plt.scatter(0, Y_AC_Point, color = 'blue', s = 100, label = f'Aerodynamic Centre: {round(AC, 2)} cm')

CG = AC - (AC * Static_Margin / 100)
Y_CG_Point = Y_Frame[3] - CG
plt.scatter(0, Y_CG_Point, color = 'orange', s = 100, label = f'Centre of Gravity: {round(CG, 2)} cm')

plt.plot()
plt.legend()
plt.grid()
plt.show()
    