from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

gamePaused = False
global goLeft, goRight
printed = False
gameOver = False
fall_speed = 100  # speed of falling which remains constant
add_speed = 1  # adds speed after scoring
height_decrease = 0
new_diamond = True
diamond_active = False
c1 = 1.0
c2 = 1.0
c3 = 1.0
goLeft = 0
goRight = 0
x_start = 0
y_min_diamond = 7000
catcher_min_x_up, catcher_max_x_up = 1000, 3000  # catcher upper body
catcher_min_x_down, catcher_max_x_down = 1500, 2500  # catcher lower body
score = 0


def draw_points(x, y):
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def draw_using_mpl(x0, y0, x1, y1):
    zone = findZone(x0, y0, x1, y1)
    x0, y0 = convert_to_zone_0(zone, x0, y0)
    x1, y1 = convert_to_zone_0(zone, x1, y1)
    dx = x1 - x0
    dy = y1 - y0
    d = 2 * dy - dx
    dne = 2 * dy - 2 * dx
    de = 2 * dy
    for i in range(x0, x1):
        a, b = convert_back_to_original(zone, x0, y0)
        if d >= 0:
            d = d + dne
            draw_points(a, b)
            x0 += 1
            y0 += 1
        else:
            d = d + de
            draw_points(a, b)
            x0 += 1


