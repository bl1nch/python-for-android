from pythonforandroid.recipes.opencv_python import OpencvPythonRecipe


class OpencvContribPythonHeadlessRecipe(OpencvPythonRecipe):
    name = "opencv-contrib-python-headless"
    version = "4.9.0.80"
    url = "https://files.pythonhosted.org/packages/3a/70/72ee1fb68f197755b90550b3d13006506d5e4a1b0a0ec6e1bbbb6000884c/opencv-contrib-python-headless-4.9.0.80.tar.gz"

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        env["ENABLE_CONTRIB"] = "1"
        env["ENABLE_HEADLESS"] = "1"
        return env


recipe = OpencvContribPythonHeadlessRecipe()
