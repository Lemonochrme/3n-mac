find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_CSMA gnuradio-csma)

FIND_PATH(
    GR_CSMA_INCLUDE_DIRS
    NAMES gnuradio/csma/api.h
    HINTS $ENV{CSMA_DIR}/include
        ${PC_CSMA_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_CSMA_LIBRARIES
    NAMES gnuradio-csma
    HINTS $ENV{CSMA_DIR}/lib
        ${PC_CSMA_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-csmaTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_CSMA DEFAULT_MSG GR_CSMA_LIBRARIES GR_CSMA_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_CSMA_LIBRARIES GR_CSMA_INCLUDE_DIRS)
