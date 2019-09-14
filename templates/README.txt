Here are some recordings from the flex sensor array. Directories are as follows:

raw-templates Straight recordings sampled from Unity, labeled by myo gesture and strength. Inside each directory, each csv
is labeled by the position the arm was in when recording. Each recording has five trials. 

Columns are [time elapsed (seconds), [sensors 1-4 voltages (0-5V)]]

raw-templates-originals: Same as before, but without named labels on the CSV.

separated-templates: All templates organized for each gesture at each position and strength, with the following naming convention:

[Gesture (1-2 characters) [Waveleft(Wl), Waveright(Wr), Fist(F), Spread Fingers(S), Double Tap(Db)]]-[Position (1 character)]-[Strength (Light, Mid, Strong)].csv

longinput.csv: A recording of a typical use-case scenario. Script for input contained in longinput-script.txt, audio recording in longinput-script.wav