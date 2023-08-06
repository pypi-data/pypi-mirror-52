import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="app_utils",
    version="0.1a2",
    author="Patrick Shinn",
    author_email="shinn5112@gmail.com",
    description="A collection of reusable utility functions to aid in rapid application development.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    platform=["Linux", "OSX", "Windows"],
    url="https://gitlab.com/shinn5112/app_utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
    ],
    python_requires='>=3.5',
)
