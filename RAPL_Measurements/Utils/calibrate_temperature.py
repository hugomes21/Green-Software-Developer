import os, re, time

NUMBER_OF_SECONDS = 30

def get_temperature():
    print(f"Sleeping {NUMBER_OF_SECONDS} seconds to calibrate the temperature...")
    time.sleep(NUMBER_OF_SECONDS)

    # Run the sensors command and redirect output to a file
    status = os.system("sensors > core_temperature.txt")
    if status != 0:
        print("Error executing command: sensors")
        return -1

    temperatures = []

    with open("core_temperature.txt", "r") as file:
        lines = file.readlines() 

    with open("core_temperature.txt", "w") as output_file:  # Open the same file for writing
        for line in lines:
            match = re.search(r'Core \d+: *\+([0-9.]+)°C', line)
            if match:
                core_number = line.split(':')[0].strip()
                temperature = float(match.group(1))
                temperatures.append(temperature)

                output_file.write(f"{core_number}: {temperature}°C\n")

        if temperatures:
            mean_temp = sum(temperatures) / len(temperatures)
        else:
            mean_temp = 0.0

        output_file.write(f"Average temperature: {mean_temp:.1f}°C\n") 

    print(f"\nMean temperature in all cores is {mean_temp:.10f}°C")

    return mean_temp

get_temperature()