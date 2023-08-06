import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyap_tdk",
    version="0.0.3",
    author="TDK",
    author_email="author@example.com",
    description="A package to integrate with the Yap tool",
    long_description="A package to integrate with the Yap tool",
    long_description_content_type="text/markdown",
    url="https://github.com/TechnionTDK/pyap",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)