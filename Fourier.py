import pygame
import math

def toPolar(x,y):
    (t,r)=(math.atan2(y,x),math.sqrt(math.pow(x,2)+math.pow(y,2)))
    return (t,r)
def toRect(t,r):
    (x,y)=(r*math.cos(t),r*math.sin(t))
    return (x,y)
def zoomT(x,y,zoom):
    (mx,my)=(0,0)
    (t,r)=toPolar(x-mx,y-my)
    (rx,ry)=toRect(t,r*zoom)
    return (rx+mx,ry+my)

def dft(xvals,yvals):
    X = {}
    Num = len(xvals)
    for k in range (0,Num):
        re = 0
        im = 0
        
        for n in range(0,Num):
            angle = (2*math.pi*k*n)/Num

            re += (yvals[n] * math.cos(angle)) - (xvals[n] * math.sin(angle))
            im += (xvals[n] * math.cos(angle)) + ((yvals[n]) * math.sin(angle))

        re = re/Num
        im = im/Num

        rad = math.sqrt((re*re) + (im*im))
        freq = k
        ph = math.atan2(im,re)
        
        X[k] = {'radius':rad, 'frequency':freq, 'phase':ph}
        
    return X



backgroundColor = (0,0,0)
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
(width, height) = (1000,600)


screen = pygame.display.set_mode((width, height))
screen.fill(backgroundColor)

pygame.display.flip()
pygame.display.set_caption("Fourier")


restart = False

pointsx = []
pointsy = []

samplex = []
sampley = []

fourier = []

wavex = []
wavey = []



zoom = 1

(cX,cY) = (0,0)

running = True
time = 0

sampling = True

sampleper = 1

first = True

(mxp,myp)=(0,0)


while running:
    if restart == True:
        pointsx = []
        pointsy = []

        samplex = []
        sampley = []

        fourier = []

        wavex = []
        wavey = []
        restart = False
        sampling = True
        sampleper = 1
        time = 0
        screen.fill(backgroundColor)
        zoom = 1
        (cX,cY) = (0,0)
        (mxp,myp)=(0,0)

    

    (m1,m2,m3) = pygame.mouse.get_pressed()
    (mx,my) = pygame.mouse.get_pos()

    if(sampling and m1):
        pygame.draw.circle(screen, red, (mx,my), 2)
        samplex.append(-mx)
        sampley.append(my)

    if(len(samplex)>0):
        sampleper =  round (len(samplex)/(800*math.log((len(samplex)+800)/800))+.3)
        
    if(m3 == True and sampling == True and len(samplex)>0):
        sampling = False
        
        
        
        
        
        sampleper =  round (len(samplex)/(1000*math.log((len(samplex)+1000)/1000))+.4)


            
        for i in range(0,len(samplex)):
            if(i%sampleper == 0):
                pointsx.insert(0,samplex[i])
                pointsy.insert(0,sampley[i])
                
        fourier = dft(pointsx,pointsy)

        
    if(sampling == False):
        if(m2==False):
            first = True
            (mxp,myp)=(cX,cY)        
        if(m2 and first):
            first = False
            (mxp,myp)=pygame.mouse.get_pos()
            (mxp,myp)=(mxp-cX,myp-cY)

        if(m2):
            (cX,cY)=(mx-mxp,my-myp)

    if(zoom<1):
        zoom = 1
        





    
        

        
    




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart = True
            if (event.key == pygame.K_o and sampling == False):
                zoom-=.01
            if (event.key == pygame.K_p and sampling == False):
                zoom+=.01

    

    

    x = 0
    y = 0
    if (sampling==False):

        screen.fill(backgroundColor)
        for i in range(0,len(fourier)):
            prevx = x
            prevy = y

            
            freq = fourier[i]['frequency']
            radius = fourier[i]['radius']*zoom
            phase = fourier[i]['phase']

            (ccx,ccy)=zoomT(cX+x,cY+y,zoom)

            if (round(radius)>=1):
                pygame.draw.circle(screen, white, (round(ccx),round(ccy)), round(radius),1)
            
            
            
            x += radius * math.cos(freq*time + phase + math.pi/2)
            y += radius * math.sin(freq*time + phase + math.pi/2)

            

            pygame.draw.line(screen, white, (round(prevx+cX),round(prevy+cY)), (round(x+cX),round(y+cY)))
            

        

        
        

        wavey.insert(0,y)
        wavex.insert(0,x)

        if (len(wavey)>3000):
            wavey.pop()
            wavex.pop()
            
        for i in range(1,len(wavey)):
         
            (ppx,ppy) = zoomT(wavex[i-1]+cX, wavey[i-1]+cY,zoom)
            (px,py) = zoomT(wavex[i]+cX,wavey[i]+cY,zoom)
            pygame.draw.line(screen, red, (round(ppx),round(ppy)),(round(px),round(py)),3)



        dt = (2*math.pi)/len(fourier)
        time += dt

        
        

    


        
    

    pygame.display.update()


    
pygame.quit()
