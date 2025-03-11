import re, time, ctypes, sys, os

NUMBER_OF_SECONDS_TO_COOL_DOWN = int(sys.argv[1])

TEMPERATURE_FILE = "core_temperatures.txt"

def get_core_temperatures():
    # Run the sensors command and capture the output
    output = os.popen('sensors').read()

    # Extract temperature values
    temperatures = re.findall(r'Core \d+:\s+\+([0-9.]+)°C', output)
    temperatures = [float(temp) for temp in temperatures]
    return temperatures

def write_temperatures_to_file(temperatures):
    with open(TEMPERATURE_FILE, 'w') as f:
        for i, temp in enumerate(temperatures):
            f.write(f"Core {i}: {temp}°C\n")
        average_temp = sum(temperatures) / len(temperatures)
        f.write(f"Average Temperature: {average_temp}°C\n")
    return average_temp

def read_average_temperature_from_file():
    with open(TEMPERATURE_FILE, 'r') as f:
        lines = f.readlines()
        average_temp_line = lines[-1]
        average_temp = float(average_temp_line.split(":")[1].strip().replace('°C', ''))
    return average_temp

def main():
    with open("../RAPL/main.c", 'r') as f:
        data = f.read()

    lib = ctypes.CDLL('../RAPL/sensors.so')

    # Define the return type of the function
    lib.getTemperature.restype = ctypes.c_float

    print("Cooling Down for {} seconds...".format(NUMBER_OF_SECONDS_TO_COOL_DOWN))
    time.sleep(NUMBER_OF_SECONDS_TO_COOL_DOWN)

    if not os.path.exists(TEMPERATURE_FILE):
        print(f"[WARNING] {TEMPERATURE_FILE} does not exist. Creating new file and recording temperatures...")
        temperatures = get_core_temperatures()
        average_temp = write_temperatures_to_file(temperatures)
    else:
        print(f"[WARNING] {TEMPERATURE_FILE} already exists. Reading existing average temperature...")
        average_temp = read_average_temperature_from_file()

    data = re.sub(r'#define TEMPERATURETHRESHOLD .*', f'#define TEMPERATURETHRESHOLD {average_temp}', data)
    
    with open("../RAPL/main.c", 'w') as f:
        f.write(data)

if __name__ == "__main__":
    main()