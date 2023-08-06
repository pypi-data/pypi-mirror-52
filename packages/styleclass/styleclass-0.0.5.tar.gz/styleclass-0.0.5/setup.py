import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="styleclass",
    version="0.0.5",
    author="Crossref",
    author_email="labs@crossref.org",
    description="Citation style classifier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/crossref/citation_style_classifier",
    scripts=[
        "bin/styleclass_classify", "bin/styleclass_evaluate",
        "bin/styleclass_generate_dataset", "bin/styleclass_train_model"
    ],
    install_requires=[
        "scipy == 1.3.0", "numpy == 1.16.4", "pandas == 0.25.0",
        "scikit_learn == 0.21.2"
    ],
    packages=setuptools.find_packages(),
    package_data={
        '': ['datasets/*.csv', 'models/*'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
