from pythonforandroid.recipes.opencv_python import OpencvPythonRecipe


class OpencvContribPythonRecipe(OpencvPythonRecipe):
    name = "opencv-contrib-python"
    version = "4.9.0.80"
    url = "https://files.pythonhosted.org/packages/41/9e/1925ba4c7262d373d9b5d7e8bf7b666840ea17dc31bf9a018de795011dea/opencv-contrib-python-4.9.0.80.tar.gz"

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        env["ENABLE_CONTRIB"] = "1"
        return env


recipe = OpencvContribPythonRecipe()
