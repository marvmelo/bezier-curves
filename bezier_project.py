from pickle import FALSE
import re
import sys, pygame

from classes import Bezier


def main():
    
    pygame.init()
    size = width, height = 1200, 600 
    screen = pygame.display.set_mode(size)
    bezier = Bezier()
    curves = []
    curves.append(bezier)
    active_curve = 0
    show_curve = True
    show_points = True
    show_lines = True
    mode = 'a'
    resolution = [5,10,50,100]
    r = 0

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT: sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                curves[active_curve].receive_input(mouse_pos[0], mouse_pos[1], mode)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    show_curve = not show_curve
                elif event.key == pygame.K_i:
                    show_points = not show_points
                elif event.key == pygame.K_o:
                    show_lines = not show_lines
                elif event.key == pygame.K_a:
                    mode = 'a'
                elif event.key == pygame.K_d:
                    mode = 'd'
                elif event.key == pygame.K_m:
                    mode = 'm'
                elif event.key == pygame.K_p:
                    if not curves[active_curve].points:
                        curves.pop(active_curve)
                    active_curve = (active_curve+1) % len(curves)
                elif event.key == pygame.K_n:
                    if not curves[active_curve].points:
                        curves.pop(active_curve)
                    new_bezier = Bezier()
                    curves.append(new_bezier)
                    active_curve = len(curves) -1
                    mode = 'a'  
                elif event.key == pygame.K_e:
                    if len(curves) >1: curves.pop(active_curve)
                    active_curve %= len(curves)
                elif event.key == pygame.K_r:
                    r = (r+1)%4
                elif event.key == pygame.K_c:
                    curves[active_curve].points.append(curves[active_curve].points[0])

        screen.fill((0,0,0))
        for i, c in enumerate(curves):
            if i==active_curve:
                c.draw_curve(resolution[r], screen, show_curve, show_points, show_lines, active=True)
            else:
                c.draw_curve(resolution[r], screen, show_curve, show_points, show_lines, active=False)

        pygame.display.flip()

if __name__=='__main__':
    main()