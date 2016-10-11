


import pygame
import time
from classes import Actor
from classes import Rectangle

# Initialize the game engine
pygame.init()

# Define some colors

 
PI = 3.141592653
# Set the height and width of the screen

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
    
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    bg_color = WHITE
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    done = False
    x_m = 20
    y_m = 0
    rect_h_p = 80
    rect_w_p = 80
    vy_mps = 30
    vx_mps = 39.43

    #adam = Rectangle(10,0,10,10,10,0,(0,0,20), 0, 0)
    #mark = Rectangle(0,14,30,30,0,-20,(200,200,200), 0, 14)
    arthur = Rectangle(14,14,90,90,-40,10,(200,29,100), 14, 14)
    jake = Rectangle(50,50,90,90,20,0,(150,150,20), 50, 50)
    actors = [arthur, jake]
    uldr_boundaries = [y_upper_edge_m,x_left_edge_m,y_lower_edge_m,x_right_edge_m]
    
    dt_s   =  0.048
    time_10 = 0
    time_510 = 0
    time_steps = 0
    ay_mps2 = 20.0 
    while not done:
        time_steps += 1
        if time_steps == 10:
            time_10 = time.clock()
        if time_steps == 510:
            print(time.clock() - time_10)
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
     
     
        clear_screen(bg_color)
        
        for a in actors:
            update_pos(a,ay_mps2,dt_s)
        
        detect_collisions(actors, uldr_boundaries)   
        # Update the velocity and position.
        vy_mps +=  ay_mps2 * dt_s
        y_m   +=  vy_mps  * dt_s

        x_m   +=  vx_mps  * dt_s
        #print(y_m)
        # Check for wall collisions.
        if (y_m + p_to_m(rect_h_p) > y_lower_edge_m): 
            vy_mps *= -1 * 0.80  # loss of 20% on each bounce.
            vx_mps *= 0.90
            y_m = fix_sticky( y_m, rect_h_p, y_upper_edge_m, y_lower_edge_m)
            
        if x_m + p_to_m(rect_w_p) > x_right_edge_m or x_m < x_left_edge_m:
            vx_mps *= -1 * 0.80
            x_m = fix_sticky(x_m,rect_w_p, x_left_edge_m,x_right_edge_m)
  
        for a in actors:
            draw_object(a)
        #pygame.draw.rect(screen, BLACK, [m_to_px(x_m), m_to_px(y_m), rect_w_p, rect_h_p], 0)
        
        pygame.display.flip()
     
        time.sleep(dt_s/2)
    # Be IDLE friendly
    pygame.quit()

def update_pos(actor, ay, dt_s):
    actor.yv +=  ay * dt_s
    actor.y_prev = actor.y_pos
    actor. x_prev = actor.x_pos
    actor.y_pos   +=  actor.yv  * dt_s
    actor.x_pos   +=  actor.xv  * dt_s
    # Check for wall collisions.
    '''if (actor.y_pos + p_to_m(actor.h) > y_lower_edge_m): 
        vy_mps *= -1 * 0.80  # loss of 20 percent on each bounce.
        vx_mps *= 0.90
        y_m = fix_sticky( y_m, y_upper_edge_m, y_lower_edge_m)
        
    if x_m + p_to_m(rect_w_p) > x_right_edge_m or x_m < x_left_edge_m:
        vx_mps *= -1 * 0.80
        x_m = fix_sticky(x_m,x_left_edge_m,x_right_edge_m)'''
