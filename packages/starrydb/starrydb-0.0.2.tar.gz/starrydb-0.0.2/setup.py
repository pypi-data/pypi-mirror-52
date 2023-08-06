import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="starrydb",
    version="0.0.2",
    author="Luo Xi",
    author_email="rossi913@163.com",
    description="A NoSQL lightweight database.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/luoxi-github/starrydb",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["msgpack", "pylibmc"],
)
