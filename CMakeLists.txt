cmake_minimum_required(VERSION 3.4)
project(linear)

# VERSION ######################################################################
set(LINEAR_VERSION_MAJOR 2)
set(LINEAR_VERSION_MINOR 20)

# CONAN SETUP ##################################################################
include(conanbuildinfo.cmake)
conan_basic_setup()

# PREDICT ######################################################################
add_library(${CMAKE_PROJECT_NAME} ${CMAKE_SOURCE_DIR}/source_subfolder/tron.cpp
                                  ${CMAKE_SOURCE_DIR}/source_subfolder/tron.h
                                  ${CMAKE_SOURCE_DIR}/source_subfolder/linear.cpp
                                  ${CMAKE_SOURCE_DIR}/source_subfolder/linear.h
                                  ${CMAKE_SOURCE_DIR}/source_subfolder/blas/blas.h
                                  ${CMAKE_SOURCE_DIR}/source_subfolder/blas/blasp.h
                                  ${CMAKE_SOURCE_DIR}/source_subfolder/blas/daxpy.c
                                  ${CMAKE_SOURCE_DIR}/source_subfolder/blas/ddot.c
                                  ${CMAKE_SOURCE_DIR}/source_subfolder/blas/dnrm2.c
                                  ${CMAKE_SOURCE_DIR}/source_subfolder/blas/dscal.c)

# PROPERTIES ###################################################################
if (WIN32 AND MSVC)
    set_target_properties(${CMAKE_PROJECT_NAME} PROPERTIES WINDOWS_EXPORT_ALL_SYMBOLS ON)
endif()

# INSTALL ######################################################################
install(TARGETS ${CMAKE_PROJECT_NAME}
        RUNTIME DESTINATION bin
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib)

install(FILES ${CMAKE_SOURCE_DIR}/source_subfolder/tron.h
              ${CMAKE_SOURCE_DIR}/source_subfolder/linear.h
        DESTINATION include)
