import setuptools


if __name__ == "__main__":
    setuptools.setup(
        name="boi-balance",
        author="Senan Kelly",
        author_email="senan@senan.xyz",
        description="command line tool to get a bank of ireland balance",
        url="https://github.com/sentriz/boi-balance",
        version="0.0.1",
        packages=setuptools.find_packages(),
        install_requires=["requests-html==0.10.0"],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        scripts=["boi-balance"],
    )
