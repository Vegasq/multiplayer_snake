import sys
import pygame
import json
import settings

from messages import NEW_CLIENT, GO_UP, GO_DOWN, GO_RIGHT, GO_LEFT, \
    GET_WORLD, CLIENT_RESET


class SnakeUI(object):
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)

    def __init__(self):
        pygame.init()

        self.size = self.width, self.height = settings.width, settings.height
        self.screen = pygame.display.set_mode(self.size)

    def get_color(self, obj):
        if obj == "#":
            return self.white
        elif obj == "@":
            return self.green
        elif obj == " ":
            return self.black
        elif obj == "*":
            return self.blue
        else:
            if "type" in obj:
                if obj["type"] == "SnakeCell":
                    if obj["alive"]:
                        return obj["color"]
                    else:
                        return self.red
        print("Unknown object: %s, len == %s" % (obj, len(obj)))
        return self.red

    def global_values(self, current_map):
        self.row_count = len(current_map)
        self.col_count = len(current_map[0])

        self.tile_width = self.width / self.col_count
        self.tile_height = self.height / self.row_count

    def get_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    return GO_LEFT
                if event.key == pygame.K_RIGHT:
                    return GO_RIGHT
                if event.key == pygame.K_UP:
                    return GO_UP
                if event.key == pygame.K_DOWN:
                    return GO_DOWN

                if event.key == pygame.K_r:
                    return CLIENT_RESET
                if event.key == pygame.K_q:
                    sys.exit()
        return None

    def draw(self, current_map):
        self.global_values(current_map)

        self.screen.fill(self.black)

        for y, row in enumerate(current_map):
            for x, col in enumerate(row):
                if current_map[y][x] in [" ", ""]:
                    continue

                pygame.draw.rect(
                    self.screen,
                    self.get_color(current_map[y][x]),
                    (
                        x*self.tile_width,
                        y*self.tile_height,
                        self.tile_width, self.tile_height
                    )
                )

        pygame.display.update()
