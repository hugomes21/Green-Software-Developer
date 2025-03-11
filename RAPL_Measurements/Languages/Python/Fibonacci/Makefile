NTIMES=10
export NTIMES

compile_O0:
	echo "No need to compile"

measure_O0:
	sudo modprobe msr
	sudo ../../../RAPL/main "python3 fibR.py $$size" Python fibonacci_normal_$(size) $(NTIMES)

clean:
	echo "No need to clean"