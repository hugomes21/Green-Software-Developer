NTIMES=10
export NTIMES

compile_O0:
#	/usr/bin/gcc -O0 bs_int.c -o bubble_sort_int_O0_$(size)
#	/usr/bin/gcc -O0 bs_float.c -o bubble_sort_float_O0_$(size)
	/usr/bin/gcc -O0 bs_double.c -o bubble_sort_double_O0_$(size)
#	/usr/bin/gcc -O0 bs_string.c -o bubble_sort_string_O0_$(size)

compile_O2:
#	/usr/bin/gcc -O2 bs_int.c -o bubble_sort_int_O2_$(size)
#	/usr/bin/gcc -O2 bs_float.c -o bubble_sort_float_O2_$(size)
	/usr/bin/gcc -O2 bs_double.c -o bubble_sort_double_O2_$(size)
#	/usr/bin/gcc -O2 bs_string.c -o bubble_sort_string_O2_$(size)

measure_O0:
	sudo modprobe msr
#	sudo ../../../RAPL/main "./bubble_sort_int_O0_$(size) $(size)" C bubble_sort_int_O0_$(size) $(NTIMES)
#	sudo ../../../RAPL/main "./bubble_sort_float_O0_$(size) $(size)" C bubble_sort_float_O0_$(size) $(NTIMES)
	sudo ../../../RAPL/main "./bubble_sort_double_O0_$(size) $(size)" C bubble_sort_double_O0_$(size) $(NTIMES)
#	sudo ../../../RAPL/main "./bubble_sort_string_O0_$(size) $(size)" C bubble_sort_string_O0_$(size) $(NTIMES)

measure_O2:
	sudo modprobe msr
#	sudo ../../../RAPL/main "./bubble_sort_int_O2_$(size) $(size)" C bubble_sort_int_O2_$(size) $(NTIMES)
#	sudo ../../../RAPL/main "./bubble_sort_float_O2_$(size) $(size)" C bubble_sort_float_O2_$(size) $(NTIMES)
	sudo ../../../RAPL/main "./bubble_sort_double_O2_$(size) $(size)" C bubble_sort_double_O2_$(size) $(NTIMES)
#	sudo ../../../RAPL/main "./bubble_sort_string_O2_$(size) $(size)" C bubble_sort_string_O2_$(size) $(NTIMES)

clean:
	rm -f bubble_sort_int_O0_* bubble_sort_float_O0_* bubble_sort_double_O0_* bubble_sort_string_O0_*
	rm -f bubble_sort_int_O2_* bubble_sort_float_O2_* bubble_sort_double_O2_* bubble_sort_string_O2_*