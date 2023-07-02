import time

# Dictionary to map sequences of movements to command names
COMMANDS = {
    'LowPass': 'Start',
    'HighPass': 'Resume',
    'LowHold': 'Stop',
    'HighHold': 'Pause',
    'PullUp': 'Louder',
    'PushDown': 'Quieter',
    'LowPass,LowPass': 'Skip forward',
    'HighPass,HighPass': 'Skip backward',
    'LowPass,LowHold': 'Power off',
    'HighPass,HighHold': 'Reset',
    'PullUp,HighPass,LowHold': 'ActivateAutoMode',
    'PushDown,LowPass,HighHold': 'DisableAutoMode'
}

# Function to analyze a list of distances and return the movement type
def analyse_recording(distance_list):
    if not distance_list:
        return 'unknown'

    length = len(distance_list)
    difference = distance_list[0] - distance_list[-1]

    if length < 8:
        return 'LowPass' if distance_list[0] < 15 else 'HighPass'
    elif 10 < difference:
        return 'PushDown'
    elif -10 > difference:
        return 'PullUp'
    else:
        return 'LowHold' if distance_list[0] < 15 else 'HighHold'

# Function to identify the command based on a list of movements
def identify_Command(movement_list):
    command = COMMANDS.get(",".join(movement_list))
    if command:
        print(command)

# Main loop function
def loop():

    threshold = 100
    below_threshold = False
    above_treshold_counter = 0
    distance_list = []
    movement_list = []

    # Main loop
    while(True):
        # Get the distance from the device and handle possible exceptions
        try:
            distance = device.getSonar()
        except Exception as e:
            print(f"Error getting distance: {e}")
            time.sleep(0.1)
            continue

        #print ("The distance is : %.2f cm"%(distance))

        # When the distance is below the threshold
        if (distance < threshold):
            above_treshold_counter = 0

            if (below_threshold == False):
                distance_list = []
                below_threshold = True
            distance_list.append(distance)
        else:
            # When the distance goes above the threshold after being below it
            if (below_threshold == True):
                result = analyse_recording(distance_list)
                movement_list.append(result)
                print(result)
                below_threshold = False

        # When the distance is above the threshold
        if (distance >= threshold):
            above_treshold_counter += 1
            if (above_treshold_counter > 20):
                print(movement_list)
                identify_Command(movement_list)
                movement_list = []
                above_treshold_counter = 0

        time.sleep(0.1)

usingRaspberryPi = False  # Change to True if running on an actual Raspberry Pi

if __name__ == '__main__':  # Program entrance
    if usingRaspberryPi:
        import UltrasonicRangerInterface as device
    else:
        import SonarSim as device
    print('Program is starting...')
    device.setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press Ctrl-C to end the program.
        device.cleanup()
        print('Bye...')
