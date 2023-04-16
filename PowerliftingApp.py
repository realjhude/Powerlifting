import math
import pickle
import os
import json
import datetime as dt
import PySimpleGUI as sg

dataMap = {}

current_date = dt.date.today()
def one_rep_max(weight, reps):
    return weight * (1 + reps / 30)

def lbs_to_kg(lbs):
    return lbs * 0.453592

def kg_to_lbs(kg):
    return kg * 2.205

def calculate_1rm(weight_unit, squat, deadlift, bench_press, reps):
    try:
        squat, deadlift, bench_press, reps = float(squat), float(bench_press), float(deadlift), int(reps)
    except ValueError:
        return "Invalid input, please enter a number for all lifts"
    
    if weight_unit.lower() == "kg":
        squat = kg_to_lbs(squat)
        deadlift = kg_to_lbs(deadlift)
        bench_press = kg_to_lbs(bench_press)
        weight_unit = "lbs"
    elif weight_unit.lower() == "lbs":
        squat = lbs_to_kg(squat)
        deadlift = lbs_to_kg(deadlift)
        bench_press = lbs_to_kg(bench_press)
        weight_unit = "kg"
        
    elif weight_unit.lower() != "lbs" and weight_unit.lower() != "kg":
        return "Invalid weight unit"
    
    squat_1rm = one_rep_max(squat, reps)
    deadlift_1rm = one_rep_max(deadlift, reps)
    bench_press_1rm = one_rep_max(bench_press, reps)

    return f"S-: {squat_1rm:.2f} {weight_unit}\nB-: {bench_press_1rm:.2f} {weight_unit}\nD-: {deadlift_1rm:.2f} {weight_unit}"
    
    
   
    
    
    
sg.theme('Black')
primary_color = '#ffffff'
secondary_color = '#000000'
    
layout = [
    [sg.Text('Lift Converter', font=('Signore', 20), justification='center', size=(40, 1))],
    [sg.Text('Enter weight unit:', font=('Signore', 14)), sg.Combo(['kg', 'lbs'], key='_WEIGHT_UNIT_', font=('Signore', 14))],
    [sg.Text('Enter squat:', font=('Signore', 14)), sg.InputText(key='_SQUAT_', font=('Signore', 14))],
    [sg.Text('Enter bench:', font=('Signore', 14)), sg.InputText(key='_BENCH_PRESS_', font=('Signore', 14))],
    [sg.Text('Enter deadlift:', font=('Signore', 14)), sg.InputText(key='_DEADLIFT_', font=('Signore', 14))],
   
    [sg.Button('Calculate', button_color=(primary_color, secondary_color), font=('Signore', 14)), sg.Button('Clear', button_color=(primary_color, secondary_color), font=('Signore', 14))],
    [sg.Multiline(size=(20, 5), disabled=True, key='_OUTPUT_')],
    [sg.Button('Add Sets',button_color=(primary_color, secondary_color), font=('Signore', 14))]
]

layout2 = [
    [sg.Text('Add Sets', font=('Signore', 20), justification='center', size=(40, 1))],
    [sg.Text('Lift:', font=('Signore', 14)), sg.InputText(key='_LIFT_', font=('Signore', 14))],
    [sg.Text('Reps:', font=('Signore', 14)), sg.InputText(key='_REPS_', font=('Signore', 14))],
    [sg.Text('RPE:', font=('Signore', 14)), sg.Combo( ['1','2','3','4','5','6','7','8','9','10'], key='_RPE_',font=('Signore', 14))],
    [sg.Button('Save', button_color=(primary_color, secondary_color), font=('Signore', 14))]
]
lift2ndWindow = '_LIFT_'


window = sg.Window("Fit", layout)


while True:
    event, values = window.read()

    if event == "Calculate":
        result = calculate_1rm(values['_WEIGHT_UNIT_'], values['_SQUAT_'], values['_BENCH_PRESS_'], values['_DEADLIFT_'] ,reps=1)
        print(current_date)
        print(result)
        window['_OUTPUT_'].update(result)
        
        
        
        output_str = ""
        if isinstance(result, dict):
            for lift, weight in result.items():
                output_str += f"{lift}: {weight}  {values['_WEIGHT_UNIT_']}\n"
        else:
            output_str = result
            with open('dataForApp.json', 'a') as f:
                f.write("\n" + "" + str(current_date) + "\n")
                f.write(output_str)
                
           
 



    elif event == "Clear":
        window['_SQUAT_'].update('')
        window['_DEADLIFT_'].update('')
        window['_BENCH_PRESS_'].update('')
        window['_OUTPUT_'].update('')
        
    if event in (None, "Exit"):
        break
        
    if event == "Add Sets":
        window = sg.Window("Fit",layout2)

        while True:
            event, values = window.read()

            saveSets = values['_REPS_'], values['_LIFT_'], values['_RPE_'], reps = 1
            
    if event == "Save":
        output_str += f"{'_REPS_'}: {'_RPE_'}  {values['_LIFT_']}\n"

window.close()
