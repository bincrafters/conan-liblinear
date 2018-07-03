#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os
import glob


class LibLinearConan(ConanFile):
    name = "liblinear"
    version = "2.20"
    github_version = "220"
    description = "A Library for Large Linear Classification"
    url = "https://github.com/konijnendijk/conan-libname"
    homepage = "https://www.csie.ntu.edu.tw/~cjlin/liblinear/"
    license = "BSD-3-Clause"
    author = "Bincrafters <bincrafters@gmail.com>"
    exports = ["LICENSE.md"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"fPIC": [True, False]}
    default_options = "fPIC=True",
    source_subfolder = "source_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "https://github.com/cjlin1/liblinear"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.github_version))
        extracted_dir = self.name + "-" + self.github_version
        os.rename(extracted_dir, self.source_subfolder)
        files = glob.glob("{0}/windows/*".format(self.source_subfolder))
        for f in files:
            os.remove(f)

    def system(self, command):
        retcode = os.system(command)
        if retcode != 0:
            raise Exception("Error while executing:\n\t %s" % command)

    def linux_build(self):
        with tools.chdir(self.source_subfolder):
            autotools = AutoToolsBuildEnvironment(self)
            autotools.make(args=["lib"])
            os.symlink("liblinear.so.3", "liblinear.so")

    def windows_build(self):
        cflags = ["/nologo", "/EHsc", "/I.", "/D _CRT_SECURE_NO_DEPRECATE"]
        cflags.append("/{0}".format(self.settings.compiler.runtime))
        if self.settings.build_type == "Debug":
            cflags.append("/DEBUG")
        else:
            cflags.append("/O2")
        self.system('cd {0} && nmake /F Makefile.win CFLAGS="{1}" lib'.format(self.source_subfolder, " ".join(cflags)))

    def build(self):
        if self.settings.os == "Linux":
            self.linux_build()
        elif self.settings.compiler == "Visual Studio":
            self.windows_build()
        else:
            raise Exception("OS or compiler not supported")

    def package(self):
        self.copy(pattern="COPYRIGHT", dst="licenses", src=self.source_subfolder)
        self.copy(pattern="linear.h", dst="include", src=self.source_subfolder)
        self.copy(pattern="tron.h", dst="include", src=self.source_subfolder)
        self.copy(pattern="liblinear.so*", dst="lib", keep_path=False, symlinks=True, src=self.source_subfolder)
        self.copy(pattern="liblinear.lib", dst="lib", keep_path=False, src=self.source_subfolder + "/windows")
        self.copy(pattern="liblinear.dll", dst="bin", keep_path=False, src=self.source_subfolder + "/windows")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
