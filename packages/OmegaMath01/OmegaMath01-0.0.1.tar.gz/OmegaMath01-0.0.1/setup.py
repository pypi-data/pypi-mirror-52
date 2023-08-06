import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OmegaMath01",
    version="0.0.1",
    author="Quantum_Wizard",
    author_email="minecraftcrusher100@gmail.com",
    description="A small package of useful miscellaneuos functions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GrandMoff100/MathFunctions",
    packages=setuptools.find_packages(include=["turtle","time","math"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
