import pyaudio
import numpy
import audioop

import threading
from queue import Queue

from sense_hat import SenseHat
from time import sleep
import random

#declares
sense = SenseHat()
sense.low_light = True

W = (255, 255, 255)
P = (0, 0, 0)
R = (255, 0, 0)
G = (0, 255, 0)


def move_marble(audio, x, y):
    new_x = x
    new_y = y
    # if 0 < audio < 50:
    #     new_x -= 1
    # elif 359 > pitch > 179:
    #     new_x += 1
    if audio < 50:
        new_y += -1
    elif 50 < audio < 250:
        new_y += 1
    elif 250 < audio < 500:
        new_y += 2       
    x,y = check_wall(x, y, new_x, new_y)
    return x,y

def check_wall(x, y, new_x, new_y):
    if (new_x >= 0 and new_y >= 1) and (new_x >= 0 and new_y <= 7) and (new_x <= 7 and new_y >= 1) and (new_x <= 7 and new_y <= 7):
        return new_x, new_y
    # elif (new_x < 0 and new_y > 0) and (new_x < 0 and new_y < 7):
    #     return x + 2, new_y
    # elif (new_x > 7 and new_y > 0) and (new_x > 7 and new_y < 7):
    #     return x - 2, new_y
    elif (new_x > 0 and new_y < 1) and (new_x < 7 and new_y < 1):
        return new_x, y
    elif (new_x > 0 and new_y > 7) and (new_x < 7 and new_y > 7):
        return new_x, y - 1
    return x,y

def floor0(floorx):
    startfloor = True
    while True:
        floory = 0
        delay = 1
        wait = 0
        newsize = 0

        if(wait == 0):
            if(startfloor == True):
                floorx = [0, 1, 2, 3, 4 , 5, 6, 7]
                startfloor = False
            else:#like snake moving
                for i in range((len(floorx) - 1), 0, -1):
                    floorx[i] = floorx[i - 1]
            
            print('First Length check: ', len(floorx))
            #give color        
            for i in range((len(floorx) - 1) ,-1 ,-1):
                maze[floory][floorx[i]] = G

            sleep(delay)
            
            print('Second Length check: ', len(floorx))
            #clear color
            for i in range((len(floorx) - 1) ,-1 ,-1):
                maze[floory][floorx[i]] = P    
            
            floorx[0] -= 1 #move forward

            #when respawn floor, above -1 already = now floorx(0) = [6], append and give newbie value from #like snake moving 
            if(newsize > 0):
                floorx.append(0)
                newsize -= 1
            
            # print('before pop Length: ', len(floorx))
            # floorx.pop(0)
            # print('after pop Length: ', len(floorx))
            print('floorx 0: ', floorx[0])
            if(floorx[0] < 0):
                if(len(floorx) == 0):#late respawn value for random pattern   
                    wait = random.randint(0, 7)
                else:#what is strange
                    floorx.pop(0)
                    print('Length check: ', len(floorx))
                    
        else:
            wait -= 1 
            if(wait == 0):
                floorx.append(7)
                newsize = random.randint(2, 7)
            sleep(delay)


def moveFood(foodx, foody, notexq, noteyq):
    while True:

        delay = 0.05
        randomFood = False
        #delayDecrease = -0.002

        notex = notexq.get()
        notey = noteyq.get()
        
        #when food ate
        if ((foodx == notex or foodx == notex+1) and (foody == notey)):
            randomFood = True
            #delay += delayDecrease

        #spawn new food
        if randomFood:
            randomFood = False
            retry = True
            while retry:
                foodx = random.randint(3, 7)
                foody = random.randint(3, 7)
                retry = False

        #print('note(x,y): ',notex, '  ', notey)
        #print('food(x,y): ',foodx, '  ', foody)
        if(foodx <= 0):
            foodx = 7
        elif(foodx > 0):
            foodx -= 1

        maze[foody][foodx] = R
        sleep(delay)
        maze[foody][foodx] = P

def marble(notex, notey, notexq, noteyq):
    while True:
        delay = 0.05
        
        # Read audio
        raws=stream.read(1024, exception_on_overflow = False)
        samples=numpy.frombuffer(raws, dtype=numpy.int16)
        result = str(samples)
        f.write(result)
        rms = audioop.rms(samples, 2)
        # Move marble          
        # px = notex
        # py = notey
        notex,notey = move_marble(rms, notex, notey)
        #put note in queue
        notexq.put(notex)
        noteyq.put(notey)
        #print graphics
        sense.clear()
        # maze[py][px] = W
        maze[notey][notex] = W
        # maze[foodPosY][foodPosX] = R
        sense.set_pixels(sum(maze,[]))
        sleep(delay)
        # maze[py][px] = P
        maze[notey][notex] = P

if __name__ == '__main__': 
    #initial position
    notex = 1
    notey = 1
    
    #initial Food
    foodx = 7
    foody = random.randint(3, 7)

    #initial wall
    floorx = [7]

    maze = [[G, G, G, G, G, G, G, G],
            [P, P, P, P, P, P, P, P],
            [P, P, P, P, P, P, P, P],
            [P, P, P, P, P, P, P, P],
            [P, P, P, P, P, P, P, P],
            [P, P, P, P, P, P, P, P],
            [P, P, P, P, P, P, P, P],
            [P, P, P, P, P, P, P, P]]

    pa = pyaudio.PyAudio()
    for i in range(pa.get_device_count()):
        dev = pa.get_device_info_by_index(i)
        print((i,dev['name'],dev['maxInputChannels'],dev['defaultSampleRate']))
        print(dev)
    stream = pa.open(format = pyaudio.paInt16,channels=1,rate=44100,input_device_index=3,input=True)
    numpy.set_printoptions(threshold=numpy.inf)
    f = open("demofile2.txt", "a")
    # count = 0
    # while True and count < 1000:

    notexq = Queue()
    noteyq = Queue()
    thread1 = threading.Thread(target=marble, args=(notex, notey, notexq, noteyq, ))
    thread2 = threading.Thread(target=moveFood, args=(foodx, foody, notexq, noteyq, ))
    thread3 = threading.Thread(target=floor0, args=(floorx, ))
    thread1.start()
    thread2.start()
    thread3.start()


