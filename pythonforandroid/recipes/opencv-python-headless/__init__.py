from pythonforandroid.recipes.opencv_python import OpencvPythonRecipe


class OpencvPythonHeadlessRecipe(OpencvPythonRecipe):
    name = "opencv-python-headless"
    version = "4.9.0.80"
    url = "https://files.pythonhosted.org/packages/3d/b2/c308bc696bf5d75304175c62222ec8af9a6d5cfe36c14f19f15ea9d1a132/opencv-python-headless-4.9.0.80.tar.gz"

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        env["ENABLE_HEADLESS"] = "1"
        return env


recipe = OpencvPythonHeadlessRecipe()
