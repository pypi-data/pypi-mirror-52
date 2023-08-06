import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Quantum_Ciphers",
    version="3.0.0",
    author="Quantum_Wizard",
    author_email="minecraftcrusher100@gmail.com",
    description="""A package of diffenent easy-to-use text ciphers.""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GrandMoff100/Quantum_Cipher2",
    packages=setuptools.find_packages(include=["quantum_ciphers"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.7',
    install_requires=['omegamath01',"antigravity"],
)
