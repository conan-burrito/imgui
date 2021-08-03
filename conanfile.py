from conans import tools, ConanFile, CMake

import os


class Recipe(ConanFile):
    name = 'imgui'
    description = 'Bloat-free Immediate Mode Graphical User interface for C++ with minimal dependencies'
    homepage = 'https://github.com/ocornut/imgui'
    license = 'MIT'
    url = 'https://github.com/conan-burrito/imgui'

    settings = 'os', 'arch', 'compiler', 'build_type'
    options = {
        'shared': [True, False],
        'fPIC': [True, False],
        'with_demo': [True, False]
    }
    default_options = {'shared': False, 'fPIC': True, 'with_demo': True}

    generators = 'cmake'
    exports_sources = ['patches/*', 'CMakeLists.txt', 'Config.cmake.in']

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    @property
    def source_subfolder(self):
        return os.path.join(self.source_folder, 'src')

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], destination='src', strip_root=True)
        for patch in self.conan_data["patches"][self.version]:
            tools.patch(**patch)

    def build(self):
        cmake = CMake(self)
        cmake.definitions['IMGUI_VERSION'] = str(self.version)
        cmake.definitions['IMGUI_SOVERSION'] = tools.Version(str(self.version)).major
        cmake.definitions['IMGUI_DEMO'] = 'ON' if self.options.with_demo else 'OFF'

        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="LICENSE.txt", dst="licenses", src=self.source_subfolder)

    def package_info(self):
        self.cpp_info.libs.append('imgui')

        self.cpp_info.names['cmake_find_package'] = 'IMGUI'
        self.cpp_info.names['cmake_find_package_multi'] = 'IMGUI'

        if self.settings.os == 'Linux':
            self.cpp_info.system_libs.append("m")

        bin_path = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH env var with : {}".format(bin_path))
        self.env_info.PATH.append(bin_path)
