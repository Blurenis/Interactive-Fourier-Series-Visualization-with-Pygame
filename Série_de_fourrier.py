import pygame
import sys
import numpy as np
import math

# Initialize Pygame
pygame.init()

# Define constants
VECTOR_ACTIVATION = False
NUMBER_ACTIVE_VECTOR = 1
NUMBER_OF_VECTOR_CALCULATED = 200

SINGLE_CLICK = False

POINT_PER_POINT_ACTIVATION = False
POINT_COLOR = (100, 100, 100)
POINT_SIZE = 3

PICTURE_SCALE = 1
PICTURE_DIRECTORY = r"C:\Users\..." # Don'to forget to set the right path if you want to show a picture
PICTURE_ACTIVATION = False

MAIN_GRID_COLOR = (55, 55, 55)
SECONDARY_GRID_COLOR = (20, 20, 20)

MAGNETUDE_SCALE = 1
ANGULAR_SPEED_SCALE = 1

CERCLE_ACTIVATION = True
CERCLE_THICKNESS = 1
CERCLE_COLOR = (25, 25, 25)

LINE_COLOR = (255, 255, 255)
LINE_THICKNESS = 3

TRIANGLE_RATIO = 7
TRIANGLE_ACTIVATION = True
TRIANGLE_COLOR = (255, 255, 255)

MARKER_2_COLOR = (0, 100, 250, 0.1)
MARKER_2_THICKNESS = 3
MARKER_2_MAX_DURATION = 10
MARKER_2_ACTIVATION = True


MARKER_COLOR = (0, 0, 200)
MARKER_THICKNESS = 1
MARKER_MAX_DURATION = 10
MARKER_ACTIVATION = False

TICK_SPEED = 60
WIDTH, HEIGHT = 1300, 800
BG_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)

# Standerdise the angular_speed_scale
ANGULAR_SPEED_SCALE *= 1/TICK_SPEED 
MARKER_MAX_DURATION *= TICK_SPEED


# Set up martker
marker_list = []
# Marker_2 initialisation list
marker_2_list = [0]

# set up drwing list
drawing_list = []
left_click = False

        
# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basic Pygame Interface")

# Load the font
font = pygame.font.Font(None, 26)

# Créer un objet Clock
clock = pygame.time.Clock()

# Charger une image
image = pygame.image.load(PICTURE_DIRECTORY)  # Remplacez par le chemin de votre image

