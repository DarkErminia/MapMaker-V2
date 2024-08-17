from PIL import Image, ImageDraw
from random import randint, random
from numpy import asarray, array

def pixel(canvas,x,y,intensity):
    global xsize
    global ysize
    if y>=0 and y<=ysize-1:
        if x>=0 and x<=xsize-1:
            canvas[y][x]+=intensity


def ellipse(canvas,x,y,r,rx,intensity):
    global xsize
    global ysize
    k=rx/r
    m=0
    n=0
    while m<=rx:
        if ((m/k+1/2))**2+(n+1/2)**2-r**2<=0:
            if m==0 and n==0:
                pixel(canvas,x,y,intensity)
            elif m==0:
                pixel(canvas,x,y+n,intensity)
                pixel(canvas,x,y-n,intensity)
            elif n==0:
                pixel(canvas,x+m,y,intensity)
                pixel(canvas,x-m,y,intensity)
            else:
                pixel(canvas,x+m,y+n,intensity)
                pixel(canvas,x+m,y-n,intensity)
                pixel(canvas,x-m,y+n,intensity)
                pixel(canvas,x-m,y-n,intensity)
            n+=1
        else:
            m+=1
            n=0
                

def circle(): #R stands for radius
    global xsize
    global ysize
    rand=randint(0,1)
    equator=round(ysize/2,0)
    x=randint(0,xsize)
    y=randint(1,ysize-1)
    r=randint(1,round(ysize/6,0))
    rx=min(r*abs((equator)/(equator-abs(y-equator))),xsize) #Distortion of x around poles
    rx=max(0.0001,rx)
    i=r/rx
    rand=randint(0,1)
    if rand==1:
        i=-i
    if x-rx<0:
        ellipse(hmap,xsize+x,y,r,rx,i)
    if x+rx>xsize:
        ellipse(hmap,x-xsize,y,r,rx,i)
    ellipse(hmap,x,y,r,rx,i)


while True:
    print("This program creates equirectangular world maps.")
    print()
    print("What height should the map be? (The width will be 2x the height.)")
    print("500 is a good number. Increasing will increase waiting time exponentially.")
    try:
        ysize=int(input("Map Y Height: "))
    except:
        print("Please use positive numbers only.")
        break
    if ysize<10:
        print("Try using a larger size.")
        break
    xsize=ysize*2
    print("How much detail do you want?")
    print("(4000 is a good amount.)")
    try:
        num=int(input("Detail amount: "))
    except:
        print("Please use positive numbers only.")
        break
    hmap=[0]*xsize
    hmap=[hmap]*ysize
    hmap=Image.new(mode = "L",size = (xsize, ysize),color=0)
    hmap=asarray(hmap).astype('float64')
    for x in range(0,num):
        circle()
        rand=randint(1,50)
        if rand==1:
            print("Progress:",round(100*x/num,2),"%")
    maxvalue=0
    for y in range(0,len(hmap)):
        for x in range(0, len(hmap[y])):
            if hmap[y][x]>maxvalue:
                maxvalue=hmap[y][x]
    minvalue=0
    for y in range(0,len(hmap)):
        for x in range(0, len(hmap[y])):
            if hmap[y][x]<minvalue:
                minvalue=hmap[y][x]
    for y in range(0,len(hmap)):
        for x in range(0, len(hmap[y])):
            hmap[y][x]=round((hmap[y][x]-minvalue)*255/(maxvalue-minvalue),0)
    hmap=hmap.astype('uint8')
    hmap=Image.fromarray(hmap)
    hmap.show()

    print("Map complete.")
    print("This is a height map. Use magic wand to click on the lighter")
    print("or darker portions to find continents and such.")
    print()


