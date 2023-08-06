import setuptools

setuptools.setup(
    name="jupytergitcommit",
    version='1.0',
    url="https://github.com/newellp2019/jupytergitcommit",
    author="Peter Newell",
    description="Jupyter extension to enable user push notebooks to a git repo",
    packages=setuptools.find_packages(),
    install_requires=[
        'psutil',
        'notebook',
        'pygithub'
    ],
    package_data={'jupytergitcommit': ['static/*']},
    include_package_data=True,
)
