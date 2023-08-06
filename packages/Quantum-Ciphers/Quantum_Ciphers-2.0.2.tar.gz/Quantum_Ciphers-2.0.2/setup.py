import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Quantum_Ciphers",
    version="2.0.2",
    author="Quantum_Wizard",
    author_email="minecraftcrusher100@gmail.com",
    description="""A package of diffenent easy-to-use text ciphers.""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GrandMoff100/Quantum_Cipher2",
    packages=setuptools.find_packages(include=["Quantum_Ciphers","ciphers"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
    install_requires=['omegamath01',"antigravity"],
)
