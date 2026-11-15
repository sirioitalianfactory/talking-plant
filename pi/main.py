"""Raspberry Pi display demo. Uses simulated readings; no hardware connected."""
import argparse
import math
import time

from pi.health import PROFILES, evaluate

def run(fullscreen=False):
    import pygame
    pygame.init()
    flags = pygame.FULLSCREEN if fullscreen else pygame.RESIZABLE
    screen = pygame.display.set_mode((800, 600), flags)
    pygame.display.set_caption("Talking Plant")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 26, bold=True)
    small = pygame.font.SysFont("monospace", 19)
    index = 0
    running = True
    start = time.monotonic()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in (pygame.K_RIGHT, pygame.K_LEFT):
                    index = (index + (1 if event.key == pygame.K_RIGHT else -1)) % len(PROFILES)
        w, h = screen.get_size()
        t = time.monotonic() - start
        soil = 50 + 36 * math.sin(t / 13)
        light = 500 + 440 * math.sin(t / 17)
        temp = 23 + 9 * math.sin(t / 23)
        profile = PROFILES[index]
        mood, states = evaluate(soil, light, temp, profile)
        palette = {"happy": (119, 227, 159), "neutral": (247, 211, 122),
                   "worried": (255, 164, 107), "sad": (241, 119, 131)}
        color = palette[mood]
        screen.fill((17, 24, 24))
        cx, cy = w // 2, h // 2 - 40
        unit = max(4, min(w, h) // 75)
        def rect(x, y, ww, hh, c=color):
            pygame.draw.rect(screen, c, (cx + x * unit, cy + y * unit, ww * unit, hh * unit))
        rect(-18, -18, 36, 36)
        rect(-10, -7, 5, 5, (17, 24, 24))
        rect(5, -7, 5, 5, (17, 24, 24))
        dark = (17, 24, 24)
        if mood == "happy":
            rect(-8, 6, 16, 2, dark)
            rect(-10, 3, 2, 3, dark)
            rect(8, 3, 2, 3, dark)
        elif mood == "neutral":
            rect(-8, 5, 16, 2, dark)
        elif mood == "worried":
            rect(-7, 5, 14, 2, dark)
            rect(6, 3, 2, 2, dark)
        else:
            rect(-8, 2, 16, 2, dark)
            rect(-10, 4, 2, 4, dark)
            rect(8, 4, 2, 4, dark)
        def center(text, y, font_obj, col=(235, 242, 235)):
            surface = font_obj.render(text, True, col)
            screen.blit(surface, surface.get_rect(center=(w // 2, y)))
        center(profile.name, max(28, h // 11), font)
        center(mood.upper(), min(h - 104, cy + 23 * unit), font, color)
        center(f"Soil {soil:.0f}% ({states['soil']})  Light {light:.0f} lux ({states['light']})", h - 65, small)
        center(f"Temperature {temp:.1f} C ({states['temperature']})", h - 36, small)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock", action="store_true", help="Use simulated readings (only available mode)")
    parser.add_argument("--fullscreen", action="store_true")
    args = parser.parse_args()
    if not args.mock:
        parser.error("Only --mock is implemented; real sensor adapters are not yet available")
    run(fullscreen=args.fullscreen)
