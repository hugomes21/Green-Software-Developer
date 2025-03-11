NTIMES=10
export NTIMES

compile_O0:
	/usr/bin/gcc -O0 fibR.c -o fibonacci_recursive_O0_$(size)

compile_O2:
	/usr/bin/gcc -O2 fibR.c -o fibonacci_recursive_O2_$(size)

measure_O0:
	sudo modprobe msr
	sudo ../../../RAPL/main "./fibonacci_recursive_O0_$(size) $(size)" C fibonacci_recursive_O0_$(size) $(NTIMES)

measure_O2:
	sudo modprobe msr
	sudo ../../../RAPL/main "./fibonacci_recursive_O2_$(size) $(size)" C fibonacci_recursive_O2_$(size) $(NTIMES)

clean:
	rm -f fibonacci_recursive_O0_* fibonacci_recursive_O2_*