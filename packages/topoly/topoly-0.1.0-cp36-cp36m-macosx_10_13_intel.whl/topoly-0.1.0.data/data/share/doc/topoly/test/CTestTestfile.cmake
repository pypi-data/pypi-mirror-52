# CMake generated Testfile for 
# Source directory: /Users/pol/dev/topopack/test
# Build directory: /Users/pol/dev/topopack/test
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(knotnet_2efv_test "sh" "-c" "/Users/pol/dev/topopack/knotnet /Users/pol/dev/topopack/test/knotnet/2efv_A -c 2 -t 2 --try 100 -o knotnet_out.txt> knotnet_stdout.txt 2>1")
add_test(knotnet_2efv_compare_results "sh" "-c" "/Users/pol/dev/topopack/test/knotnet/compare_output.sh /Users/pol/dev/topopack/test/knotnet/result/KNOTS_2efv_A knotnet_out.txt")
add_test(knotnet_py_2efv_test "sh" "-c" "/Users/pol/dev/topopack/test/knotnet/test_py_knotnet.sh /Users/pol/dev/topopack/test/../ /Users/pol/dev/topopack/test/knotnet/2efv_A knotnet_py_out.txt> knotnet_py_stdout.txt 2>1")
add_test(knotnet_py_2efv_compare_results "sh" "-c" "/Users/pol/dev/topopack/test/knotnet/compare_output.sh /Users/pol/dev/topopack/test/knotnet/result/KNOTS_2efv_A knotnet_py_out.txt")
add_test(preprocess_py_test "sh" "-c" "/Users/pol/dev/topopack/test/preprocess/test_py_preprocess.sh /Users/pol/dev/topopack/test/../ /Users/pol/dev/topopack/test/preprocess/t31_numbered_cut.xyz preprocess_py_out.txt> preprocess_py_stdout.txt 2>1")
add_test(yamada_py_test "sh" "-c" "/Users/pol/dev/topopack/test/homfly/test_py_Yamada_full.sh /Users/pol/dev/topopack/test/../ /Users/pol/dev/topopack/test/data > yamada_py_stdout.txt 2>1")
add_test(surfacesmytraj_test "sh" "-c" "/Users/pol/dev/topopack/test/surfaces/find_lassos.sh /Users/pol/dev/topopack/surfacesmytraj /Users/pol/dev/topopack/test/lassos.out")
set_tests_properties(surfacesmytraj_test PROPERTIES  WORKING_DIRECTORY "/Users/pol/dev/topopack/test/surfaces")
add_test(surfacesmytraj_compare_results "/opt/local/bin/cmake" "-E" "compare_files" "/Users/pol/dev/topopack/test/surfaces/good_lassos.out" "/Users/pol/dev/topopack/test/lassos.out")
set_tests_properties(surfacesmytraj_compare_results PROPERTIES  WORKING_DIRECTORY "/Users/pol/dev/topopack/test/surfaces")
add_test(homfly_test "sh" "-c" "/Users/pol/dev/topopack/test/homfly/calc_homfly.sh /Users/pol/dev/topopack/homflylink /Users/pol/dev/topopack/lmpoly /Users/pol/dev/topopack/ncuclinks /Users/pol/dev/topopack/test/knots.out")
set_tests_properties(homfly_test PROPERTIES  WORKING_DIRECTORY "/Users/pol/dev/topopack/test/homfly")
add_test(homfly_compare_results "/opt/local/bin/cmake" "-E" "compare_files" "/Users/pol/dev/topopack/test/homfly/good_knots.out" "/Users/pol/dev/topopack/test/knots.out")
set_tests_properties(homfly_compare_results PROPERTIES  WORKING_DIRECTORY "/Users/pol/dev/topopack/test/surfaces")
