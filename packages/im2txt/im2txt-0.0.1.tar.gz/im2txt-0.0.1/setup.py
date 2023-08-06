import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="im2txt",
    version="0.0.1",
    author="Rafael Rayes",
    author_email="rafa@rayes.com.br",
    description="Encode images in form of text and decode again!!",
    long_description="""
'''
first import the package on your terminal with pip:
```
pip3 install im2txt
```
next you import the module:
```
import im2txt
```
now you just need to encode the image of your preference:
```
im2txt.encode('/path/to/image/pooptest.jpg')
```
you will receive a ```pooptest.txt``` file.
This file will have the pixel value of all pixels on the image.

To decode the .txt file back to an image we use:
```
im2txt.decode('path/to/txtfile/pooptest.txt')
```
you will receive the encoded image back again in form of .png!

""",
    long_description_content_type="text/markdown",
    url="https://github.com/rrayes3110",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
