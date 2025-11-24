import pygame
import heapLogic as hl
import math

hp = hl.heapLogic()

# pyGame setup
pygame.init()
# Name of the window
pygame.display.set_caption("HEAP TREE WITH PYGAME by Bonilla & Vizcaíno")
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

#Input boxes:
node_boxes = dict()
node_click = False
position_removed = None
# Visual theme colors
EDGE_COLOR = (28, 58, 92)          # main edge color (dark bluish)
EDGE_SHADOW_COLOR = (180, 190, 200) # subtle shadow for edges
NODE_FILL_COLOR = (240, 248, 255)  # very light blue for node fill
NODE_BORDER_COLOR = (20, 40, 80)   # dark border
NODE_SHADOW_COLOR = (200, 210, 220) # node drop shadow
NODE_TEXT_COLOR = (18, 32, 64)      # node text

# Pending insertion animation state
pending_insertion = None
INsertion_DURATION_MS = 520


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

        ##Chech if there has been a click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if text_box.collidepoint(event.pos):
                box_click = True
            else:
                box_click = False

            for pos, rect_value in node_boxes.items():
                rect, value = rect_value
                
                if rect.collidepoint(event.pos):
                    node_click = True
                    position_removed = value
                    break
                else:
                    node_click = False

        if event.type == pygame.KEYDOWN and box_click:
            if event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            elif event.key == pygame.K_RETURN and user_input.strip() != "":
                # start an animated insertion from the input box to the target node position
                value = int(user_input)
                user_input = ""
                if pending_insertion is None:
                    future_positions = compute_heap_positions(len(hp.monti) + 1, screen.get_width(), top_margin=60, level_height=110)
                    target_index = hp.tam + 1
                    target_pos = future_positions[target_index] if target_index < len(future_positions) else (screen.get_width() // 2, 100)
                    pending_insertion = {
                        'value': value,
                        'start_pos': (text_box.centerx, text_box.centery),
                        'target_pos': target_pos,
                        'start_time': pygame.time.get_ticks(),
                        'duration': INsertion_DURATION_MS,
                    }
            else:
                user_input += event.unicode

    screen.fill("white")

    # compute positions for the current heap
    positions = compute_heap_positions(len(hp.monti), screen.get_width(), top_margin=60, level_height=110)

    # draw nodes (iterate starting at index 1 so heap uses 1-based indices)
    node_w, node_h = 100, 50

    # helper: sample a quadratic bezier curve P0->CP->P1
    def quad_bezier(p0, cp, p1, steps=18):
        pts = []
        for i in range(steps + 1):
            t = i / steps
            x = (1 - t) * (1 - t) * p0[0] + 2 * (1 - t) * t * cp[0] + t * t * p1[0]
            y = (1 - t) * (1 - t) * p0[1] + 2 * (1 - t) * t * cp[1] + t * t * p1[1]
            pts.append((int(x), int(y)))
        return pts

    # draw edges first so they appear under the nodes
    for idx in range(1, hp.tam + 1):
        parent_pos = positions[idx]
        if parent_pos is None:
            continue
        px, py = parent_pos
        parent_bottom = (px, py + node_h // 2 - 4)

        for child_idx in (2 * idx, 2 * idx + 1):
            if child_idx <= hp.tam and child_idx < len(positions):
                child_pos = positions[child_idx]
                if child_pos is None:
                    continue
                cx, cy = child_pos
                child_top = (cx, cy - node_h // 2 + 4)

                # control point: slightly above the midpoint for a gentle upward curve
                mid_x = (parent_bottom[0] + child_top[0]) / 2
                level_gap = abs(math.log2(child_idx) - math.log2(idx)) if idx > 0 else 1
                curve_offset = max(24, 36 - int(level_gap) * 6)
                cp = (mid_x, min(parent_bottom[1], child_top[1]) - curve_offset)

                points = quad_bezier(parent_bottom, cp, child_top, steps=20)

                # shadow (thicker, subtle)
                pygame.draw.lines(screen, EDGE_SHADOW_COLOR, False, points, 6)
                # main antialiased line on top
                try:
                    pygame.draw.aalines(screen, EDGE_COLOR, False, points)
                except Exception:
                    # fallback if aalines not available for some surfaces
                    pygame.draw.lines(screen, EDGE_COLOR, False, points, 3)

    # then draw nodes on top of the edges
    for idx in range(1, hp.tam+1):
        pos = positions[idx]
        if pos is None:
            continue
        x, y = pos
        rect = pygame.Rect(x - node_w // 2, y - node_h // 2, node_w, node_h)
        node_boxes[pos] = (rect, hp.monti[idx])
        # node fill with a soft drop shadow
        shadow_rect = rect.move(4, 6)
        pygame.draw.rect(screen, NODE_SHADOW_COLOR, shadow_rect, border_radius=8)
        pygame.draw.rect(screen, NODE_FILL_COLOR, rect, border_radius=8)  # fill
        pygame.draw.rect(screen, NODE_BORDER_COLOR, rect, 3, border_radius=8)  # border

        # render the number centered in the rect (bold-ish)
        text_surf = font.render(str(hp.monti[idx]), True, NODE_TEXT_COLOR)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    if hp.tam == 0:
        text_surf = font.render("Agrega un valor en el recuadro de abajo :)", True, "black")
        screen.blit(text_surf, (450, 320))

    #Receive user input
    if box_click:
        color = pygame.Color('green')
    else:
        color = pygame.Color('blue')

    pygame.draw.rect(screen, color, text_box, 4)
    user_surf = font.render(user_input, True,'black')
    screen.blit(user_surf, (text_box.x + 5, text_box.y + 5))
    text_box.w = max(100,user_surf.get_width()+10)

    # Handle pending insertion animation (draw moving node and finalize)
    if pending_insertion:
        now = pygame.time.get_ticks()
        elapsed = now - pending_insertion['start_time']
        t = min(1.0, elapsed / pending_insertion['duration'])
        # ease-out cubic for a smooth finish
        te = 1 - (1 - t) ** 3
        sx, sy = pending_insertion['start_pos']
        tx, ty = pending_insertion['target_pos']
        cx = int(sx + (tx - sx) * te)
        cy = int(sy + (ty - sy) * te)

        # small pop at the end
        scale = 1.0
        if t > 0.85:
            # quick little overshoot pulse
            overshoot_t = (t - 0.85) / 0.15
            scale = 1.0 + 0.08 * (1 - abs(1 - overshoot_t * 2))

        w = int(node_w * scale)
        h = int(node_h * scale)
        rect = pygame.Rect(cx - w // 2, cy - h // 2, w, h)
        shadow_rect = rect.move(4, 6)
        pygame.draw.rect(screen, NODE_SHADOW_COLOR, shadow_rect, border_radius=8)
        pygame.draw.rect(screen, NODE_FILL_COLOR, rect, border_radius=8)
        pygame.draw.rect(screen, NODE_BORDER_COLOR, rect, 3, border_radius=8)
        text_surf = font.render(str(pending_insertion['value']), True, NODE_TEXT_COLOR)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

        if t >= 1.0:
            hp.agregar(pending_insertion['value'])
            pending_insertion = None

    #Remove from the heap
    if node_click:
        hp.quitar(position_removed)
        position_removed = None

    pygame.display.flip()
    clock.tick(60)