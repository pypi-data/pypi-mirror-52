import json
import os
import shutil
import subprocess


class PyPi:
    def __init__(self):
        with open('cvs_config.json') as config_file:
            self._config = json.load(config_file)

    def __checkout(self):
        command = f"""cvs -d {self._config['cvsroot']} checkout -P -r {self._config['branch']} -d {self._config['checkoutPath']} -- vaultcx/Source/tools/cvpysdk"""
        subprocess.run(command)

    def __build_package(self):
        setup_path = os.path.join(self._config['checkoutPath'], "setup.py")
        wheel_command = f"python {setup_path} bdist_wheel --universal"
        gztar_command = f"python {setup_path} sdist --formats=gztar"
        subprocess.run(wheel_command, check=True)
        subprocess.run(gztar_command, check=True)

    def __upload_to_test_repository(self):
        command = f"""twine upload --repository-url https://test.pypi.org/legacy/ dist/* -u {self._config['username']} -p {self._config['password']}"""
        subprocess.run(command)

    def __install_test_cvpysdk(self):
        shutil.rmtree("cvpysdk.egg-info")
        import cvpysdk
        command = f"python -m pip install --index-url https://test.pypi.org/simple/ cvpysdk=={cvpysdk.__version__}"
        subprocess.run(command)

    def __run_automation(self):
        command = f"python {self._config['automation_path']} --inputJSON C:\\inputs\\pypi.json"
        subprocess.run(command)

    def __upload_to_pypi(self):
        command = f"""twine upload dist/* -u {self._config[
            'username']} -p {self._config['password']}"""
        subprocess.run(command)

    def __install_cvpysdk(self):
        import cvpysdk
        command = f"python -m pip install  cvpysdk=={cvpysdk.__version__}"
        subprocess.run(command)

    def run(self):
        # self.__checkout()
        self.__build_package()
        self.__upload_to_test_repository()
        self.__install_test_cvpysdk()
        self.__run_automation()
        self.__upload_to_pypi()
        self.__install_cvpysdk()


if __name__ == "__main__":
    pypi = PyPi()
    pypi.run()
