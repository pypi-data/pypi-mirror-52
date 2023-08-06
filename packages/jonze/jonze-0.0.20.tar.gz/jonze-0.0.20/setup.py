import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jonze",
    version="0.0.20",
    author="Zeio Nara",
    author_email="zeionara@gmail.com",
    description="Reusable Joint Slot and Intent Extraction implementation in Tensorflow2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zeionara/jonze",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)