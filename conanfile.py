#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class LibLinearConan(ConanFile):
    name = "liblinear"
    version = "2.20"
    description = "A Library for Large Linear Classification"
    url = "https://github.com/bincrafters/conan-liblinear"
    homepage = "https://www.csie.ntu.edu.tw/~cjlin/liblinear/"
    license = "BSD-3-Clause"
    author = "Bincrafters <bincrafters@gmail.com>"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True",
    source_subfolder = "source_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "https://github.com/cjlin1/liblinear"
        github_version = self.version.replace(".", "")
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, github_version))
        extracted_dir = self.name + "-" + github_version
        os.rename(extracted_dir, self.source_subfolder)

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.configure()
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="COPYRIGHT", dst="licenses", src=self.source_subfolder)
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
