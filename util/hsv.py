import Image, colorsys
def convert2hsv(im):
    if not isinstance(im, Image.Image):
        im = Image.open(im)
    im = im.convert('RGB')
    R, G, B = im.split()
    H, L, S = [], [], []
    for r, g, b in zip(R.getdata(), G.getdata(), B.getdata()):
        h, l, s = colorsys.rgb_to_hls(r/255., g/255., b/255.)
        H.append(int(h*255.))
        L.append(int(l*255.))
        S.append(int(s*255.))
    R.putdata(H)
    G.putdata(L)
    B.putdata(S)
    return Image.merge('RGB', (R, G, B))

def test():
    path = '../static/dataset/simpcity/0.jpg'
    im = Image.open(path)
    im.show()
    im2 = convert2hsv(im)
    im2.show()

if __name__ == '__main__':
    test()

    
