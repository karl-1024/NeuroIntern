from psychopy import visual, core, event
import random
import pandas as pd

# Create a clock to record precise times
experiment_clock = core.Clock()

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

    instructions = visual.TextStim(win, text=instruction_text, height=20, color='black')
    instructions.draw()
    win.flip()
    event.waitKeys(keyList=['return'])

    # Display finger instruction image for 5 seconds
    finger_instruction_image = visual.ImageStim(win, image='finger_instruction.png')
    finger_instruction_image.draw()
    win.flip()
    core.wait(5)

# Create a window with a grey background
win = visual.Window(size=(800, 600), color='grey', units='pix')

# Display instructions
display_instructions()

# Define image file paths
image_files = {
    'red': {'red': 'red_red.png', 'green': 'red_green.png', 'blue': 'red_blue.png'},
    'green': {'red': 'green_red.png', 'green': 'green_green.png', 'blue': 'green_blue.png'},
    'blue': {'red': 'blue_red.png', 'green': 'blue_green.png', 'blue': 'blue_blue.png'}
}

colors = ['red', 'green', 'blue']
pairings = []

for color in colors:
    for word in colors:
        pairings.extend([image_files[color][word]] * 4)

random.shuffle(pairings)

# Initialize a list to store experiment data
experiment_data = []

# Reset the clock to zero at the beginning of the experiment
experiment_clock.reset()

# Run the Stroop task trials
for trial, image_file in enumerate(pairings):
    # Blank screen before fixation (0.5 seconds)
    win.flip()
    core.wait(0.5)

    # Record the time for fixation onset with microsecond precision
    fixation_onset = experiment_clock.getTime()

    # Fixation cross (0.5 seconds)
    fixation_cross = visual.TextStim(win, text='+', height=40, color='black')
    fixation_cross.draw()
    win.flip()
    core.wait(0.5)

    # Record the time for fixation offset with microsecond precision
    fixation_offset = experiment_clock.getTime()

    # Blank screen after fixation (0.5 seconds)
    win.flip()
    core.wait(0.5)

    # Record the time for stimulus onset with microsecond precision
    stimulus_onset = experiment_clock.getTime()

    # Stimulus presentation (1.5 seconds)
    stimulus = visual.ImageStim(win, image=image_file)
    stimulus.draw()
    win.flip()
    start_time = experiment_clock.getTime()

    # Wait for a response
    response = event.waitKeys(maxWait=1.5, keyList=['r', 'g', 'b'], timeStamped=experiment_clock)

    # Record the time for stimulus offset with microsecond precision
    stimulus_offset = experiment_clock.getTime()

    # Determine the correct response based on the color in the image file name
    correct_response = image_file.split('_')[0]

    # Calculate response time and correctness
    response_key = None
    response_time = None
    correctness = False
    if response:
        response_key = response[0][0]  # The key that was pressed
        response_time = response[0][1]  # The response time
        correctness = (response_key == correct_response[0])  # Compare the first letter

    # Record trial data with microsecond precision
    trial_data = {
        'trial_number': trial + 1,
        'stimulus_file': image_file,
        'response_key': response_key,
        'response_time': response_time,
        'correctness': correctness,
        'fixation_onset': fixation_onset,
        'fixation_offset': fixation_offset,
        'stimulus_onset': stimulus_onset,
        'stimulus_offset': stimulus_offset
    }
    experiment_data.append(trial_data)

    # Feedback presentation (0.5 seconds)
    feedback_text = "正確!" if correctness else "錯誤!" if response_key else "請更快地回應。"
    feedback = visual.TextStim(win, text=feedback_text, height=30, color='black')
    feedback.draw()
    win.flip()
    core.wait(0.5)

    # Clear the screen for the next trial
    win.flip()

# Close the window
win.close()

# Convert the data to a DataFrame and save to an Excel file
df = pd.DataFrame(experiment_data)
excel_filename = 'experiment_data.xlsx'
df.to_excel(excel_filename, index=False)