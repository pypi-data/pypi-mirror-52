import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-indices",
    version="0.0.4.post2",
    author="Jatinderjit Singh",
    author_email="jatinderjit89@gmail.com",
    description="Create JSON indexes concurrently",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jatinderjit/django-indices",
    packages=setuptools.find_packages(),
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