# Scale the picture
image = pygame.transform.scale(image, (image.get_width() // PICTURE_SCALE, image.get_height() // PICTURE_SCALE))
image_rect = image.get_rect()


# Set up vectors
vectors_list = []
class Vector:
    def __init__(self, magnetude, angle, angular_speed):
        self.magnetude = magnetude
        self.angular_speed = angular_speed
        self.angle = angle




def add_element_drawing_list(drawing_list):
    """This function adds equidistant points between each pair of points in the drawing_list to double the total number of points approximately."""
    
    if not drawing_list:
        return drawing_list  # Return the empty list if the input list is empty

    new_drawing_list = []
    
    # Compute the total distance
    total_distance = 0
    for i in range(len(drawing_list) - 1):
        distance = np.sqrt((drawing_list[i][0] - drawing_list[i + 1][0])**2 + (drawing_list[i][1] - drawing_list[i + 1][1])**2)
        total_distance += distance
    
    # Compute the average distance and target new average distance
    average_length = total_distance / len(drawing_list)
    new_average_length = average_length / 2  # New desired spacing

    # Process each segment to add points at `new_average_length`
    for i in range(len(drawing_list) - 1):
        start_point = np.array(drawing_list[i])
        end_point = np.array(drawing_list[i + 1])
        
        # Calculate distance of the current segment
        segment_length = np.linalg.norm(end_point - start_point)
        
        # Number of new points to add between start_point and end_point
        num_new_points = int(segment_length // new_average_length)
        
        # Add the original start point
        new_drawing_list.append(tuple(start_point))
        
        # Interpolate points along the segment
        for j in range(1, num_new_points + 1):
            new_point = start_point + (end_point - start_point) * (j / (num_new_points + 1))
            new_drawing_list.append(tuple(new_point))
    
    # Add the last point from the original list
    new_drawing_list.append(drawing_list[-1])
    
    return new_drawing_list
        
def show_command():
    print("Increase the number of vector by 1: UP")
    print("Decrease the number of vector by 1: DOWN")
    print("Calculating the vectors: ENTER")
    print("Double the number of point: d")
    
def draw_marker_2(vectors_list_temp):

    global marker_2_list
    
    if NUMBER_ACTIVE_VECTOR == marker_2_list[0]:
        
        if MARKER_2_ACTIVATION:
            for i in range(len(marker_2_list[1:-1])):
                pygame.draw.line(screen, MARKER_2_COLOR, marker_2_list[1:][i] , marker_2_list[1:][i+1], MARKER_2_THICKNESS)
    else:
        # reset the list
        marker_2_list = [NUMBER_ACTIVE_VECTOR]
        
        
        
        
        
        for i in range(1, int(2*np.pi*TICK_SPEED + 3)):
            
            # Set the starting point at the middle
            starting_point = (WIDTH // 2, HEIGHT // 2)
            index_vector = 0
            
            for vector in vectors_list_temp: 
                
                if index_vector < NUMBER_ACTIVE_VECTOR:
                    x, y = get_vertical_horizontal_value(vector.magnetude, vector.angle)
                    x += starting_point[0]
                    y += starting_point[1]
                    

                    
                # Changing the starting poit
                starting_point = (x, y)
                
                # Updating the angle of the vector
                vector.angle += ANGULAR_SPEED_SCALE*vector.angular_speed
                
                # Increase the inde of the vector
                index_vector += 1
            
            # Addind the coordonnate at the list    
            marker_2_list.append(starting_point)

            
def draw_text(text, font, color, surface, x, y):
    
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)
    
def compute_vector(number_of_vector):
    
    dt = 1 / len(drawing_list)
    nb_t = len(drawing_list)
    
    for n in range(number_of_vector):
        
        for n in [n, -n]:
            Cn = 0 + 0j
            omega = -2*n*np.pi
            
            t_pos = 0
            for t in np.arange(0, 1, dt):
                
                f_of_t = drawing_list[t_pos][0] - WIDTH//2 + 1j*drawing_list[t_pos][1] - 1j*(HEIGHT // 2)
                
                Cn +=  f_of_t*(np.cos(omega*t) + 1j*np.sin(omega*t))*dt
            
                t_pos += 1
            
            # Compute the caracteristics of the new vector
            magnetude, angle = get_magnetude_initial_angle(Cn)        
            vectors_list.append(Vector(magnetude=magnetude, angle=angle, angular_speed=n))
            
            # Don't loop for 0
            if n == 0:
                break
            

            
            
            
        
def draw_point():
    "This function will draw the shape of the mouse"
    
    for point in drawing_list:
        pygame.draw.circle(screen, POINT_COLOR, point, POINT_SIZE)     
        
def get_vertical_horizontal_value(magnetude:float, angle:float):
    "This function take the magnetude and the angle and return the x, y coordonnates of the point of the vector. The angle must be in radian"
    
    x = np.cos(angle)*magnetude
    y = np.sin(angle)*magnetude
    return x, y

def get_magnetude_initial_angle(expression_complex):
    "This function take the complexe expression and return the magnetude and the initial angle"
 
    magnetude = np.abs(expression_complex)
    angle = np.angle(expression_complex)
    return magnetude, angle

def draw_marker():
    "This function will draw the marker of the vector"

    
    if MARKER_ACTIVATION : 
        for i in range(len(marker_list[0: -1])):
            pygame.draw.line(screen, MARKER_COLOR,marker_list[i] , marker_list[i+1], MARKER_THICKNESS)
            
        
def vector_mode(vectors_list: list):
    "This function draws the Fourier vectors and adds a triangle at the end of each vector."
    
    # Set the starting point at the middle
    starting_point = (WIDTH // 2, HEIGHT // 2)
    
    index_vector = 0
    for vector in vectors_list: 
        
        if index_vector < NUMBER_ACTIVE_VECTOR:
            # Calculate the new position of the vector's end point
            x, y = get_vertical_horizontal_value(vector.magnetude, vector.angle)
            x += starting_point[0]
            y += starting_point[1]
            
            # Draw the line representing the vector
            pygame.draw.line(screen, LINE_COLOR, starting_point, (x, y), LINE_THICKNESS)
            
            # Draw the circle (if activated)
            if CERCLE_ACTIVATION:
                pygame.draw.circle(screen, CERCLE_COLOR, starting_point, vector.magnetude, CERCLE_THICKNESS)
            
            # Draw the triangle at the end of the vector
            if TRIANGLE_ACTIVATION:  # Optional condition if needed to toggle triangle drawing
                lenght_arrow = np.sqrt((starting_point[0]-x)**2 + (starting_point[1]-y)**2) / TRIANGLE_RATIO
                base_coordonate = (((TRIANGLE_RATIO - 1)*x + starting_point[0])/TRIANGLE_RATIO, ((TRIANGLE_RATIO - 1)*y + starting_point[1])/TRIANGLE_RATIO)
                
                # I want to daw a triangle with the center of the base base_coordonate, the lenght of the base lenght_arrow and the top of the triangle (x, y)
                # Calculate angle of the line from starting point to (x, y)
                angle = np.arctan2(y - starting_point[1], x - starting_point[0])
                
                # Calculate the half-length of the base
                half_base_length = lenght_arrow / 2
                
                # Calculate the two base vertices
                base_point1 = (
                    base_coordonate[0] + half_base_length * np.cos(angle + np.pi/2),
                    base_coordonate[1] + half_base_length * np.sin(angle + np.pi/2)
                )

                base_point2 = (
                    base_coordonate[0] + half_base_length * np.cos(angle - np.pi/2),
                    base_coordonate[1] + half_base_length * np.sin(angle - np.pi/2)
                )
                
                # Draw the triangle using pygame
                pygame.draw.polygon(screen, TRIANGLE_COLOR, [(x, y), base_point1, base_point2])
                
            # Changing the starting point for the next vector
            starting_point = (x, y)
        
        # Update the angle of the vector
        vector.angle += ANGULAR_SPEED_SCALE * vector.angular_speed
        
        # Increase the index of the vector
        index_vector += 1
    
    # Save the marker
    marker_list.append((x, y))
    if len(marker_list) > MARKER_MAX_DURATION:
        marker_list.pop(0)

def draw_grid(screen, width, height, interval=50):

    # Définition du centre de l'écran
    center_x, center_y = width // 2, height // 2

    # Dessiner les lignes verticales
    for x in range(0, width, interval):
        pygame.draw.line(screen, SECONDARY_GRID_COLOR, (x, 0), (x, height), 1)

    # Dessiner les lignes horizontales
    for y in range(0, height, interval):
        pygame.draw.line(screen, SECONDARY_GRID_COLOR, (0, y), (width, y), 1)

    # Tracer l'axe X en surlignant la ligne centrale horizontale
    pygame.draw.line(screen, MAIN_GRID_COLOR, (0, center_y), (width, center_y), 2)

    # Tracer l'axe Y en surlignant la ligne centrale verticale
    pygame.draw.line(screen, MAIN_GRID_COLOR, (center_x, 0), (center_x, height), 2)





    
# Main loop
show_command()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 1 pour le bouton gauche de la souris
                if not SINGLE_CLICK:
                        if not POINT_PER_POINT_ACTIVATION:
                            left_click = True
                        else:
                            drawing_list.append(pygame.mouse.get_pos())
                else: 
                    drawing_list.append(pygame.mouse.get_pos())

        # Détecter le relâchement du bouton gauche de la souris
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                left_click = False
                
        if event.type == pygame.KEYDOWN:
            
            # Calculer les differents vecteurs
            if event.key == pygame.K_RETURN:
                compute_vector(NUMBER_OF_VECTOR_CALCULATED)
                VECTOR_ACTIVATION = True
            
            # Control number of vectors
            if event.key == pygame.K_UP:
                NUMBER_ACTIVE_VECTOR += 1
            elif event.key == pygame.K_DOWN:
                if NUMBER_ACTIVE_VECTOR > 1:
                    NUMBER_ACTIVE_VECTOR -= 1
            
            # Remove the point
            if event.key == pygame.K_LEFT:
                drawing_list = drawing_list[:-60]
            
            # Add the point
            if event.key == pygame.K_d:
                drawing_list = add_element_drawing_list(drawing_list)
                
                
    # Fill the background
    screen.fill(BG_COLOR)
    
    # Dessiner le repère orthonormé
    draw_grid(screen, WIDTH, HEIGHT, interval=50)

    # Draw everything

    if not VECTOR_ACTIVATION: 
        # Draw the picture
        if PICTURE_ACTIVATION:
            screen.blit(image, ((WIDTH - image_rect.width) // 2, (HEIGHT - image_rect.height) // 2))

        draw_point()
        if left_click:
            drawing_list.append(pygame.mouse.get_pos())
    else: 
        
        vector_mode(vectors_list=vectors_list)
        draw_marker()
        draw_marker_2(vectors_list_temp=vectors_list)
        
        
        
    
    
    # Draw state
    draw_text(f"Number of points: {len(drawing_list)}", font, (255, 255, 255), screen, WIDTH // 2, HEIGHT - 50)
    draw_text(f"Number of vectors: {NUMBER_ACTIVE_VECTOR}", font, (255, 255, 255), screen, WIDTH // 2, HEIGHT - 30)        
        
        
    
    
    # Update the display
    pygame.display.flip()
    
    # Set up the speed
    clock.tick(TICK_SPEED)

    # Show state
    
# Clean up
pygame.quit() -1
sys.exit()