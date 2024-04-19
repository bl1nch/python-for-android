import glob
import shutil
from multiprocessing import cpu_count

import sh

from pythonforandroid.logger import info, shprint
from pythonforandroid.recipe import CompiledComponentsPythonRecipe
from pythonforandroid.util import current_directory


class NumpyRecipe(CompiledComponentsPythonRecipe):

    version = "1.26.4"
    url = "https://files.pythonhosted.org/packages/65/6e/09db70a523a96d25e115e71cc56a6f9031e7b8cd166c1ac8438307c14058/numpy-1.26.4.tar.gz"
    site_packages_name = "numpy"
    depends = ["cython"]
    hostpython_prerequisites = ["setuptools"]

    install_in_hostpython = True
    call_hostpython_via_targetpython = False

    patches = [
        "patches/p4a.patch",
    ]

    def get_recipe_env(self, arch=None, with_flags_in_cc=True):
        env = super().get_recipe_env(arch, with_flags_in_cc)

        # _PYTHON_HOST_PLATFORM declares that we're cross-compiling
        # and avoids issues when building on macOS for Android targets.
        env["_PYTHON_HOST_PLATFORM"] = arch.command_prefix

        # NPY_DISABLE_SVML=1 allows numpy to build for non-AVX512 CPUs
        # See: https://github.com/numpy/numpy/issues/21196
        env["NPY_DISABLE_SVML"] = "1"
        env["MATHLIB"] = "m"
        env["SETUPTOOLS_USE_DISTUTILS"] = "stdlib"
        
        return env

    def build_arch(self, arch):
        self.install_hostpython_prerequisites()
        super().build_arch(arch)

    def _build_compiled_components(self, arch):
        info("Building compiled components in {}".format(self.name))

        env = self.get_recipe_env(arch)
        with current_directory(self.get_build_dir(arch.arch)):
            hostpython = sh.Command(self.hostpython_location)
            shprint(
                hostpython,
                "setup.py",
                self.build_cmd,
                "-v",
                _env=env,
                *self.setup_extra_args
            )
            build_dir = glob.glob("build/lib.*")[0]
            shprint(
                sh.find,
                build_dir,
                "-name",
                '"*.o"',
                "-exec",
                env["STRIP"],
                "{}",
                ";",
                _env=env,
            )

    def _rebuild_compiled_components(self, arch, env):
        info("Rebuilding compiled components in {}".format(self.name))

        hostpython = sh.Command(self.real_hostpython_location)
        shprint(hostpython, "setup.py", "clean", "--all", "--force", _env=env)
        shprint(
            hostpython,
            "setup.py",
            self.build_cmd,
            "-v",
            _env=env,
            *self.setup_extra_args
        )

    def build_compiled_components(self, arch):
        self.setup_extra_args = ["-j", str(cpu_count())]
        self._build_compiled_components(arch)
        self.setup_extra_args = []

    def rebuild_compiled_components(self, arch, env):
        self.setup_extra_args = ["-j", str(cpu_count())]
        self._rebuild_compiled_components(arch, env)
        self.setup_extra_args = []

    def get_hostrecipe_env(self, arch):
        env = super().get_hostrecipe_env(arch)
        env["RANLIB"] = shutil.which("ranlib")
        env["SETUPTOOLS_USE_DISTUTILS"] = "stdlib"
        return env


recipe = NumpyRecipe()
