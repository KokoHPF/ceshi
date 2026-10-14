import cv2, numpy as np, sys
from PIL import Image, ImageDraw, ImageFont
FONT='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
def region(shape, box):
    """box: (x0,y0,x1,y1) 轴对齐框，或 ((xa,ya),(xb,yb),半宽) 沿文字中线的斜框"""
    r=np.zeros(shape,np.uint8)
    if len(box)==4: cv2.rectangle(r,(box[0],box[1]),(box[2],box[3]),1,-1)
    else:
        (xa,ya),(xb,yb),h=box; v=np.array([xb-xa,yb-ya],float); n=np.array([-v[1],v[0]])/np.linalg.norm(v)*h
        pts=np.array([[xa,ya]+n,[xb,yb]+n,[xb,yb]-n,[xa,ya]-n],np.int32); cv2.fillPoly(r,[pts],1)
    return r
def center(box):
    if len(box)==4: return (box[0]+box[2])/2,(box[1]+box[3])/2
    (xa,ya),(xb,yb),_=box; return (xa+xb)/2,(ya+yb)/2
def mask_text(img, box, dark):
    """只把区域内的文字笔画（亮字或暗字）做掩膜，再修补"""
    g=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY); r=region(g.shape,box)
    sel=(g<70) if dark else (g>170)
    m=(sel&(r>0)).astype(np.uint8)*255
    m=cv2.dilate(m,np.ones((5,5),np.uint8),iterations=2)
    return m
def run(src,dst,labels):
    img=np.array(Image.open(src).convert('RGB'))
    M=np.zeros(img.shape[:2],np.uint8)
    for (box,txt,dark,size,ang) in labels: M|=mask_text(img,box,dark)
    out=cv2.inpaint(img,M,7,cv2.INPAINT_TELEA)
    pil=Image.fromarray(out)
    for (box,txt,dark,size,ang) in labels:
        cx,cy=center(box)
        f=ImageFont.truetype(FONT,size)
        fill=(30,30,30) if dark else (255,255,255); stroke=(255,255,255) if dark else (0,0,0)
        tmp=Image.new('RGBA',(size*len(txt)+40,size+40),(0,0,0,0)); d=ImageDraw.Draw(tmp)
        d.text((20,20),txt,font=f,fill=fill,stroke_width=2,stroke_fill=stroke+(160,))
        tmp=tmp.crop(tmp.getbbox()).rotate(ang,expand=True,resample=Image.BICUBIC)
        pil.paste(tmp,(int(cx-tmp.width/2),int(cy-tmp.height/2)),tmp)
    pil.save(dst)
L={
 'f2':[((715,625,1055,685),'皮下组织',True,44,0),(((862,810),(1220,758),24),'指伸肌',False,44,8),((70,856,395,914),'利斯特结节',False,40,0),((830,975,1055,1035),'舟骨',False,46,0),(((1272,1032),(1380,903),22),'小多角骨',False,38,50)],
 'f3':[((385,610,660,665),'皮下组织',True,42,0),((685,680,1000,725),'指伸肌',True,38,0),((190,825,325,875),'桡骨',False,42,0),((600,910,785,965),'舟骨',False,42,0),((1130,940,1300,990),'头状骨',False,40,0)],
 'f4':[((70,603,390,660),'皮下组织',True,44,0),((180,685,840,740),'指总伸肌',True,44,0),((73,913,230,967),'桡骨',False,44,0),((600,915,757,970),'月骨',False,44,0),((995,998,1190,1055),'头状骨',False,44,0)],
 'f5':[((5,255,168,304),'桡骨',False,44,0),((277,341,437,390),'月骨',False,44,0),((579,367,769,420),'头状骨',False,44,0)],
}
for k,v in L.items(): run(f'{k}.png',f'{k}_cn.png',v)
