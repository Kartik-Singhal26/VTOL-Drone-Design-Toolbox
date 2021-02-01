# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 23:46:01 2021

@author: kartik
"""
import pandas as pd
import numpy as np
import math as m
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random 
import decimal

# Define all known variables here
Density = 1.00649 # Corresponding to Altitude
mu = 0.00001789 #Dynamic Viscosity of Air at Sea level in Pa·s
Air_Kinematic_Viscosity = 0.00001470
P0 = 1.225 # Air density at sea level

class DroneDesignToolbox:
    def __init__(self, Weight_Total, Wing_Span, Payload, Altitude, Flight_Velocity, Reynold_Number, Taper):
        self.Weight_Total = Weight_Total
        self.Wing_Span = Wing_Span
        self.Payload = Payload
        self.Altitude = Altitude
        self.Flight_Velocity = Flight_Velocity
        self.Reynold_Number = Reynold_Number
        self.Taper = Taper
        self.Velocity = Flight_Velocity

    # Calculate Dynamic Pressure Value
    
    def Calc_Dynamic_Pressure(self):
        self.dynamic_pressure = Density*(self.Velocity**2)*0.5
        self.Q = [{'Altitude': self.Altitude, 'Density': Density, 'Target Velocity': self.Velocity, 'Dynamic Pressure': self.dynamic_pressure}]
    
        return pd.DataFrame(self.Q)

    # Calculate Wing Dimension Parameters 

    def Calc_Wing_Dimensions(self):
    
        self.Lift = 1.20 * self.Weight_Total # 20% Factor    
        self.Mean_Chord_Length = (mu * self.Reynold_Number)/(Density * self.Velocity) # Mean Aerodynamic Chord
                          
        # Wing Dimensions Parameters
        self.Wing_root_chord = self.Mean_Chord_Length * (3/2) / ((1 + self.Taper + self.Taper ** 2) / (1 + self.Taper)) 
        self.Wing_tip_chord = self.Taper * self.Wing_root_chord
        self.Area = self.Wing_root_chord * (self.Wing_Span * (1 + self.Taper)) / 2 
        self.Aerodynamic_Centre = 0.25 * self.Mean_Chord_Length
            
        # Wing Performance Parameters (These parameters are important for aerofoil selection)
        self.Aspect_Ratio = (self.Wing_Span ** 2) / self.Area
        self.Wing_Loading = self.Weight_Total / self.Area
            
        # Update the Database       
        self.wing_dim = {'Reynold\'s Number': self.Reynold_Number,
                         'Wing Span': self.Wing_Span, 'Total Weight': self.Weight_Total, 'Lift': self.Lift,
                         'Mean Chord Length': self.Mean_Chord_Length, 'Taper Value': self.Taper,
                         'Wing Root Chord': self.Wing_root_chord, 'Wing Tip Chord': self.Wing_tip_chord,
                         'Wing Area': self.Area, 'Aerodynamic Centre': self.Aerodynamic_Centre,
                         'Aspect Ratio': self.Aspect_Ratio, 'Wing Loading Ratio': self.Wing_Loading}
            
        return pd.DataFrame(self.wing_dim, index = [0])

    # Calculate Performance Coefficients    

    def Calc_Performance_Coefficients(self):
        
        # Ideal Lift Coefficients
        self.Ideal_Cruise_Lift_Coeff = 2 *self.Weight_Total / (Density * (self.Velocity**2) * self.Area)
        self.Wing_Cruise_Lift_Coeff = self.Ideal_Cruise_Lift_Coeff * (1/0.95)
        self.Wing_Aerofoil_Ideal_Lift_Coeff = self.Wing_Cruise_Lift_Coeff * (1/0.9)
           
        self.Stall_Speed = m.sqrt((self.Wing_Loading * 2)/(P0 * self.Ideal_Cruise_Lift_Coeff))
    
        # Maximum Lift Coefficients
        self.Max_Lift_Coefficient = 2 * self.Lift / (P0 * (self.Stall_Speed ** 2) * self.Area)
        self.Wing_Max_Lift_Coeff = self.Max_Lift_Coefficient * (1/0.95)
        self.Wing_Airfoil_Gross_Max_Lift_Coeff = self.Wing_Max_Lift_Coeff * (1/0.9)
        
        # Update the Database
        self.perf_coeff = {'Ideal Cruise Lift Coefficent': self.Ideal_Cruise_Lift_Coeff, 
                      'Wing Cruise_Lift Coefficeint': self.Wing_Cruise_Lift_Coeff, 
                      'Wing Aerofoil Ideal Lift Coefficient': self.Wing_Aerofoil_Ideal_Lift_Coeff,
                      'Maximum Lift Coefficient': self.Max_Lift_Coefficient, 
                      'Maximum Wing Lift Coefficient': self.Wing_Max_Lift_Coeff,
                      'Maximum Gross Wing Airfoil Lift Coefficient': self.Wing_Airfoil_Gross_Max_Lift_Coeff, 
                      'Stall Speed': self.Stall_Speed}
        
        return pd.DataFrame(self.perf_coeff, index = [0])
    