from pygame.draw import *
import pygame, sys

class Bezier:
    
    def __init__(self):
        
        self.points = []
        self.W = (255,255,255)
        self.G = (100,50,100)
        
    def add_point(self, pX, pY):
        
        self.points.append([pX, pY])
        
    def remove_point(self, idx):
        
        self.points.pop(idx)
        
    def __interpolate(self, p0, p1, t):
        
        return [p0[0] + t*(p1[0]-p0[0]), p0[1] + t*(p1[1]-p0[1])]
    
    def casteljau(self, t, points_list):
        
        if (len(points_list)==1):
            return points_list[0]
        else:
            new_points_list = []
            for idx in range(len(points_list)-1):
                new_points_list.append(self.__interpolate(points_list[idx], points_list[idx+1], t))
            return self.casteljau(t, new_points_list)
                
    def calculate_points(self, step):
        
        if (not self.points): return []
        points_list = []
        for i in range(step+1):
            t = i/step
            points_list.append(self.casteljau(t, self.points))
        return points_list
    
    def draw_curve(self, step, screen, show_curve=True, show_points=True, show_lines=True, active=True):
        
        points_to_draw = self.calculate_points(step)
        if show_points:
            for idx in range(len(self.points)):
                if active: circle(screen, self.W, [self.points[idx][0], self.points[idx][1]], 6)
                else: circle(screen, self.G, [self.points[idx][0], self.points[idx][1]], 6)
        if show_lines:
            for idx in range(len(self.points)-1):
                if active: line(screen, self.W, [self.points[idx][0], self.points[idx][1]], [self.points[idx+1][0], self.points[idx+1][1]])
                else: line(screen, self.G, [self.points[idx][0], self.points[idx][1]], [self.points[idx+1][0], self.points[idx+1][1]])
        if show_curve:
            for idx in range(len(points_to_draw)-1):
                if active: line(screen, self.W, (points_to_draw[idx][0],points_to_draw[idx][1]), (points_to_draw[idx+1][0],points_to_draw[idx+1][1]))
                else: line(screen, self.G, (points_to_draw[idx][0],points_to_draw[idx][1]), (points_to_draw[idx+1][0],points_to_draw[idx+1][1]))
        
    def __selected_point(self, pX, pY):

        for idx, p in enumerate(self.points):
            delta_x = p[0] - pX
            delta_y = p[1] - pY
            if delta_x**2 + delta_y**2 < 36:
                return idx
        return -1

    def receive_input(self, pX, pY, mode):

        if mode=='a':
            self.add_point(pX, pY)
        elif mode=='d':
            idx = self.__selected_point(pX, pY)
            if idx != -1:
                self.remove_point(idx)
        elif mode=='m':
            idx = self.__selected_point(pX, pY)
            if idx != -1:
                hasnt_chosen = True
                while hasnt_chosen:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT: sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            self.points[idx] = [mouse_pos[0], mouse_pos[1]]
                            hasnt_chosen = False