def detect_collisions(actors, uldr_boundaries):
    for i in range(len(actors)):
        #print('i: ' + str(i))
        curr_actor = actors[i]
        y_extreme = curr_actor.y_pos + p_to_m(curr_actor.h)
        x_extreme = curr_actor.x_pos + p_to_m(curr_actor.w)
        if (y_extreme > uldr_boundaries[2]): 
            curr_actor.yv *= -1 * 0.80  # loss of 20% on each bounce.
            curr_actor.xv *= 0.90
            curr_actor.y_pos = fix_sticky(curr_actor.y_pos,curr_actor.h,uldr_boundaries[0], uldr_boundaries[2])
        if (curr_actor.x_pos < uldr_boundaries[1] or x_extreme > uldr_boundaries[3]):
            curr_actor.xv *= -1 * 0.8
            curr_actor.x_pos = fix_sticky(curr_actor.x_pos,curr_actor.w,uldr_boundaries[1],uldr_boundaries[3])
        for j in range(i+1,len(actors)):
            #print('j: ' + str(j))
            other_actor = actors[j]
            other_y_extreme = other_actor.y_pos + p_to_m(other_actor.h)
            other_x_extreme = other_actor.x_pos + p_to_m(other_actor.w)
            y_collision_down = y_extreme > other_actor.y_pos and curr_actor.y_pos < other_actor.y_pos


            y_collision_up = curr_actor.y_pos < other_y_extreme and curr_actor.y_pos > other_actor.y_pos
            #print(curr_actor.y_pos)
            #print(other_y_extreme)
            x_collision_left = curr_actor.x_pos < other_x_extreme and curr_actor.x_pos > other_actor.x_pos
            x_collision_right = x_extreme > other_actor.x_pos and curr_actor.x_pos < other_actor.x_pos

            x_extreme_prev = curr_actor.x_prev + p_to_m(curr_actor.w)
            other_x_extreme_prev = other_actor.x_prev + p_to_m(other_actor.w)
            y_extreme_prev = curr_actor.y_prev + p_to_m(curr_actor.h)
            other_y_extreme_prev = other_actor.y_prev + p_to_m(other_actor.h)
            
            x_overlap = (curr_actor.x_prev >= other_actor.x_prev and curr_actor.x_prev <= other_x_extreme_prev) or (x_extreme_prev >= other_actor.x_prev and x_extreme_prev <= other_x_extreme_prev) or (curr_actor.x_prev < other_actor.x_prev and x_extreme_prev > other_x_extreme_prev)
            y_overlap = (curr_actor.y_prev >= other_actor.y_prev and curr_actor.y_prev <= other_y_extreme_prev) or (y_extreme_prev >= other_actor.y_prev and y_extreme_prev <= other_y_extreme_prev) or (curr_actor.y_prev < other_actor.y_prev and y_extreme_prev > other_y_extreme_prev)
            
            
            if (x_overlap and (y_collision_up or y_collision_down)):
                print("Y-collide")
                print("first: " + str((curr_actor.x_prev >= other_actor.x_prev and curr_actor.x_prev <= other_x_extreme_prev)))
                print("second: " + str((x_extreme_prev >= other_actor.x_prev and x_extreme_prev <= other_x_extreme_prev)))
                print("third: " + str((curr_actor.x_prev < other_actor.x_prev and x_extreme_prev > other_x_extreme_prev)))
                
                print("Up: " + str(y_collision_up))
                print("Down: " + str(y_collision_down))
                print("first: " + str((curr_actor.x_prev >= other_actor.x_prev and curr_actor.x_prev <= other_x_extreme_prev)))
                print("second: " + str((x_extreme_prev >= other_actor.x_prev and x_extreme_prev <= other_x_extreme_prev)))
                print("third: " + str((curr_actor.x_prev < other_actor.x_prev and x_extreme_prev > other_x_extreme_prev)))
                curr_actor.yv *= -1 * 0.80
                other_actor.yv *= -1 *0.80
                if (y_collision_up):
                    y_mean = (curr_actor.y_pos + other_y_extreme)/2
                    curr_actor.y_pos = y_mean 
                    other_actor.y_pos = y_mean - p_to_m(other_actor.h)
                if (y_collision_down):
                    y_mean = (y_extreme + other_actor.y_pos)/2
                    other_actor.y_pos = y_mean 
                    curr_actor.y_pos = y_mean - p_to_m(curr_actor.h)
            
            if (y_overlap and (x_collision_right or x_collision_left)):
                print("X-collide")
                if (x_collision_left):
                    print("LEFT")
                elif (x_collision_right):
                    print("RIGHT")
                curr_actor.xv *= -1 * 0.80
                other_actor.xv *= -1 *0.80
                if (x_collision_left):
                    x_mean = (curr_actor.x_pos + other_x_extreme)/2
                    curr_actor.x_pos = x_mean 
                    other_actor.x_pos = x_mean - p_to_m(other_actor.w)
                if (x_collision_right):
                    x_mean = (x_extreme + other_actor.x_pos)/2
                    other_actor.x_pos = x_mean 
                    curr_actor.x_pos = x_mean - p_to_m(curr_actor.w)
                


     

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