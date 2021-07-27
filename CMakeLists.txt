cmake_minimum_required(VERSION 3.8.2)

set(IMGUI_SOVERSION 1)
mark_as_advanced(IMGUI_SOVERSION)

set(IMGUI_VERSION 1.83)
mark_as_advanced(IMGUI_VERSION)

project(imgui LANGUAGES CXX VERSION ${IMGUI_VERSION})
if(EXISTS ${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
   include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
   conan_basic_setup()
endif()

option(IMGUI_DEMO "Include the ImGui demo window implementation in library" ON)

add_library(imgui
   src/imgui.cpp
   src/imgui_draw.cpp
   src/imgui_widgets.cpp
   src/imgui_tables.cpp

   $<$<BOOL:IMGUI_DEMO>:src/imgui_demo.cpp>
)

add_library(imgui::imgui ALIAS imgui)

target_include_directories(imgui
   PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/src>

   PUBLIC $<INSTALL_INTERFACE:include>
)

set_target_properties(imgui PROPERTIES
   SOVERSION ${IMGUI_SOVERSION}
   VERSION ${IMGUI_VERSION}
)

if(NOT APPLE)
   set_target_properties(imgui PROPERTIES INSTALL_RPATH $ORIGIN)
endif()

if(NOT CMAKE_CROSSCOMPILING)
   add_executable(imgui-binary-to-compressed-c MACOSX_BUNDLE src/misc/fonts/binary_to_compressed_c.cpp)
endif()

#
# Bindings
#
include(GNUInstallDirs)

macro(add_binding name extension)
   add_library(${name} INTERFACE)
   target_sources(${name} INTERFACE $<INSTALL_INTERFACE:${CMAKE_INSTALL_DATADIR}/imgui_impl_${name}.${extension}>)
   add_library(imgui::${name} ALIAS ${name})
endmacro()

add_binding(allegro5 cpp)
add_binding(android cpp)
add_binding(dx9 cpp)
add_binding(dx10 cpp)
add_binding(dx11 cpp)
add_binding(dx12 cpp)
add_binding(glfw cpp)
add_binding(glut cpp)
add_binding(marmelade cpp)
add_binding(metal mm)
add_binding(opengl2 cpp)
add_binding(opengl3 cpp)
add_binding(osx mm)
add_binding(sdl cpp)
add_binding(vulkan cpp)
add_binding(win32 cpp)
add_binding(wgpu cpp)

#
# Installation
#
include(CMakePackageConfigHelpers)

set(IMGUI_CONFIG_INSTALL_DIR "${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}")

set(IMGUI_GENERATED_CMAKE_DIR "${CMAKE_CURRENT_BINARY_DIR}/generated/cmake")
set(IMGUI_VERSION_CONFIG "${IMGUI_GENERATED_CMAKE_DIR}/IMGUIConfigVersion.cmake")
set(IMGUI_PROJECT_CONFIG "${IMGUI_GENERATED_CMAKE_DIR}/IMGUIConfig.cmake")

set(IMGUI_INSTALL_CMAKEDIR "${CMAKE_INSTALL_LIBDIR}/cmake/IMGUI" CACHE STRING "Path to the IMGUI cmake files")

write_basic_package_version_file(${IMGUI_VERSION_CONFIG} COMPATIBILITY SameMajorVersion)
configure_package_config_file(${CMAKE_CURRENT_LIST_DIR}/Config.cmake.in
   ${IMGUI_PROJECT_CONFIG}
   INSTALL_DESTINATION ${IMGUI_INSTALL_CMAKEDIR}
)

set(IMGUI_BINARIES imgui)
if(NOT CMAKE_CROSSCOMPILING)
   set(IMGUI_BINARIES ${IMGUI_BINARIES} imgui-binary-to-compressed-c)
endif()

install(
   TARGETS
      ${IMGUI_BINARIES}

      allegro5 dx9 dx10 dx11 dx12 glfw glut marmelade metal opengl2 opengl3 osx sdl vulkan win32 wgpu

   EXPORT IMGUI_Targets

   BUNDLE DESTINATION ${CMAKE_INSTALL_BINDIR} COMPONENT IMGUI_Runtime
   RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR} COMPONENT IMGUI_Runtime
   LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR} COMPONENT IMGUI_Runtime NAMELINK_COMPONENT IMGUI_Development
   ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR} COMPONENT IMGUI_Development
   INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

install(
   FILES
      src/imconfig.h
      src/imgui.h
      src/imgui_internal.h
      src/imstb_rectpack.h
      src/imstb_textedit.h
      src/imstb_truetype.h

      src/backends/imgui_impl_allegro5.h
      src/backends/imgui_impl_android.h
      src/backends/imgui_impl_dx10.h
      src/backends/imgui_impl_dx11.h
      src/backends/imgui_impl_dx12.h
      src/backends/imgui_impl_dx9.h
      src/backends/imgui_impl_glfw.h
      src/backends/imgui_impl_glut.h
      src/backends/imgui_impl_marmalade.h
      src/backends/imgui_impl_metal.h
      src/backends/imgui_impl_opengl2.h
      src/backends/imgui_impl_opengl3.h
      src/backends/imgui_impl_osx.h
      src/backends/imgui_impl_sdl.h
      src/backends/imgui_impl_vulkan.h
      src/backends/imgui_impl_win32.h
      src/backends/imgui_impl_wgpu.h

   DESTINATION
      ${CMAKE_INSTALL_INCLUDEDIR}
)

install(
   FILES
      src/backends/imgui_impl_allegro5.cpp
      src/backends/imgui_impl_android.cpp
      src/backends/imgui_impl_dx10.cpp
      src/backends/imgui_impl_dx11.cpp
      src/backends/imgui_impl_dx12.cpp
      src/backends/imgui_impl_dx9.cpp
      src/backends/imgui_impl_glfw.cpp
      src/backends/imgui_impl_glut.cpp
      src/backends/imgui_impl_marmalade.cpp
      src/backends/imgui_impl_metal.mm
      src/backends/imgui_impl_opengl2.cpp
      src/backends/imgui_impl_opengl3.cpp
      src/backends/imgui_impl_osx.mm
      src/backends/imgui_impl_sdl.cpp
      src/backends/imgui_impl_vulkan.cpp
      src/backends/imgui_impl_win32.cpp
      src/backends/imgui_impl_wgpu.cpp

   DESTINATION
      ${CMAKE_INSTALL_DATADIR}
)

install(
   FILES
      ${IMGUI_PROJECT_CONFIG}
      ${IMGUI_VERSION_CONFIG}

   DESTINATION
      ${IMGUI_INSTALL_CMAKEDIR}
)

install(EXPORT IMGUI_Targets
   DESTINATION ${IMGUI_INSTALL_CMAKEDIR}
   NAMESPACE imgui::
   COMPONENT IMGUI_Development
)

install(
   FILES
      src/misc/fonts/Cousine-Regular.ttf
      src/misc/fonts/DroidSans.ttf
      src/misc/fonts/Karla-Regular.ttf
      src/misc/fonts/ProggyClean.ttf
      src/misc/fonts/ProggyTiny.ttf
      src/misc/fonts/Roboto-Medium.ttf

   DESTINATION
      ${CMAKE_INSTALL_DATADIR}/fonts/
)
