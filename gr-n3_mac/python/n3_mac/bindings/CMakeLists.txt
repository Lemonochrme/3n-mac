# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT n3_mac_sources)
    message(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT n3_mac_sources)

########################################################################
# Check for pygccxml
########################################################################
gr_python_check_module_raw("pygccxml" "import pygccxml" PYGCCXML_FOUND)

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND n3_mac_python_files python_bindings.cc)

gr_pybind_make_oot(n3_mac ../../.. gr::n3_mac "${n3_mac_python_files}")

# copy bindings extension for use in QA test module
add_custom_command(
    TARGET n3_mac_python
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:n3_mac_python>
            ${PROJECT_BINARY_DIR}/test_modules/gnuradio/n3_mac/)

install(
    TARGETS n3_mac_python
    DESTINATION ${GR_PYTHON_DIR}/gnuradio/n3_mac
    COMPONENT pythonapi)
