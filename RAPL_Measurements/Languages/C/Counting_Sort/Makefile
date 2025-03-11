NTIMES=10
export NTIMES

compile_O0:
#	/usr/bin/gcc -O0 cs_int.c -o counting_sort_int_O0_$(size)
#	/usr/bin/gcc -O0 cs_float.c -o counting_sort_float_O0_$(size)
	/usr/bin/gcc -O0 cs_double.c -o counting_sort_double_O0_$(size)
#	/usr/bin/gcc -O0 cs_string.c -o counting_sort_string_O0_$(size)

compile_O2:
#	/usr/bin/gcc -O2 cs_int.c -o counting_sort_int_O2_$(size)
#	/usr/bin/gcc -O2 cs_float.c -o counting_sort_float_O2_$(size)
	/usr/bin/gcc -O2 cs_double.c -o counting_sort_double_O2_$(size)
#	/usr/bin/gcc -O2 cs_string.c -o counting_sort_string_O2_$(size)

measure_O0:
	sudo modprobe msr
#	sudo ../../../RAPL/main "./counting_sort_int_O0_$(size) $(size)" C counting_sort_int_O0_$(size) $(NTIMES)
#	sudo ../../../RAPL/main "./counting_sort_float_O0_$(size) $(size)" C counting_sort_float_O0_$(size) $(NTIMES)
	sudo ../../../RAPL/main "./counting_sort_double_O0_$(size) $(size)" C counting_sort_double_O0_$(size) $(NTIMES)
#	sudo ../../../RAPL/main "./counting_sort_string_O0_$(size) $(size)" C counting_sort_string_O0_$(size) $(NTIMES)

measure_O2:
	sudo modprobe msr
#	sudo ../../../RAPL/main "./counting_sort_int_O2_$(size) $(size)" C counting_sort_int_O2_$(size) $(NTIMES)
#	sudo ../../../RAPL/main "./counting_sort_float_O2_$(size) $(size)" C counting_sort_float_O2_$(size) $(NTIMES)
	sudo ../../../RAPL/main "./counting_sort_double_O2_$(size) $(size)" C counting_sort_double_O2_$(size) $(NTIMES)
#	sudo ../../../RAPL/main "./counting_sort_string_O2_$(size) $(size)" C counting_sort_string_O2_$(size) $(NTIMES)

clean:
	rm -f counting_sort_int_O0_* counting_sort_float_O0_* counting_sort_double_O0_* counting_sort_string_O0_*
	rm -f counting_sort_int_O2_* counting_sort_float_O2_* counting_sort_double_O2_* counting_sort_string_O2_*