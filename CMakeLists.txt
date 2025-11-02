cmake_minimum_required(VERSION 3.10.0)

project(FailureCriteria
 VERSION 0.1
 DESCRIPTION "This project provides the implementation of various criteria for brittle and ductile failure"
 LANGUAGES CXX
# SPDX_LICENSE LGPL-2.1-or-later
)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(PACKAGE failure-criteria)

include(cmake/modules/mfm.cmake)

# testing
set(CTEST_CONFIGURATION_TYPE "${JOB_BUILD_CONFIGURATION}")
enable_testing()
if(CMAKE_CONFIGURATION_TYPES)
  add_custom_target(check COMMAND 
    ${CMAKE_CTEST_COMMAND} -T test -C $<CONFIGURATION>)
else(CMAKE_CONFIGURATION_TYPES)
  add_custom_target(check COMMAND 
    ${CMAKE_CTEST_COMMAND} -T test )
endif(CMAKE_CONFIGURATION_TYPES)

# add subdirectories here

add_subdirectory(src)