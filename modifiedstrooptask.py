from psychopy import core, visual, event
import random 
import pandas as pd 

#assessments = [fixation_on, fixation_off, stimuli_on, stimuli_off, reaction_speed]
experiment_clock = core.Clock()
def display_instructions():
    instruction_text = " " 
    instructions = visual.TextStim(win, text = instruction_text)
win = visual.Window(size=(800,600), color='grey', units='pix')
color_translations = {"red" : "紅", "blue" :"藍", "green" : "綠", "brown" : "棕"}
color_chinese = ["紅", "藍", "綠"]
color_english = ["red", "blue", "green"]
experiment_data = []

pairings = []
for i in color_chinese: 
    for j in color_english: 
        pairings.append((i,j))
random.shuffle(pairings) 
def display_stimuli():
    for i in range(9):
        #blank screen before fixation
        win.flip()
        core.wait(0.5) 
        #display fixation
        fixation_onset = experiment_clock.getTime() 
        fixation_cross = visual.TextStim(win, text='+', height=40, color='black')
        fixation_cross.draw()
        win.flip()
        core.wait(0.5)
        fixation_offset = experiment_clock.getTime() 
        
        #display stimuli 
        correct_color = random.choice(color_english) 
        test = visual.TextStim(win, text = random.choice(color_chinese), height = 60, color = correct_color) 
        test.draw()
        win.flip(clearBuffer = False)
        stimulus_onset = experiment_clock.getTime()
        #waiting for response 
        response = event.waitKeys(keyList=['r', 'g', 'b'], timeStamped=experiment_clock)
        if response: 
            data = {
                    "response_key" : response[0][0], 
                    "correct" : response[0][0] == correct_color 
                    "fixation_onset" : fixation_onset
                    "fixation_offset" : fixation_offset 
                    "stimulus_onset": stimulus_onset,
                    "response_time" : response[0][1], 
                    }
            experiment_data.append(data)
                    
            
            
        

experiment_clock.reset() 
display_stimuli()



