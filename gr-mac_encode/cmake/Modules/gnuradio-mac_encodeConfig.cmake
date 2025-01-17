find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_MAC_ENCODE gnuradio-mac_encode)

FIND_PATH(
    GR_MAC_ENCODE_INCLUDE_DIRS
    NAMES gnuradio/mac_encode/api.h
    HINTS $ENV{MAC_ENCODE_DIR}/include
        ${PC_MAC_ENCODE_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_MAC_ENCODE_LIBRARIES
    NAMES gnuradio-mac_encode
    HINTS $ENV{MAC_ENCODE_DIR}/lib
        ${PC_MAC_ENCODE_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-mac_encodeTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_MAC_ENCODE DEFAULT_MSG GR_MAC_ENCODE_LIBRARIES GR_MAC_ENCODE_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_MAC_ENCODE_LIBRARIES GR_MAC_ENCODE_INCLUDE_DIRS)
