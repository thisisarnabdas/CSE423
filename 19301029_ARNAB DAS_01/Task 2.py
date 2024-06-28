import random
import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

points_info = []
frozen = False
speed_timer = 0.02
blink = False


class Point:
    def __init__(self, x, y):
        self.point_x = x
        self.point_y = 500 - y # converts traditional point to opengl
        self.c1 = random.randint(0, 1)
        self.c2 = random.randint(0, 1)
        self.c3 = random.randint(0, 1)
        r = random.randint(1, 4)
        if r == 1:
            self.change_x = 1
            self.change_y = 1
        elif r == 2:
            self.change_x = 1
            self.change_y = -1
        elif r == 3:
            self.change_x = -1
            self.change_y = 1
        elif r == 4:
            self.change_x = -1
            self.change_y = -1
        self.temp_c1 = 0
        self.temp_c2 = 0
        self.temp_c3 = 0


def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def animate():
    global speed_timer, frozen, points_info, blink
    if not frozen: # jokhon pause thakbena
        for i in points_info:
            movement_decision(i)
            i.point_x += i.change_x
            i.point_y += i.change_y
    else:
        for i in points_info:
            i.point_x = i.point_x
            i.point_y = i.point_y
    if blink:
        time.sleep(1)
        blink = False
    else:
        time.sleep(speed_timer)
    glutPostRedisplay()


def display():
    global points_info
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    draw_points(points_info)
    # call the draw methods here
    # main layout of the house
    glutSwapBuffers()


def mouseInput(button, state, x, y):
    global points_info, blink
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        obj = generate_new_point(x, y)
        points_info.append(obj)
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        blink = True
    glutPostRedisplay()


def generate_new_point(x, y):
    new_point = Point(x, y) #p point class er new object toiri hoy
    return new_point


def draw_points(lst):
    global blink
    for i in lst:
        glPointSize(5)  # pixel size. by default 1 thake
        glBegin(GL_POINTS)
        if blink:
            glColor3f(0, 0, 0)
        else:
            glColor3f(i.c1, i.c2, i.c3)
        glVertex2f(i.point_x, i.point_y)  # jekhane show korbe pixel
        glEnd()


def movement_decision(obj): #bari khawar por co-ordinate ulta hoye jaabe
    if obj.point_x == 0 or obj.point_x == 500:
        obj.change_x = -1 * obj.change_x
    if obj.point_y == 0 or obj.point_y == 500:
        obj.change_y = -1 * obj.change_y


def specialKeyListener(key, x, y):
    global speed_timer
    if key == GLUT_KEY_UP:
        speed_timer /= 2
    if key == GLUT_KEY_DOWN:
        speed_timer *= 2
    glutPostRedisplay()


def keyboardListener(key, x, y):
    global frozen
    if key == b' ':
        if frozen:
            frozen = False
        else:
            frozen = True
    glutPostRedisplay()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)  # window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice")  # window name
glutDisplayFunc(display)
glutIdleFunc(animate)
glutMouseFunc(mouseInput)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMainLoop()
