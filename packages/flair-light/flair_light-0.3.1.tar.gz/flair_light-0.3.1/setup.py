import io
import os
import shutil
import sys
import setuptools


NAME = "flair_light"
DESCRIPTION = "A lightweight version of Flair, the very simple framework for state-of-the-art NLP."
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "0.3.1"
REQUIRED = [
    "bpemb==0.2.9",
]


class UploadCommand(setuptools.Command):
    description = "Build and publish the package."
    user_options = list()

    @staticmethod
    def status(s):
        print(f"\033[1m{s}\033[0m")

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds...")
            shutil.rmtree("dist")
        except OSError:
            pass

        self.status("Building source and wheel distribution...")
        os.system(f"{sys.executable} setup.py sdist bdist_wheel")

        self.status("Uploading the package to PyPI via Twine...")
        os.system("twine upload dist/*")

        sys.exit()


setuptools.setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=REQUIRES_PYTHON,
    packages=setuptools.find_packages(exclude=("tests",)),
    install_requires=REQUIRED,
    include_package_data=True,
    package_data={"flair": ["embeddings/en/en.wiki.bpe.vs100000.model"]},
    license="MIT",
    cmdclass={
        "upload": UploadCommand,
    },
)
