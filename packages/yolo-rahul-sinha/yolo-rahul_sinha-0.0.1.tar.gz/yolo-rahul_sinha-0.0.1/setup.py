import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yolo-rahul_sinha",
    version="0.0.1",
    author="Rahul Sinha",
    author_email="rsnasa4@gmail.com",
    description="Yolo implementation on a given picture using Opencv",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aamras/yolo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)