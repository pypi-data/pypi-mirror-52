"""
Setup Module for the Download folder as archive Plugin.
"""
import setuptools
from setupbase import create_cmdclass, ensure_python, find_packages, get_version

package_data_spec = {
    "jupyterlab_downloadfolder": []
}


data_files_spec = [
    (
        "etc/jupyter/jupyter_notebook_config.d",
        "jupyter-config/jupyter_notebook_config.d",
        "jupyterlab_downloadfolder.json",
    )
]

cmdclass = create_cmdclass(
    package_data_spec=package_data_spec, data_files_spec=data_files_spec
)

with open("README.md") as readme_file:
    readme = readme_file.read()

setup_dict = dict(
    name="jupyterlab_downloadfolder",
    version=get_version("jupyterlab_downloadfolder/_version.py"),
    description="Plugin JupyterLab for Downloading a folder as archive",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Frederic Collonval",
    author_email="fcollonval@gmail.com",
    url="https://github.com/fcollonval/jupyterlab-download-folder",
    license="MIT",
    packages=find_packages(),
    keywords=["jupyterlab"],
    include_package_data=True,
    install_requires=["jupyterlab"],
    cmdclass=cmdclass,
    python_requires=">=3.5",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    zip_safe=False,
)

try:
    ensure_python(setup_dict["python_requires"].split(","))
except ValueError as e:
    raise ValueError(
        "{:s}, to use {} you must use python {} ".format(
            e, setup_dict["name"], setup_dict["python_requires"]
        )
    )

setuptools.setup(**setup_dict)
