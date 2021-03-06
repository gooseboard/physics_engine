


import pygame
import time
from classes import Actor
from classes import Rectangle
from math import atan2, degrees, pi
from random import randint, seed
# Initialize the game engine
pygame.init()
seed()
screen = None

# Loop until the user clicks the close button.

# Loop as long as done == False
def main():
    global screen
    x_right_edge_p = 800
    x_left_edge_p = 0
    y_lower_edge_p = 450
    y_upper_edge_p = 0
    y_lower_edge_m = p_to_m(y_lower_edge_p)
    x_right_edge_m = p_to_m(x_right_edge_p)
    y_upper_edge_m = 0
    x_left_edge_m = 0

    size = (x_right_edge_p, y_lower_edge_p)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Phys")
    clock = pygame.time.Clock()
    

    bg_color = (200,240,250)
    
    done = False

    '''adam = Rectangle(10,0,70,40,10,0,(0,0,20),0)
    ash = Rectangle(15,5,70,40,10,0,(230,100,20),0)
    eve = Rectangle(10,30,30,10,10,-50,(90,90,230),0)
    mark = Rectangle(0,14,20,30,-4,-20,(200,200,200),0)
    arthur = Rectangle(14,14,90,90,-40,10,(200,29,100),0)
    jake = Rectangle(50,50,90,90,20,0,(150,150,20),0)

    actors = [arthur, jake,mark, adam, ash, eve]'''
    actors = random_box_generator(20)

    for a in actors:# give mass
        a.mass = float(a.w*a.h)*0.1



    
 
    
    uldr_boundaries = [y_upper_edge_m,x_left_edge_m,y_lower_edge_m,x_right_edge_m]
    
    dt_s   =  0.038
  
    ay_mps2 = 20.0 
    while not done:
        
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
     
     
        clear_screen(bg_color)
        
        for a in actors:
            update_pos(a,ay_mps2,dt_s)
        
        detect_collisions(actors, uldr_boundaries)   
        # Update the velocity and position.
        
  
        for a in actors:
            draw_object(a)
        
        
        pygame.display.flip()
     
        #time.sleep(dt_s/2)
    # Be IDLE friendly
    pygame.quit()
def random_box_generator(n):
    li = []
    for i in range(n):
        a = Rectangle(randint(0,50),randint(0,70),randint(1,90),randint(1,90),randint(-20,20),randint(-20,20),(randint(0,255),randint(0,255),randint(0,255)),0)
        li.append(a)
    return li


    ash = Rectangle(15,5,70,40,10,0,(230,100,20),0)
def update_pos(actor, ay, dt_s):
    actor.yv +=  ay * dt_s
    
    actor.y_pos   +=  actor.yv  * dt_s
    actor.x_pos   +=  actor.xv  * dt_s

