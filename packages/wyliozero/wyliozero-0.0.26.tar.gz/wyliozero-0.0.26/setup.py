import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wyliozero",
    version="0.0.26",
    author="Serban Razvan",
    author_email="razvan.serban@wyliodrin.com",
    description="Library for Wyliodrin Lab",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Wyliodrin/wyliozero",
    packages=setuptools.find_packages(),
    install_requires= ['gpiozero', 'Adafruit_DHT', 'pymata_aio', 'RPi.GPIO', 'Adafruit_CharLCD'],
    classifiers=[
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Unix",
        "Topic :: Education"
    ],
    python_requires='>=3.6'
)
