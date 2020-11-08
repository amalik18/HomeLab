import setuptools
rt setuptools

with open("README.md", "r") as fh:
        long_description = fh.read()

        setuptools.setup(
                    name="Django-HomeLab", # Replace with your own username
                        version="0.0.1",
                            author="Ali Malik",
                                author_email="ali_malik96@yahoo.com",
                                    description="First Django test Project",
                                        long_description=long_description,
                                            long_description_content_type="text/markdown",
                                                url="https://github.com/amalik18/HomeLab",
                                                    packages=setuptools.find_packages(),
                                                        classifiers=[
                                                                    "Programming Language :: Python :: 3",
                                                                            "License :: OSI Approved :: MIT License",
                                                                                    "Operating System :: OS Independent",
                                                                                        ],
                                                            python_requires='>=3.6',
                                                            )

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Django-HomeLab", # Replace with your own username
    version="0.0.1",
    author="Ali Malik",
    author_email="ali_malik96@yahoo.com",
    description="First Django test project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amalik18/HomeLab",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
