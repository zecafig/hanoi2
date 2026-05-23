"""Pygame-ce application for Tower of Hanoi."""

from __future__ import annotations

import sys

import pygame

from hanoi.core import HanoiGame, PieceCountPrompt

WIDTH = 1080
HEIGHT = 720
FPS = 60

# Material 3-inspired light scheme tokens.
PRIMARY = (0, 104, 116)
ON_PRIMARY = (255, 255, 255)
PRIMARY_CONTAINER = (151, 240, 255)
ON_PRIMARY_CONTAINER = (0, 31, 36)
SECONDARY = (74, 98, 103)
ON_SECONDARY = (255, 255, 255)
TERTIARY = (101, 91, 151)
ERROR = (186, 26, 26)

BACKGROUND = (245, 250, 251)
SURFACE = (248, 250, 251)
SURFACE_VARIANT = (219, 228, 230)
SURFACE_CONTAINER = (236, 242, 243)
OUTLINE = (111, 121, 123)
ON_SURFACE = (23, 29, 30)
ON_SURFACE_VARIANT = (63, 72, 74)

PEG_COLOR = (100, 120, 124)
BASE_COLOR = (79, 102, 107)
CURSOR_COLOR = PRIMARY

DISK_COLORS = [
    (0, 188, 212),
    (3, 169, 244),
    (33, 150, 243),
    (30, 136, 229),
    (25, 118, 210),
    (21, 101, 192),
    (13, 71, 161),
    (46, 125, 50),
    (102, 187, 106),
    (255, 202, 40),
    (255, 167, 38),
    (244, 81, 30),
]

FONT_CANDIDATES = [
    "Noto Sans",
    "DejaVu Sans",
    "Helvetica",
    "Arial",
]


def _wrap_text(font: pygame.font.Font, text: str, max_width: int) -> list[str]:
    words = text.split()
    if not words:
        return [""]

    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if font.size(candidate)[0] <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def _blit_wrapped_text(
    screen: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    color: tuple[int, int, int],
    x: int,
    y: int,
    max_width: int,
    *,
    max_lines: int = 2,
    line_gap: int = 4,
) -> int:
    lines = _wrap_text(font, text, max_width)
    rendered_lines = lines[:max_lines]
    if len(lines) > max_lines:
        last = rendered_lines[-1]
        ellipsis = "..."
        while last and font.size(last + ellipsis)[0] > max_width:
            last = last[:-1]
        rendered_lines[-1] = (last + ellipsis).rstrip()

    line_height = font.get_linesize()
    for idx, line in enumerate(rendered_lines):
        surface = font.render(line, True, color)
        screen.blit(surface, (x, y + idx * (line_height + line_gap)))

    return y + len(rendered_lines) * line_height + max(0, len(rendered_lines) - 1) * line_gap


def _draw_background(screen: pygame.Surface) -> None:
    for y in range(HEIGHT):
        blend = y / HEIGHT
        top = BACKGROUND
        bottom = (230, 239, 241)
        r = int(top[0] * (1 - blend) + bottom[0] * blend)
        g = int(top[1] * (1 - blend) + bottom[1] * blend)
        b = int(top[2] * (1 - blend) + bottom[2] * blend)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))


def _disk_color(size: int) -> tuple[int, int, int]:
    return DISK_COLORS[(size - 1) % len(DISK_COLORS)]


def _tower_centers() -> list[int]:
    span = WIDTH // 4
    return [span, span * 2, span * 3]


def _load_font(size: int, *, bold: bool = False) -> pygame.font.Font:
    for font_name in FONT_CANDIDATES:
        font_path = pygame.font.match_font(font_name, bold=bold)
        if font_path is not None:
            return pygame.font.Font(font_path, size)
    return pygame.font.Font(None, size)


def _draw_elevated_surface(
    screen: pygame.Surface,
    rect: pygame.Rect,
    *,
    radius: int,
    fill: tuple[int, int, int],
    border: tuple[int, int, int],
    shadow_alpha: int = 35,
) -> None:
    shadow = pygame.Surface((rect.width + 12, rect.height + 12), pygame.SRCALPHA)
    pygame.draw.rect(shadow, (0, 0, 0, shadow_alpha), (6, 8, rect.width, rect.height), border_radius=radius)
    screen.blit(shadow, (rect.x - 6, rect.y - 8))
    pygame.draw.rect(screen, fill, rect, border_radius=radius)
    pygame.draw.rect(screen, border, rect, width=1, border_radius=radius)


