#!/bin/bash

# Define number of times to execute each program
NTIMES=10

# Define the number of seconds to wait for the CPU to cooldown
COOLDOWN_SECONDS=30

# Define power limit values
POWER_LIMITS=(2 12 20) # aqui os powercaps, aquilo que te dá o consumo de energia mais baixo

# Define input sizes
INPUT_SIZES=(40)

# Compile sensors which will be used to calculate cool temperature
cd RAPL
gcc -shared -o sensors.so sensors.c
cd ..

# Update the temperature value
cd Utils/
python3 temperatureUpdate.py $COOLDOWN_SECONDS

# Update the number of times the program will run for each case
for language in "../Languages/C"; do
    for program in "$language"/Fibonacci*; do
        if [ -d "$program" ]; then
            makefile_path="$program/Makefile"
            if [ -f "$makefile_path" ]; then
                python3 ntimesUpdate.py "$NTIMES" "$makefile_path"
            else
                echo "Makefile not found: $makefile_path"
            fi
        fi
    done
done
cd ..

# Loop over power limit values
for limit in "${POWER_LIMITS[@]}"
do
    cd Utils/
    python3 raplCapUpdate.py $limit ../RAPL/main.c
    cd ..
    
    # Make RAPL
    cd RAPL/
    rm sensors.so
    make
    cd ..

    # Iterate over programs
    for language in "Languages/C"; do
        for program in "$language"/Fibonacci*; do
            if [ -d "$program" ]; then
                makefile_path="$program/Makefile"
                if [ -f "$makefile_path" ]; then
                    cd "$program"

                    # Iterate over input sizes
                    for size in "${INPUT_SIZES[@]}"; do
                        # Measure with -O0 optimization
                        make compile_O0 size=$size
                        make measure_O0 size=$size
                        file="measurements.csv"
                        if [ -f "$file" ]; then
                            while IFS=, read -r line; do
                                input_size=$(echo "$line" | cut -d',' -f2)  # Assuming input size is in the second column
                                echo "${program##*/}_O0_${input_size}_cap${limit}, $line" >> ../../measurements.csv
                            done < <(tail -n +2 "$file")
                        fi

                        # Measure with -O2 optimization
                        make compile_O2 size=$size
                        make measure_O2 size=$size
                        file="measurements.csv"
                        if [ -f "$file" ]; then
                            while IFS=, read -r line; do
                                input_size=$(echo "$line" | cut -d',' -f2)  # Assuming input size is in the second column
                                echo "${program##*/}_O2_${input_size}_cap${limit}, $line" >> ../../measurements.csv
                            done < <(tail -n +2 "$file")
                        fi
                    done
                    make clean
                    cd ../../..
                else
                    echo "Makefile not found: $makefile_path"
                fi
            fi
        done
    done
done