def findZone(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    if abs(dx) > abs(dy):  # For Zone 0, 3, 4 & 7
        if dx > 0 and dy > 0:
            return 0
        elif dx < 0 and dy > 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        else:
            return 7
    else:  # For zone 1, 2, 5 & 6
        if dx > 0 and dy > 0:
            return 1
        elif dx < 0 and dy > 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        else:
            return 6


def convert_to_zone_0(zone, x0, y0):
    if zone == 0:
        return x0, y0
    elif zone == 1:
        return y0, x0
    elif zone == 2:
        return y0, -x0
    elif zone == 3:
        return -x0, y0
    elif zone == 4:
        return -x0, -y0
    elif zone == 5:
        return -y0, -x0
    elif zone == 6:
        return -y0, x0
    elif zone == 7:
        return x0, -y0


def convert_back_to_original(zone, x0, y0):
    if zone == 0:
        return x0, y0
    if zone == 1:
        return y0, x0
    if zone == 2:
        return -y0, x0
    if zone == 3:
        return -x0, y0
    if zone == 4:
        return -x0, -y0
    if zone == 5:
        return -y0, -x0
    if zone == 6:
        return y0, -x0
    if zone == 7:
        return x0, -y0


def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 10000, 0.0, 10000, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def draw_arrow():
    glColor3f(0.0, 1.0, 1.0)
    draw_using_mpl(1000, 9000, 2000, 9000)
    draw_using_mpl(1000, 9000, 1500, 9500)
    draw_using_mpl(1000, 9000, 1500, 8500)


def draw_cross():
    glColor3f(1.0, 0.0, 0.0)
    draw_using_mpl(8000, 9500, 9000, 8500)
    draw_using_mpl(8000, 8500, 9000, 9500)


def draw_pause_button():
    glColor3f(1.0, 1.0, 0.0)
    draw_using_mpl(4750, 9500, 4750, 8500)
    draw_using_mpl(5250, 9500, 5250, 8500)


def draw_play_button():
    glColor3f(1.0, 1.0, 0.0)
    draw_using_mpl(4750, 9500, 5250, 9000)
    draw_using_mpl(4750, 9500, 4750, 8500)
    draw_using_mpl(4750, 8500, 5250, 9000)


def draw_diamond():
    global height_decrease, new_diamond, c1, c2, c3, x_start, y_min_diamond, gameOver, score, catcher_max_x_up, catcher_min_x_up, add_speed, gamePaused, diamond_active

    if not gamePaused:
        if not diamond_active:
            # Initializing new diamond
            x_start = random.randint(250, 9750)  # screen width is 10000
            c1 = random.random()
            c2 = random.random()
            c3 = random.random()
            height_decrease = 0
            diamond_active = True

        if diamond_active:
            if y_min_diamond - height_decrease <= 600:
                if x_start >= catcher_min_x_up - goLeft + goRight and x_start <= catcher_max_x_up - goLeft + goRight:
                    score += 1
                    add_speed += 50
                    print("Score:", score)
                    diamond_active = False
                else:
                    gameOver = True
                    diamond_active = False

    if gameOver and not printed:
        print("Game Over")
        print("Score", score)

    if diamond_active:
        if not gameOver:
            glColor3f(c1, c2, c3)
        else:
            glColor3f(0.0, 0.0, 0.0)
        draw_using_mpl(x_start, 8000 - height_decrease, x_start + 250, 7500 - height_decrease)
        draw_using_mpl(x_start, 8000 - height_decrease, x_start - 250, 7500 - height_decrease)
        draw_using_mpl(x_start + 250, 7500 - height_decrease, x_start,
                       y_min_diamond - height_decrease)  # y_min dimond er bottomer y coordinate
        draw_using_mpl(x_start - 250, 7500 - height_decrease, x_start, y_min_diamond - height_decrease)

        if not gamePaused:
            height_decrease += fall_speed + add_speed


def draw_catcher():
    global gameOver, catcher_min_x_up, catcher_max_x_up, catcher_max_x_down, catcher_min_x_down
    if gameOver:
        glColor3f(1.0, 0.0, 0.0)
    else:
        glColor3f(1.0, 1.0, 1.0)
    draw_using_mpl(catcher_min_x_down - goLeft + goRight, 50, catcher_max_x_down - goLeft + goRight, 50)
    draw_using_mpl(catcher_min_x_up - goLeft + goRight, 600, catcher_max_x_up - goLeft + goRight, 600)
    draw_using_mpl(catcher_min_x_up - goLeft + goRight, 600, catcher_min_x_down - goLeft + goRight, 50)
    draw_using_mpl(catcher_max_x_down - goLeft + goRight, 50, catcher_max_x_up - goLeft + goRight, 600)


def display():
    global gamePaused
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    # glColor3f(1.0, 1.0, 0.0)  # konokichur color set (RGB)
    # call the draw methods here
    draw_arrow()
    draw_cross()
    if gamePaused:
        draw_play_button()
    else:
        draw_pause_button()
    draw_diamond()
    draw_catcher()
    glutSwapBuffers()


def animate():
    global gameOver, gamePaused
    if not gameOver:
        glutPostRedisplay()
        if not gamePaused:
            pass


def specialKeyListener(key, left, right):
    global goLeft, goRight, catcher_min_x_up, catcher_max_x_up, gameOver
    glutPostRedisplay()
    movement_speed = 500
    if not gamePaused and not gameOver:
        if key == GLUT_KEY_LEFT:
            if catcher_min_x_up - goLeft - movement_speed + goRight >= 0:
                goLeft += movement_speed
        if key == GLUT_KEY_RIGHT:
            if catcher_max_x_up - goLeft + movement_speed + goRight <= 10000:
                goRight += movement_speed


def restartGame():
    global score, gameOver, height_decrease, add_speed, diamond_active
    print(""""███████ ████████  █████  ██████  ████████ ██ ███    ██  ██████       ██████  ██    ██ ███████ ██████  
██         ██    ██   ██ ██   ██    ██    ██ ████   ██ ██           ██    ██ ██    ██ ██      ██   ██ 
███████    ██    ███████ ██████     ██    ██ ██ ██  ██ ██   ███     ██    ██ ██    ██ █████   ██████  
     ██    ██    ██   ██ ██   ██    ██    ██ ██  ██ ██ ██    ██     ██    ██  ██  ██  ██      ██   ██ 
███████    ██    ██   ██ ██   ██    ██    ██ ██   ████  ██████       ██████    ████   ███████ ██   ██ 
                                                                                                      
                                                                                                      """)
    score = 0
    gameOver = False
    diamond_active = False
    height_decrease = 0
    add_speed = 1


def mouseInput(button, state, x,
               y):  # mouse input er co-ordinate alada top left theke (0,0) start hbe and it will use the(500,500)
    global gamePaused, gameOver, printed, score
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if x >= 45 and x <= 100 and y >= 25 and y <= 75:
            restartGame()
        if x >= 225 and x <= 275 and y >= 25 and y <= 75:
            if not gamePaused:
                gamePaused = True
            else:
                gamePaused = False
        if x >= 390 and x <= 460 and y >= 25 and y <= 75:
            printed = True
            print("Goodbye")
            print("Score:", score)
            gameOver = True
            glutLeaveMainLoop()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)  # window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice")  # window name
glutDisplayFunc(display)
glutIdleFunc(animate)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseInput)
glutMainLoop()
