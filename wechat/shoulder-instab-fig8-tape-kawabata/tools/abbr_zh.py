import sys, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
FONT='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
def tight(g, box, thr=190):
    x0,y0,x1,y1=box; w=g[y0:y1,x0:x1]>thr; ys,xs=np.nonzero(w)
    return (x0+xs.min(), y0+ys.min(), x0+xs.max()+1, y0+ys.max()+1)
def run(src, out, items, fs, thr=190):
    img=np.array(Image.open(src).convert('RGB')); g=img.mean(2)
    mask=np.zeros(g.shape,np.uint8); tb=[]
    for box,t in items:
        b=tight(g,box,thr); tb.append((b,t)); x0,y0,x1,y1=b
        mask[y0-3:y1+3,x0-3:x1+3]=((g[y0-3:y1+3,x0-3:x1+3]>120)*255).astype(np.uint8)
    mask=cv2.dilate(mask,np.ones((3,3),np.uint8),iterations=2)
    img=cv2.inpaint(img,mask,5,cv2.INPAINT_TELEA)
    im=Image.fromarray(img); dr=ImageDraw.Draw(im); f=ImageFont.truetype(FONT,fs)
    for (x0,y0,x1,y1),t in tb:
        dr.text(((x0+x1)/2,(y0+y1)/2),t,font=f,fill=(255,255,255),anchor='mm',stroke_width=2,stroke_fill=(0,0,0))
    im.save(out); return tb
