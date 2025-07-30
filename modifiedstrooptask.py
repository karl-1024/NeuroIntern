from psychopy import core, visual, event, gui 
import random 
import pandas as pd 

#assessments = [fixation_on, fixation_off, stimuli_on, stimuli_off, reaction_speed]

info = {'Subject ID (type manually):': ''}
dlg = gui.DlgFromDict(dictionary=info, title='Experimenter Input')
if dlg.OK:
    subject_id = info['Subject ID (type manually):']
else:
    core.quit()
experiment_clock = core.Clock()
win = visual.Window(size=(800,600), color='grey', units='pix')
def display_instructions():
    instruction_text = ("在這個遊戲中，您將看到顏色詞語（紅色，藍色，綠色）逐一出現。\n\n"
                        "您的任務是按下與字體顏色相對應的按鈕，而不是詞語本身。\n\n"
                        "儘量快速和準確地回應。\n\n"
                        "回應鍵如下:\n\n"
                        "r = 紅色\n"
                        "b = 藍色\n"
                        "g = 綠色\n\n"
                        "記住，選擇字母的顏色，忽略詞語本身。\n\n"
                        "按 'Enter' 開始，一旦您理解了規則。")
    #displays instruction text 
    instructions = visual.TextStim(win, text = instruction_text, pos = (-5.0,0.0))
    instructions.draw()
    win.flip()  
    enter_key = event.waitKeys(keyList = ['return'])
    #waits for response (enter key) 
    if enter_key: 
        finger_placement = visual.ImageStim(win, image = 'finger_instruction.png')
        finger_placement.draw() 
        win.flip()
        core.wait(3)
    

color_translations = {"red" : "紅", "blue" :"藍", "green" : "綠", "brown" : "棕"}
color_chinese = ["紅", "藍", "綠"]
color_english = ["red", "blue", "green"]
experiment_data = []

pairings = []
for i in color_english: 
    for j in color_chinese: 
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
        #test_text is tuple -- (english, chinese) 
        test_text = pairings[i]
        correct_color = test_text[0]
        #checks if color of text is same as text 
        congruence = color_translations[correct_color] == test_text[1]
        test = visual.TextStim(win, text = test_text[1], height = 60, color = correct_color) 
        test.draw()
        win.flip(clearBuffer = False)
        stimulus_onset = experiment_clock.getTime()
        #waiting for response 
        response = event.waitKeys(keyList=['r', 'g', 'b'], timeStamped=experiment_clock)
        if response: 
            data = {
                    "response_key" : response[0][0], 
                    "correct_color" : correct_color,
                    "correct" : response[0][0] == correct_color[0] ,
                    "congruent" : congruence,
                    "fixation_onset" : fixation_onset,
                    "fixation_offset" : fixation_offset ,
                    "stimulus_onset": stimulus_onset,
                    "response_time" : response[0][1],
                    "response_speed" : response[0][1] - stimulus_onset
                    }
            experiment_data.append(data)
                    
            
    
        

experiment_clock.reset() 
display_instructions()
display_stimuli()
df = pd.DataFrame(experiment_data)
df.to_csv()
print(experiment_data)
print(pairings)





