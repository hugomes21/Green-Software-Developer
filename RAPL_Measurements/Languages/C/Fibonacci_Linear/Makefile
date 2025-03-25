NTIMES=10
export NTIMES

compile_O0:
	/usr/bin/gcc -O0 fibL.c -o fibonacci_linear_O0_$(size)

compile_O2:
	/usr/bin/gcc -O2 fibL.c -o fibonacci_linear_O2_$(size)

exec_O0:
	./fibonacci_linear_O0_$(size) $(size)

exec_O2:
	./fibonacci_linear_O2_$(size) $(size)

measure_O0:
	sudo modprobe msr
	sudo ../../../RAPL/main "./fibonacci_linear_O0_$(size) $(size)" C fibonacci_linear_O0_$(size) $(NTIMES)

measure_O2:
	sudo modprobe msr
	sudo ../../../RAPL/main "./fibonacci_linear_O2_$(size) $(size)" C fibonacci_linear_O2_$(size) $(NTIMES)

clean:
	rm -f fibonacci_linear_O0 fibonacci_linear_O2