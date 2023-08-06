This package was made bu Rafael Rayes, contact via rafa@rayes.com.br

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