from conans import ConanFile, CMake, tools
import os


class Recipe(ConanFile):
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"
    requires = [
        'SDL2/2.0.12@conan-burrito/stable',
        'glad/0.1.33@conan-burrito/stable',
    ]

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if tools.cross_building(self.settings):
            return

        self.run(os.path.join('bin', 'test'), run_environment=True)
