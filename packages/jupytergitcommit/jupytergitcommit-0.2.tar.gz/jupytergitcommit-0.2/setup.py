import setuptools

setuptools.setup(
    name="jupytergitcommit",
    version='0.2',
    url="https://github.com/newellp2019/gitcommit",
    author="Peter Newell",
    description="Jupyter extension to enable user push notebooks to a git repo",
    packages=setuptools.find_packages(),
    install_requires=[
        'psutil',
        'notebook',
        'pygithub'
    ],
    package_data={'jupytergithubcommit': ['static/*']},
)
