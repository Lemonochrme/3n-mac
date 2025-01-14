find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_N3_MAC gnuradio-n3_mac)

FIND_PATH(
    GR_N3_MAC_INCLUDE_DIRS
    NAMES gnuradio/n3_mac/api.h
    HINTS $ENV{N3_MAC_DIR}/include
        ${PC_N3_MAC_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_N3_MAC_LIBRARIES
    NAMES gnuradio-n3_mac
    HINTS $ENV{N3_MAC_DIR}/lib
        ${PC_N3_MAC_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-n3_macTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_N3_MAC DEFAULT_MSG GR_N3_MAC_LIBRARIES GR_N3_MAC_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_N3_MAC_LIBRARIES GR_N3_MAC_INCLUDE_DIRS)
