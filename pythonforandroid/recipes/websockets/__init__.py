from pythonforandroid.recipe import CompiledComponentsPythonRecipe


class WebsocketsRecipe(CompiledComponentsPythonRecipe):
    name = "websockets"
    version = "12.0"
    url = "https://github.com/python-websockets/websockets/archive/{version}.tar.gz"
    depends = ["setuptools"]
    call_hostpython_via_targetpython = False

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        return env


recipe = WebsocketsRecipe()
