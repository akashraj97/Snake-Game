######################## Turtle Snake Game ########################

import turtle
from random import randint
from time import sleep

# Screen Size Setup and Other Settings
turtle.setup(width=500,height=500)

SCREEN = turtle.Screen()
SCREEN.bgcolor('yellow')
SCREEN.title('Snake')

score = -1

SIZE_W,SIZE_H = 500,500
sl = 110     #Sleep Timing to increase Snake Speed

dir_x,dir_y = 0,0

snake_coor=[]
food = 1
food_coor = (0,0)
stop = False

def getRandPos():
    while True:
        x,y =  (randint(-SIZE_W//2, SIZE_W//2), randint(-SIZE_H//2, SIZE_H//2))
        x-= (x%18)
        y-= (y%18)
        if ((-SIZE_W+9)//2<x<(SIZE_W-9)//2) and ((-SIZE_H+9)//2<y<(SIZE_H-9)//2) and x%18==0 and y%18==0:
            return (x,y)


def actualise_display():
    global SIZE_W,SIZE_H
    tracer = SCREEN.tracer()
    SIZE_W,SIZE_H = SCREEN.window_width(),SCREEN.window_height()
    #print("Screen Size ",SIZE_W,SIZE_H,snake_coor[0])
    SCREEN.tracer(0)
    
    food.clearstamps(1)
    snake.clearstamps(len(snake_coor))
    
    food.goto(food_coor[0], food_coor[1])
    food.stamp()

    for x, y in snake_coor:
        snake.goto(x, y)
        snake.stamp()
    
    SCREEN.tracer(tracer)
    
def safeDistance(x,yrr):
    return sum([ int(((x[0]-y[0])**2+(x[1]-y[1])**2)**.5>18) for y in yrr ])==0

def foodOutOfScreen():
	global food_coor,SIZE_H,SIZE_W
	return ((-SIZE_W+9)//2<food_coor[0]<(SIZE_W-9)//2) and ((-SIZE_H+9)//2<food_coor[1]<(SIZE_H-9)//2)

def actualise_pos():
    global snake_coor, food_coor, stop, sl

    avance()
    if not foodOutOfScreen():
        food_coor = getRandPos()
        while safeDistance(food_coor,snake_coor):
            print("Snake Coor ",snake_coor,"  Food Coor",food_coor)
            food_coor = getRandPos()
    isBorderCollision()
    if isSelfCollision():
        #print(snake_coor)
        stop = True
    if isFoodCollision():
        print("Collision Snake and Food Co-ordinates",snake_coor[0],food_coor)
        sl -= (0.02*sl)
        sl = int(sl)
        append()
        food_coor = getRandPos()
        while safeDistance(food_coor,snake_coor):
            print("Snake Coor ",snake_coor,"  Food Coor",food_coor)
            food_coor = getRandPos()

def loop():
    while True:
        if stop:
            return gameOver()
        actualise_pos()
        actualise_display()
        sleep(sl/1000.0)
    
def isSelfCollision():
    global snake_coor
    return len(set(snake_coor))<len(snake_coor)

def isFoodCollision():
    sx, sy = snake_coor[0]
    fx, fy = food_coor
    distance = ((sx-fx)**2 + (sy-fy)**2)**.5
    return distance<18

def isBorderCollision():
    global snake_coor
    x, y = snake_coor[0]
#    return not (-SIZE//2-50<x<SIZE//2+50) or not (-SIZE//2-50<y<SIZE//2+50)
    if not (-SIZE_W//2+9<x<SIZE_W//2-9):
        if (-SIZE_W//2+9>=x):
            x = SIZE_W//2-9
            x -= (x%18)
        elif (x>=SIZE_W//2-9):
            #print("One")
            x = -SIZE_W//2+9
            x += (abs(x)%18) if abs(x)%18!=0 else 0
        snake_coor[0] = (x,y)
    if not (-SIZE_H//2+9<y<SIZE_H//2-9):
        if not (-SIZE_H//2+9<=y):
            y = SIZE_H//2-9
            y -= (y%18)
        elif not (SIZE_H//2-9>=y):
            y = -SIZE_H//2+9
            y += abs(y)%18 if abs(y)%18!=0 else 0
        snake_coor[0] = (x,y)

def avance():
    global snake_coor
    x, y = snake_coor[0]
    x += dir_x*18
    y += dir_y*18
    snake_coor.insert(0, (x, y))
    snake_coor.pop(-1)

def append():
    global snake_coor
    a = snake_coor[-1][:]
    snake_coor.append(a)

def setDir(x, y):
    global dir_x, dir_y
    dir_x = x
    dir_y = y
    
def right():
    if (dir_x,dir_y)==(-1,0):
        return
    setDir(1, 0)
def left():
    if (dir_x,dir_y)==(1,0):
        return
    setDir(-1, 0)
def up():
    if (dir_x,dir_y)==(0,-1):
        return
    setDir(0, 1)
def down():
    if (dir_x,dir_y)==(0,1):
        return
    setDir(0, -1)
    
def gameOver():
    d = turtle.Turtle()
    d.up()
    d.ht()
    d.color("blue")
    d.write("GAME OVER\nScore : %04d" % (len(snake_coor)), align="center", font=("Arial", 30, "bold"))
    SCREEN.onclick(lambda *a:[SCREEN.bye(),exit()])
    return len(snake_coor)

def startSnakeGame():
    
    global SCREEN,food,snake,snake_coor,food_coor,stop,dir_x,dir_y,sl

    SCREEN = turtle.Screen()
    SCREEN.title("Snake")
    SCREEN.setup(SIZE_W, SIZE_H)
    SCREEN.bgcolor("yellow")

    food = turtle.Turtle()
    food.width(18)
    food.up()
    food.shape("circle")
    food.color("red")
    food.ht()

    food_coor = getRandPos()

    sl = 110
    
    snake = turtle.Turtle()
    snake.width(18)
    snake.up()
    snake.shape("circle")
    snake.color("green")
    snake.ht()

    snake_coor = [(0, 0)]

    dir_x = 1
    dir_y = 0

    stop = False

    SCREEN.onkeypress(up, "Up")
    SCREEN.onkeypress(down, "Down")
    SCREEN.onkeypress(right, "Right")
    SCREEN.onkeypress(left, "Left")
    SCREEN.listen()
    return loop()
    turtle.mainloop()

while True:
    
    prompt = "1. New Game\n2. Exit" if score==-1 else "Your score: "+str(score)+"\n\n1.New Game\n2.Exit"
    
    choice = SCREEN.numinput(title="Enter your choice",prompt=prompt,minval=1,maxval=2)

    if choice == 1:
        SCREEN.clearscreen()
        score = startSnakeGame()
    elif choice == 2:
        SCREEN.bye()
        exit(0)
    else:
        turtle.Turtle().write("Please Enter your choice", align="center", font=("Arial", 30, "bold"))
        sleep(2)
        SCREEN.clear()
        SCREEN.bgcolor('yellow')