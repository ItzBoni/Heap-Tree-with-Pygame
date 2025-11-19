import pygame
import heapLogic as hl
import math

hp = hl.heapLogic()
hp.agregar(67)
hp.agregar(2004)


# pyGame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)
running = True


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

    screen.fill("gray")

    # compute positions for the current heap
    positions = compute_heap_positions(len(hp.monti), screen.get_width(), top_margin=60, level_height=110)

    # draw nodes (iterate starting at index 1 so heap uses 1-based indices)
    node_w, node_h = 100, 50

    # draw edges (parent -> children) using computed positions
    for idx in range(1, hp.tam+1):
        parent_pos = positions[idx]
        if parent_pos is None:
            continue
        px, py = parent_pos
        # children indices in array-backed heap
        for child_idx in (2 * idx, 2 * idx + 1):
            if child_idx <= hp.tam and child_idx < len(positions):
                child_pos = positions[child_idx]
                if child_pos is None:
                    continue
                cx, cy = child_pos
                # draw line from bottom-center of parent to top-center of child
                start = (px, py + node_h // 2)
                end = (cx, cy - node_h // 2)
                pygame.draw.line(screen, (0, 0, 0), start, end, 3)

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
        screen.blit(text_surf, text_rect)

    pygame.display.flip()
    clock.tick(60)
