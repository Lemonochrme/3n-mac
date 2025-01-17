# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT communication_simulation_sources)
    MESSAGE(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT communication_simulation_sources)

########################################################################
# Check for pygccxml
########################################################################
GR_PYTHON_CHECK_MODULE_RAW(
    "pygccxml"
    "import pygccxml"
    PYGCCXML_FOUND
    )

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND communication_simulation_python_files
    python_bindings.cc)

GR_PYBIND_MAKE_OOT(communication_simulation
   ../../..
   gr::communication_simulation
   "${communication_simulation_python_files}")

# copy bindings extension for use in QA test module
add_custom_command(TARGET communication_simulation_python POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:communication_simulation_python>
    ${PROJECT_BINARY_DIR}/test_modules/gnuradio/communication_simulation/
)

install(TARGETS communication_simulation_python DESTINATION ${GR_PYTHON_DIR}/gnuradio/communication_simulation COMPONENT pythonapi)