def detect_collisions(actors, uldr_boundaries):
    for i in range(len(actors)):
        curr_actor = actors[i]
        y_extreme = curr_actor.y_pos + p_to_m(curr_actor.h)
        x_extreme = curr_actor.x_pos + p_to_m(curr_actor.w)
        if (y_extreme > uldr_boundaries[2]): 
            curr_actor.yv *= -1 * 0.90  # loss of 20% on each bounce.
            curr_actor.xv *= 0.90
            curr_actor.y_pos = fix_sticky(curr_actor.y_pos,curr_actor.h,uldr_boundaries[0], uldr_boundaries[2])
        if (curr_actor.x_pos < uldr_boundaries[1] or x_extreme > uldr_boundaries[3]):
            curr_actor.xv *= -1 * 0.9
            curr_actor.x_pos = fix_sticky(curr_actor.x_pos,curr_actor.w,uldr_boundaries[1],uldr_boundaries[3])
        for j in range(i+1,len(actors)):
            other_actor = actors[j]
            other_y_extreme = other_actor.y_pos + p_to_m(other_actor.h)
            other_x_extreme = other_actor.x_pos + p_to_m(other_actor.w)
            x_overlap = (curr_actor.x_pos >= other_actor.x_pos and curr_actor.x_pos <= other_x_extreme) or (x_extreme >= other_actor.x_pos and x_extreme <= other_x_extreme) or (curr_actor.x_pos < other_actor.x_pos and x_extreme > other_x_extreme)
            y_overlap = (curr_actor.y_pos >= other_actor.y_pos and curr_actor.y_pos <= other_y_extreme) or (y_extreme >= other_actor.y_pos and y_extreme <= other_y_extreme) or (curr_actor.y_pos < other_actor.y_pos and y_extreme > other_y_extreme)
            if x_overlap and y_overlap:
                dx = (curr_actor.x_pos + p_to_m(curr_actor.w)/2) - (other_actor.x_pos + p_to_m(other_actor.w)/2)
                dy = (curr_actor.y_pos + p_to_m(curr_actor.h)/2) - (other_actor.y_pos + p_to_m(other_actor.h)/2)
                angle = 180*atan2(-dy,dx)/pi
                m1 = curr_actor.mass
                m2 = other_actor.mass
                
                term1 = (m1-m2)/(m1+m2)
                if abs(angle) >= 45 and abs(angle) <= 135:
                    #print("Y-collide")
                    if angle > 0: #down collision
                        y_mean = (y_extreme + other_actor.y_pos)/2
                        other_actor.y_pos = y_mean 
                        curr_actor.y_pos = y_mean - p_to_m(curr_actor.h)
                    else: 
                        y_mean = (curr_actor.y_pos + other_y_extreme)/2
                        curr_actor.y_pos = y_mean 
                        other_actor.y_pos = y_mean - p_to_m(other_actor.h)
                    v1 = curr_actor.yv
                    curr_actor.yv = 0.95*((term1*v1) + (2*m2/(m1+m2))*other_actor.yv)
                    other_actor.yv = 0.95*(((2*m1/(m1+m2))*v1) - term1*other_actor.yv)
                else: #x_collision
                    '''print("X-collide")
                    print("i,j: " + str(i) + "," +str(j))
                    print("my vel: " + str(curr_actor.xv))
                    print("my mass: " + str(curr_actor.mass))
                    print("his vel: " + str(other_actor.xv))
                    print("his mass: " + str(other_actor.mass))'''
                    if abs(angle) > 45:
                        x_mean = (x_extreme + other_actor.x_pos)/2
                        other_actor.x_pos = x_mean 
                        curr_actor.x_pos = x_mean - p_to_m(curr_actor.w)
                    else: 
                        x_mean = (curr_actor.x_pos + other_x_extreme)/2
                        curr_actor.x_pos = x_mean 
                        other_actor.x_pos = x_mean - p_to_m(other_actor.w)
                    v1 = curr_actor.xv
                    curr_actor.xv = 0.95*(term1*v1 + (2*m2/(m1+m2))*other_actor.xv)
                    other_actor.xv = 0.95*(((2*m1/(m1+m2))*v1) - term1*other_actor.xv)
                    #print("my vel after: " + str(curr_actor.xv))
                    #print("his vel after: " + str(other_actor.xv))
            
def draw_object(actor):
    global screen
    if isinstance(actor, Rectangle):
        pygame.draw.rect(screen, actor.color, [m_to_px(actor.x_pos), m_to_px(actor.y_pos), actor.w, actor.h], 0)
def clear_screen(color):
    screen.fill(color)

def m_to_px(x_m):
    return int(round( x_m * 7.0))   # pixels per meter.
def p_to_m(x_p):
    return x_p/7.0   # pixels per meter.
    
def fix_sticky( x_m, width_p, x_left_edge_m, x_right_edge_m):
    # Simple stickiness correction. Move it back to the surface.
    if (x_m < x_left_edge_m): 
        x_corrected_m = x_left_edge_m  
    elif (x_m + p_to_m(width_p) > x_right_edge_m): 
        x_corrected_m = x_right_edge_m - p_to_m(width_p)  
    return x_corrected_m
  

main()