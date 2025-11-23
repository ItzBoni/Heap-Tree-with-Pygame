import pygame
import heapLogic as hl
import math

hp = hl.heapLogic()

# pyGame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)
running = True

#Input
user_input = ""
num_to_add = None
box_click = False
text_box = pygame.Rect(0,680,100,40)
color = pygame.Color('blue')


def compute_heap_positions(length, screen_width, top_margin=50, level_height=110, start_index=1):
    """Return a list of (x,y) positions for a heap stored in an array of given
    `length` where valid heap indices start at `start_index` (1 by default).

    The returned list has the same length as the array; index 0 will be `None`
    when `start_index` is 1 so callers can index positions by the heap index.
    """
    positions = [None] * length
    if length <= start_index:
        return positions

    # compute positions for heap indices start_index..length-1
    for k in range(start_index, length):
        # k is the heap index (1-based for a typical heap representation)
        level = int(math.floor(math.log2(k)))
        level_start = 2 ** level
        index_in_level = k - level_start
        nodes_in_level = 2 ** level
        # spacing leaves margins at left/right by dividing by (nodes_in_level+1)
        spacing = screen_width / (nodes_in_level + 1)
        x = spacing * (index_in_level + 1)
        y = top_margin + level * level_height
        positions[k] = (int(x), int(y))

    return positions

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if text_box.collidepoint(event.pos):
                box_click = True
            else:
                box_click = False
        if event.type == pygame.KEYDOWN and box_click:
            if event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            elif event.key == pygame.K_RETURN:
                num_to_add = int(user_input)
                user_input = ""
            else:
                user_input += event.unicode

    screen.fill("gray")

    # compute positions for the current heap
    positions = compute_heap_positions(len(hp.monti), screen.get_width(), top_margin=60, level_height=110)

    # draw nodes (iterate starting at index 1 so heap uses 1-based indices)
    node_w, node_h = 100, 50
    for idx in range(1, hp.tam+1):
        pos = positions[idx]
        if pos is None:
            continue
        x, y = pos
        rect = pygame.Rect(x - node_w // 2, y - node_h // 2, node_w, node_h)
        pygame.draw.rect(screen, (255, 255, 255), rect)  # fill
        pygame.draw.rect(screen, (0, 0, 0), rect, 3, 8)  # border rounded

        # render the number centered in the rect
        text_surf = font.render(str(hp.monti[idx]), True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf,text_rect)

    #Receive user input
    if box_click:
        color = pygame.Color('green')
    else:
        color = pygame.Color('blue')
    pygame.draw.rect(screen, color, text_box, 4)
    user_surf = font.render(user_input, True,'black')
    screen.blit(user_surf, (text_box.x + 5, text_box.y + 5))
    text_box.w = max(100,user_surf.get_width()+10)

    #Append to the heap
    if num_to_add:
        hp.agregar(num_to_add)
        num_to_add = None


    pygame.display.flip()
    clock.tick(60)
