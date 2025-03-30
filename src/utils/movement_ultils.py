from src.config import SCREEN_HEIGHT, SCREEN_WIDTH, CELL_SIZE

# def check_collision(pixel_x, pixel_y, direction, speed, objects_block, map_matrix):
#     new_pixel_x, new_pixel_y = pixel_x, pixel_y

#     # Calculate the new position based on the direction and speed
#     if direction == "l":
#         new_pixel_x = pixel_x - speed
#     elif direction == "r":
#         new_pixel_x = pixel_x + speed
#     elif direction == "u":
#         new_pixel_y = pixel_y - speed
#     elif direction == "d":
#         new_pixel_y = pixel_y + speed

#     top_left = (new_pixel_x, new_pixel_y)
#     top_right = (new_pixel_x +  objects_block[0] - 1, new_pixel_y)
#     bottom_left = (new_pixel_x, new_pixel_y + objects_block[1] - 1)
#     bottom_right = (new_pixel_x + objects_block[0] - 1, new_pixel_y + objects_block[1] - 1)

#     for pos in [top_left, top_right, bottom_left, bottom_right]:
#         if pos[0] < 0 or pos[1] < 0 or pos[0] >= SCREEN_WIDTH or pos[1] >= SCREEN_HEIGHT:
#             return True

#         if map_matrix[pos[1] // CELL_SIZE[1]][pos[0] // CELL_SIZE[0]] == 1:
#             return True
        
#     return False

def check_collision(pixel_x, pixel_y, direction, speed, objects_block, map_matrix):
    new_pixel_x, new_pixel_y = pixel_x, pixel_y

    # Calculate the new position based on the direction and speed
    if direction == "l":
        new_pixel_x = pixel_x - speed
    elif direction == "r":
        new_pixel_x = pixel_x + speed
    elif direction == "u":
        new_pixel_y = pixel_y - speed
    elif direction == "d":
        new_pixel_y = pixel_y + speed

    # Adjust collision points based on direction to prevent early collision detection
    if direction == "l":
        # For left movement, check left edge points
        points_to_check = [
            (new_pixel_x, new_pixel_y),  # top left
            (new_pixel_x, new_pixel_y + objects_block[1] - 1)  # bottom left
        ]
    elif direction == "r":
        # For right movement, check right edge points
        points_to_check = [
            (new_pixel_x + objects_block[0] - 1, new_pixel_y),  # top right
            (new_pixel_x + objects_block[0] - 1, new_pixel_y + objects_block[1] - 1)  # bottom right
        ]
    elif direction == "u":
        # For upward movement, check top edge points
        points_to_check = [
            (new_pixel_x, new_pixel_y),  # top left
            (new_pixel_x + objects_block[0] - 1, new_pixel_y)  # top right
        ]
    elif direction == "d":
        # For downward movement, check bottom edge points
        points_to_check = [
            (new_pixel_x, new_pixel_y + objects_block[1] - 1),  # bottom left
            (new_pixel_x + objects_block[0] - 1, new_pixel_y + objects_block[1] - 1)  # bottom right
        ]
    else:
        # If no direction, check all corners
        points_to_check = [
            (new_pixel_x, new_pixel_y),  # top left
            (new_pixel_x + objects_block[0] - 1, new_pixel_y),  # top right
            (new_pixel_x, new_pixel_y + objects_block[1] - 1),  # bottom left
            (new_pixel_x + objects_block[0] - 1, new_pixel_y + objects_block[1] - 1)  # bottom right
        ]

    # Check if any of the points would collide with a wall
    for pos in points_to_check:
        # Check if the position is out of bounds
        if pos[0] < 0 or pos[1] < 0:
            return True
            
        if pos[0] >= SCREEN_WIDTH or pos[1] >= SCREEN_HEIGHT:
            return True

        # Check if the position is a wall in the matrix
        matrix_x = int(pos[0] // CELL_SIZE[0])
        matrix_y = int(pos[1] // CELL_SIZE[1])
        
        if matrix_x >= len(map_matrix[0]) or matrix_y >= len(map_matrix):
            return True
        if map_matrix[matrix_y][matrix_x] == 1:
            return True
        
    return False

def calculate_coords(pos):
    x, y = pos
    return x * CELL_SIZE[0], y * CELL_SIZE[1]
        
