import glob
from logging import info
from os.path import join

import sh

from pythonforandroid.logger import shprint
from pythonforandroid.recipe import CompiledComponentsPythonRecipe
from pythonforandroid.util import current_directory


class OpencvPythonRecipe(CompiledComponentsPythonRecipe):
    name = "opencv-python"
    version = "4.9.0.80"
    url = "https://files.pythonhosted.org/packages/25/72/da7c69a3542071bf1e8f65336721b8b2659194425438d988f79bc14ed9cc/opencv-python-4.9.0.80.tar.gz"
    depends = ["setuptools", "numpy"]
    patches = ["patches/p4a_build.patch"]
    hostpython_prerequisites = ["scikit-build", "packaging", "wheel"]
    call_hostpython_via_targetpython = False

    def build_arch(self, arch):
        self.install_hostpython_prerequisites()
        super().build_arch(arch)

    def build_compiled_components(self, arch):
        info('Building compiled components in {}'.format(self.name))

        env = self.get_recipe_env(arch)
        hostpython = sh.Command(self.hostpython_location)
        with current_directory(self.get_build_dir(arch.arch)):
            if self.install_in_hostpython:
                shprint(hostpython, 'setup.py', 'clean', '--all', _env=env)
            shprint(hostpython, 'setup.py', self.build_cmd, '-v',
                    _env=env, *self.setup_extra_args)

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        env["ANDROID_NDK"] = self.ctx.ndk_dir
        env["ANDROID_SDK"] = self.ctx.sdk_dir

        python_major = self.ctx.python_recipe.version[0]
        python_include_root = self.ctx.python_recipe.include_root(arch.arch)
        python_site_packages = self.ctx.get_site_packages_dir(arch)
        python_link_root = self.ctx.python_recipe.link_root(arch.arch)
        python_link_version = self.ctx.python_recipe.link_version
        python_library = join(
            python_link_root, "libpython{}.so".format(python_link_version)
        )
        python_include_numpy = join(python_site_packages, "numpy", "core", "include")

        cmake_args = [
            "-DANDROID=ON",
            "-DWITH_IPP=OFF",
            "-DWITH_ITT=OFF",
            "-DWITH_TIFF=OFF",
            "-DWITH_JASPER=OFF",
            "-DWITH_OPENEXR=OFF",
            "-DWITH_WEBP=OFF",
            "-DBUILD_ANDROID_PROJECTS=OFF",
            "-DBUILD_ANDROID_EXAMPLES=OFF",
            "-DBUILD_TESTS=OFF",
            "-DBUILD_PERF_TESTS=OFF",
            "-DENABLE_TESTING=OFF",
            "-DBUILD_EXAMPLES=OFF",
            "-DANDROID_ABI={}".format(arch.arch),
            "-DANDROID_STANDALONE_TOOLCHAIN={}".format(self.ctx.ndk_dir),
            "-DANDROID_NATIVE_API_LEVEL={}".format(self.ctx.ndk_api),
            "-DANDROID_EXECUTABLE={}/tools/android".format(env["ANDROID_SDK"]),
            "-DANDROID_SDK_TOOLS_VERSION=6514223",
            "-DANDROID_PROJECTS_SUPPORT_GRADLE=ON",
            "-DCMAKE_TOOLCHAIN_FILE={}".format(
                join(self.ctx.ndk_dir, "build", "cmake", "android.toolchain.cmake")
            ),
            "-DOPENCV_FORCE_PYTHON_LIBS=ON",
            "-DPYTHON{major}_INCLUDE_PATH={include_path}".format(
                major=python_major, include_path=python_include_root
            ),
            "-DPYTHON{major}_LIBRARIES={python_lib}".format(
                major=python_major, python_lib=python_library
            ),
            "-DPYTHON{major}_NUMPY_INCLUDE_DIRS={numpy_include}".format(
                major=python_major, numpy_include=python_include_numpy
            ),
        ]

        env["CMAKE_ARGS"] = " ".join(cmake_args)
        return env


recipe = OpencvPythonRecipe()
