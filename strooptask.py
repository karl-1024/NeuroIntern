from psychopy import visual, core, event
import random

def display_instructions():
    instruction_text = ("在這個遊戲中，您將看到顏色詞語（紅色，藍色，綠色）逐一出現。"
                        "您的任務是按下與字體顏色相對應的按鈕，而不是詞語本身。\n\n"
                        "儘量快速和準確地回應。\n\n"
                        "回應鍵如下:\n\n"
                        "r = 紅色\n"
                        "b = 藍色\n"
                        "g = 綠色\n\n"
                        "記住，選擇字母的顏色，忽略詞語本身。\n\n"
                        "按 'Enter' 開始，一旦您理解了規則。")

    instructions = visual.TextStim(win, text=instruction_text, height=20, color='black')
    instructions.draw()
    win.flip()
    start_time = core.getTime()
    while core.getTime() - start_time < 10.0 or not event.getKeys(keyList=['return']):
        pass

# Create a window
win = visual.Window(size=(800, 600), color='white', units='pix')

# Create text stimulus
text_stim = visual.TextStim(win, height=40, color='black')

# Display instructions
display_instructions()

# Define colors and words
colors = ['紅色', '綠色', '藍色']
words = ['紅色', '綠色', '藍色']

# Create a list to store the pairings
pairings = []

# Iterate through each color and color option to create pairings
for color in colors:
    for option in colors:
        # Repeat each pairing 4 times
        pairings.extend([(color, option)] * 4)

# Shuffle the pairings to randomize the order
random.shuffle(pairings)

# Run 36 trials of the Stroop task
for pairing in pairings:
    color, option = pairing

    # Fixation cross (0.5 seconds) 
    fixation_cross = visual.TextStim(win, text='+', height=40, color='black')
    fixation_cross.draw()
    win.flip()
    core.wait(0.5)

    # Stimulus presentation (1.5 seconds)
    text_stim.color = color.lower()  # Set color based on the chosen color
    text_stim.text = option  # Set the text based on the chosen color option
    text_stim.draw()
    win.flip()
    core.wait(1.5)

    # Clear the screen (0.5 seconds)
    win.flip()
    core.wait(0.5)

    # Feedback presentation (0.5 seconds)
    response = event.getKeys(keyList=['r', 'g', 'b'])
    if response and response[0] in ['r', 'g', 'b']:
        if response[0] == color[0].lower():
            feedback_text = "正確!"
        else:
            feedback_text = "錯誤!"
    else:
        feedback_text = "請更快地回應。"

    feedback = visual.TextStim(win, text=feedback_text, height=30, color='black')
    feedback.draw()
    win.flip()
    core.wait(0.5)

    # Clear the screen for the next trial
    win.flip()

# Close the window
win.close()
core.quit()