def _draw_board(
    screen: pygame.Surface,
    game: HanoiGame,
    title_font: pygame.font.Font,
    text_font: pygame.font.Font,
    autoplay_remaining: int,
) -> None:
    top_bar = pygame.Rect(40, 20, WIDTH - 80, 118)
    _draw_elevated_surface(
        screen,
        top_bar,
        radius=22,
        fill=SURFACE,
        border=SURFACE_VARIANT,
        shadow_alpha=24,
    )

    metrics_card = pygame.Rect(top_bar.right - 286, top_bar.y + 26, 250, 70)
    _draw_elevated_surface(
        screen,
        metrics_card,
        radius=16,
        fill=PRIMARY_CONTAINER,
        border=(128, 220, 236),
        shadow_alpha=18,
    )

    left_x = 62
    left_y = 34
    left_w = metrics_card.x - left_x - 24

    title = title_font.render("Tower of Hanoi", True, ON_SURFACE)
    screen.blit(title, (left_x, left_y))

    subtitle_y = left_y + title.get_height() + 6
    _blit_wrapped_text(
        screen,
        text_font,
        "Arrow keys move cursor. Enter/Space picks or places. A autoplay. N new, R reset, Q quit.",
        ON_SURFACE_VARIANT,
        left_x,
        subtitle_y,
        left_w,
        max_lines=2,
    )

    status = f"Pieces {game.piece_count}   Moves {game.move_count}"
    status_text = text_font.render(status, True, ON_PRIMARY_CONTAINER)
    screen.blit(status_text, (metrics_card.x + 14, metrics_card.y + 10))

    optimal_text_card = text_font.render(
        f"Optimal {game.get_optimal_moves()}", True, ON_PRIMARY_CONTAINER
    )
    screen.blit(optimal_text_card, (metrics_card.x + 14, metrics_card.y + 40))

    info_y = top_bar.bottom + 8
    if autoplay_remaining > 0:
        auto_chip = pygame.Rect(56, info_y, 266, 30)
        pygame.draw.rect(screen, PRIMARY_CONTAINER, auto_chip, border_radius=14)
        pygame.draw.rect(screen, (128, 220, 236), auto_chip, width=1, border_radius=14)
        auto_text = text_font.render(f"Autoplay {autoplay_remaining} moves", True, PRIMARY)
        screen.blit(auto_text, (auto_chip.x + 12, auto_chip.y + 4))

    win_y = info_y
    if autoplay_remaining > 0:
        win_y += 34

    if game.has_won:
        win_text = title_font.render("Solved! Press N for a new challenge.", True, TERTIARY)
        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, win_y))

    board_top = win_y + (title_font.get_height() + 10 if game.has_won else 8)
    board_rect = pygame.Rect(46, board_top, WIDTH - 92, HEIGHT - board_top - 46)
    _draw_elevated_surface(
        screen,
        board_rect,
        radius=26,
        fill=SURFACE_CONTAINER,
        border=SURFACE_VARIANT,
        shadow_alpha=30,
    )

    centers = _tower_centers()
    base_y = HEIGHT - 84
    peg_h = 280
    disk_h = 22
    min_w = 70
    max_w = 250

    pygame.draw.rect(screen, BASE_COLOR, (120, base_y, WIDTH - 240, 18), border_radius=9)

    for i, center in enumerate(centers):
        pygame.draw.rect(screen, PEG_COLOR, (center - 6, base_y - peg_h, 12, peg_h), border_radius=6)

        if i == game.cursor_tower:
            pygame.draw.rect(
                screen,
                CURSOR_COLOR,
                (center - 95, base_y - peg_h - 40, 190, 30),
                width=4,
                border_radius=8,
            )

        if game.selected_tower == i:
            pygame.draw.circle(screen, PRIMARY, (center, base_y - peg_h - 55), 11)
            pygame.draw.circle(screen, ON_PRIMARY, (center, base_y - peg_h - 55), 11, width=2)

        for depth, piece in enumerate(game.towers[i]):
            width_ratio = (piece - 1) / max(1, game.piece_count - 1)
            disk_w = int(min_w + (max_w - min_w) * width_ratio)
            top = base_y - disk_h * (depth + 1)
            disk_rect = pygame.Rect(center - disk_w // 2, top, disk_w, disk_h - 2)
            color = _disk_color(piece)
            pygame.draw.rect(screen, color, disk_rect, border_radius=8)
            pygame.draw.rect(screen, (255, 255, 255), disk_rect, width=1, border_radius=8)

    footer_note = text_font.render("Goal: move all disks to the right-most tower", True, ON_SURFACE_VARIANT)
    screen.blit(footer_note, (62, HEIGHT - 34))


def _draw_prompt(
    screen: pygame.Surface,
    prompt: PieceCountPrompt,
    title_font: pygame.font.Font,
    text_font: pygame.font.Font,
    purpose: str,
) -> None:
    _draw_background(screen)

    card = pygame.Rect(WIDTH // 2 - 260, HEIGHT // 2 - 180, 520, 320)
    _draw_elevated_surface(
        screen,
        card,
        radius=24,
        fill=SURFACE,
        border=SURFACE_VARIANT,
        shadow_alpha=34,
    )

    title = title_font.render("Tower of Hanoi", True, ON_SURFACE)
    description = text_font.render(purpose, True, ON_SURFACE_VARIANT)
    label = text_font.render(
        f"Piece count ({prompt.min_count}-{prompt.max_count}):", True, ON_SURFACE
    )

    field = pygame.Rect(card.x + 42, card.y + 168, card.width - 84, 62)
    pygame.draw.rect(screen, SURFACE, field, border_radius=12)
    border_color = ERROR if prompt.error else OUTLINE
    pygame.draw.rect(screen, border_color, field, width=2, border_radius=12)

    entered = title_font.render(prompt.text or "_", True, PRIMARY)
    hints = text_font.render("Type digits, Enter to confirm, Backspace to edit.", True, ON_SURFACE_VARIANT)

    screen.blit(title, (card.x + 42, card.y + 32))
    screen.blit(description, (card.x + 42, card.y + 88))
    screen.blit(label, (card.x + 42, card.y + 138))
    screen.blit(entered, (field.x + 12, field.y + 12))
    screen.blit(hints, (card.x + 42, card.y + 250))

    if prompt.error:
        error_text = text_font.render(prompt.error, True, ERROR)
        screen.blit(error_text, (card.x + 42, card.y + 236))


def _event_to_prompt_key(event: pygame.event.Event) -> str | None:
    if event.key == pygame.K_BACKSPACE:
        return "BACKSPACE"
    if event.key in {pygame.K_RETURN, pygame.K_KP_ENTER}:
        return "ENTER"
    if event.unicode.isdigit():
        return event.unicode
    return None


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Tower of Hanoi")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    title_font = _load_font(38, bold=True)
    text_font = _load_font(23)

    prompt = PieceCountPrompt()
    game: HanoiGame | None = None
    mode = "prompt"
    prompt_purpose = "Choose your starting puzzle size."
    autoplay_moves: list[tuple[int, int]] = []
    autoplay_timer_ms = 0
    autoplay_delay_ms = 400

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                    continue

                if mode == "prompt":
                    prompt_key = _event_to_prompt_key(event)
                    if prompt_key is not None:
                        value = prompt.apply_key(prompt_key)
                        if value is not None:
                            if game is None:
                                game = HanoiGame(value)
                            else:
                                game.start_new_game(value)
                            mode = "game"
                            prompt.clear()
                    continue

                if game is None:
                    continue

                if event.key == pygame.K_n:
                    mode = "prompt"
                    prompt.clear()
                    prompt_purpose = "Enter a piece count for a new game."
                    autoplay_moves = []
                    autoplay_timer_ms = 0
                elif event.key == pygame.K_r:
                    game.reset()
                    autoplay_moves = []
                    autoplay_timer_ms = 0
                elif event.key == pygame.K_a:
                    game.reset()
                    game.selected_tower = None
                    autoplay_moves = game.solve()
                    autoplay_timer_ms = 0
                elif event.key == pygame.K_LEFT:
                    if not autoplay_moves:
                        game.move_cursor(-1)
                elif event.key == pygame.K_RIGHT:
                    if not autoplay_moves:
                        game.move_cursor(1)
                elif event.key in {pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER}:
                    if not autoplay_moves:
                        game.select_or_move(game.cursor_tower)

            elif event.type == pygame.MOUSEBUTTONDOWN and mode == "game" and game is not None:
                if not autoplay_moves:
                    mouse_x, _mouse_y = pygame.mouse.get_pos()
                    centers = _tower_centers()
                    distances = [abs(mouse_x - center) for center in centers]
                    clicked_tower = distances.index(min(distances))
                    game.cursor_tower = clicked_tower
                    game.select_or_move(clicked_tower)

        frame_ms = clock.tick(FPS)

        if mode == "game" and game is not None and autoplay_moves and not game.has_won:
            autoplay_timer_ms += frame_ms
            if autoplay_timer_ms >= autoplay_delay_ms:
                source, target = autoplay_moves.pop(0)
                game.select_or_move(source)
                game.select_or_move(target)
                autoplay_timer_ms = 0

        if mode == "prompt":
            _draw_prompt(screen, prompt, title_font, text_font, prompt_purpose)
        else:
            _draw_background(screen)
            if game is not None:
                _draw_board(screen, game, title_font, text_font, len(autoplay_moves))

        pygame.display.flip()

    pygame.quit()
    sys.exit(0)
