"""all credit to Rafael Rayes"""
"""we advise you to use a powerfull IDE, otherwise this might take a while"""
def encode(your_image):
    try:
        from PIL import Image, ImageColor
        from tqdm import tqdm
        im = Image.open(your_image)
        imagename = im.filename
        imagename = imagename.replace('.jpg', '')
        imagename = imagename.replace('.png', '')
        im = im.convert('RGB')
        txt_filename = (str(imagename)+'.txt')
        save = open(txt_filename, "w")
        im = im.rotate(90)
        l = []
        l.append(im.width)
        l.append(im.height)
        for i in tqdm(range(im.width)):
                for j in range(im.height):
                        pixel = im.getpixel((i, j))
                        s = str(pixel)
                        l.append(s)
        save.writelines("%s\n" % line for line in l)
    except:
        print('something went wrong, we could not complete the action')
def decode(your_text_file):
    try:
        from PIL import Image, ImageColor
        import ast
        from tqdm import tqdm
        im = Image.open('black.png')
        im = im.convert('RGB')
        with open(your_text_file) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        im = im.resize((int(content[0]), int(content[1])))
        pixels = im.load()
        q = 2
        for i in tqdm(range(im.width)):
                for j in range(im.height):
                        s = ast.literal_eval(content[q])
                        pixels[i, j] = s
                        q +=1
        im = im.rotate(270)
        im.show()
    except:
        print('something went wrong, we could not complete the action')
decode('/Users/Rafa/Desktop/PP 2/blackhole.txt')