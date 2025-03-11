NTIMES=10
export NTIMES

compile_O0:
#	/usr/bin/gcc -O0 ms_int.c -o merge_sort_int_O0_$(size)
#	/usr/bin/gcc -O0 ms_float.c -o merge_sort_float_O0_$(size)
	/usr/bin/gcc -O0 ms_double.c -o merge_sort_double_O0_$(size)
#	/usr/bin/gcc -O0 ms_string.c -o merge_sort_string_O0_$(size)

compile_O2:
#	/usr/bin/gcc -O2 ms_int.c -o merge_sort_int_O2_$(size)
#	/usr/bin/gcc -O2 ms_float.c -o merge_sort_float_O2_$(size)
	/usr/bin/gcc -O2 ms_double.c -o merge_sort_double_O2_$(size)
#	/usr/bin/gcc -O2 ms_string.c -o merge_sort_string_O2_$(size)

measure_O0:
	sudo modprobe msr
#	sudo ../../../RAPL/main "./merge_sort_int_O0_$(size) $(size)" C merge_sort_int_O0_$(size) $(NTIMES)
#	sudo ../../../RAPL/main "./merge_sort_float_O0_$(size) $(size)" C merge_sort_float_O0_$(size) $(NTIMES)
	sudo ../../../RAPL/main "./merge_sort_double_O0_$(size) $(size)" C merge_sort_double_O0_$(size) $(NTIMES)
#	sudo ../../../RAPL/main "./merge_sort_string_O0_$(size) $(size)" C merge_sort_string_O0_$(size) $(NTIMES)

measure_O2:
	sudo modprobe msr
#	sudo ../../../RAPL/main "./merge_sort_int_O2_$(size) $(size)" C merge_sort_int_O2_$(size) $(NTIMES)
#	sudo ../../../RAPL/main "./merge_sort_float_O2_$(size) $(size)" C merge_sort_float_O2_$(size) $(NTIMES)
	sudo ../../../RAPL/main "./merge_sort_double_O2_$(size) $(size)" C merge_sort_double_O2_$(size) $(NTIMES)
#	sudo ../../../RAPL/main "./merge_sort_string_O2_$(size) $(size)" C merge_sort_string_O2_$(size) $(NTIMES)

clean:
	rm -f merge_sort_int_O0_* merge_sort_float_O0_* merge_sort_double_O0_* merge_sort_string_O0_*
	rm -f merge_sort_int_O2_* merge_sort_float_O2_* merge_sort_double_O2_* merge_sort_string_O2_*