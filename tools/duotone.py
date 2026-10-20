import sys
from PIL import Image, ImageOps, ImageEnhance
# Тонирование в оранжевый «как у Velowave»: тени тёмно-коричневые, середина оранжевая, светлые места персиковые
STOPS=[(0,(34,9,2)),(0.38,(150,40,6)),(0.62,(240,104,26)),(0.85,(255,170,90)),(1,(255,226,190))]
def lut():
    out=[]
    for c in range(3):
        for i in range(256):
            t=i/255
            for (a,ca),(b,cb) in zip(STOPS,STOPS[1:]):
                if a<=t<=b:
                    k=(t-a)/(b-a); out.append(round(ca[c]+(cb[c]-ca[c])*k)); break
    return out
def duo(src,dst,w,contrast=1.15,q=78):
    im=Image.open(src).convert('RGB')
    if im.width>w: im=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
    g=ImageOps.grayscale(im); g=ImageOps.autocontrast(g,cutoff=1); g=ImageEnhance.Contrast(g).enhance(contrast)
    Image.merge('RGB',(g,g,g)).point(lut()).save(dst,quality=q,optimize=True,progressive=True)
if __name__=='__main__':
    duo(sys.argv[1],sys.argv[2],int(sys.argv[3]))
