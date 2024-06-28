from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

position = 0
x1, y1, m1, m2 = 0, 0, 0.0, 0.0
color1 = 0
color2 = 0


def draw_points(x, y):
    glPointSize(5)  # pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x, y)  # jekhane show korbe pixel
    glEnd()


def draw_lines(a, b, c, d, w):
    glLineWidth(w)
    glBegin(GL_LINES)
    glVertex2f(a, b)
    glVertex2f(c, d)
    glEnd()


def draw_triangles(a, b, c, d, e, f):
    glBegin(GL_TRIANGLES)
    glVertex2f(a, b)
    glVertex2f(c, d)
    glVertex2f(e, f)
    glEnd()


def find_y_value(m, x1, y1, x):
    return m * x - m * x1 + y1 #dhal er sutro m= (y-y1)/(x-x1)


def draw_rain(m1, m2, x1, y1):
    global position
    x = 50
    y = 450
    y_new = 450
    while x < 450:
        x_new = x
        if x < 95 or x > 405: #jokhon roof er baire pore
            while y > 200:
                y_new -= random.randint(30, 70)
                draw_lines(x, y, x - position, y_new, 1)
                y = y_new - 5
                x = x - position
        elif x >= 95 and x < 251: #jokhon roof er upore(leeft side)
            val_y = find_y_value(m1, x1, y1, x) #straight line er jonno
            while y > val_y:
                val_y = find_y_value(m1, x1, y1, x) #recalculating cause diagonnaly o porbe aand for each x, y ber kora lagbe
                y_new -= random.randint(30, 70)
                if y_new < val_y: #jodi new y er value roof er niche pore taile roof hit kora porjonto
                    draw_lines(x, y, x - position, val_y, 1)
                else: #ar naile jemne ase emnei thakbe
                    draw_lines(x, y, x - position, y_new, 1)
                y = y_new - 5
                x = x - position
        elif x > 251 and x <= 405: #jokhon roof er upore(right side)
            val_y = find_y_value(m2, x1, y1, x)
            while y > val_y:
                val_y = find_y_value(m2, x1, y1, x)
                y_new -= random.randint(30, 70)
                if y_new < val_y:
                    draw_lines(x, y, x - position, val_y, 1)
                else:
                    draw_lines(x, y, x - position, y_new, 1)
                y = y_new - 5
                x = x - position
        if position < 0:
            x = x_new + 25 - position
        else:
            x = x_new + 25 + position
        y = 450
        y_new = 450


def animate():
    glutPostRedisplay()
    global x1, y1, m1, m2
    draw_rain(m1, m2, x1, y1)
    time.sleep(0.2)


def specialKeyListener(key, x, y):
    global position
    if key == GLUT_KEY_RIGHT:
        position -= 2
    if key == GLUT_KEY_LEFT:
        position += 2
    glutPostRedisplay()


def keyboardListener(key, x, y):
    global color1, color2
    if color1 == 0:
        if color2 != 0:
            if key == b'b':
                color2 -= 0.25
        if key == b'f':
            color2 += 0.25
            color1 += 0.25
    elif color1 == 1:
        if color2 != 1:
            if key == b'f':
                color2 += 0.25
        if key == b'b':
            color2 -= 0.25
            color1 -= 0.25
    elif color1 > 0 and color1 < 1:
        if key == b'f':
            color2 += 0.25
            if color1 == 0.25:
                color1 += 0.50
            else:
                color1 += 0.25
        if key == b'b':
            color2 -= 0.25
            if color1 == 0.75:
                color1 -= 0.50
            else:
                color1 -= 0.25
    glutPostRedisplay()


def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    global color1, color2
    global x1, y1, m1, m2
    glClearColor(1 - color2, 1 - color2, 1 - color2, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    # glColor3f(0.0, 0.0, 0.0) #konokichur color set (RGB)
    # call the draw methods here
    glColor3f(0 + color1, 0 + color1, 0 + color1)  # color of the lines of the house
    # main layout of the house
    draw_lines(103, 100, 398, 100, 10)
    draw_lines(108, 100, 108, 250, 10)
    draw_lines(393, 100, 393, 250, 10)
    draw_lines(103, 250, 398, 250, 10)
    # left roof line
    draw_lines(95, 247, 251, 350, 10)
    # finding gradient for the above line
    m1 = (350 - 247) / (251 - 95)
    x1 = 251
    y1 = 350
    # right roof line
    draw_lines(405, 247, 251, 350, 10)
    # finding gradient for the above line
    m2 = (247-350) / (405-251)
    # roof
    # door
    draw_lines(150, 100, 150, 200, 4)
    draw_lines(200, 100, 200, 200, 4)
    draw_lines(150, 197, 200, 197, 4)
    draw_points(185, 145)
    # window
    draw_lines(300, 180, 300, 220, 4)
    draw_lines(300, 217, 340, 217, 4)
    draw_lines(340, 220, 340, 180, 4)
    draw_lines(300, 182, 340, 182, 4)
    draw_lines(300, 200, 340, 200, 2)
    draw_lines(320, 220, 320, 180, 2)
    # using a loop to draw rain particles
    draw_rain(m1, m2, x1, y1)
    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)  # window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice")  # window name
glutDisplayFunc(showScreen)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMainLoop()
