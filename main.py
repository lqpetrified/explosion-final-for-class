# Phys Box
# Author: lynn qiao
# Date: May 19 2026

import random

import pygame

pygame.init()

# COLOURS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# CONSTANTS
WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)


class Snow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((3, 3))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        # self.rect = pygame.FRect(self.rect)
        self.rect.centerx = random.uniform(375, 425)
        self.rect.centery = random.uniform(275, 325)
        self.y_vel = random.uniform(-6, 6)
        self.x_vel = random.uniform(-6, 6)
        self.bounce = 0.8

    def update(self):
        self.y_vel += 0.3

        self.x_vel *= 1.01

        self.rect.y += self.y_vel
        self.rect.x += self.x_vel
        if self.x_vel >= 4 or self.x_vel <= -4:
            self.x_vel *= 0.9


def main():
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Phys box")

    # variables
    bounce = 0.6
    pygame.mixer.init()
    bounce_sound = pygame.mixer.Sound("sounds/explode.mp3")
    done = False
    drag_active = False
    rainbow_active = False
    clock = pygame.time.Clock()
    snow_sprites = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    for _ in range(500):
        snow = Snow()
        all_sprites.add(snow)
        snow_sprites.add(snow)

    time_at_click = 0

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                drag_active = True

            if event.type == pygame.MOUSEBUTTONUP:
                drag_active = False
                # gets the time at release
                time_at_click = pygame.time.get_ticks()
                bounce_sound.play()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for sprite in all_sprites:
                        sprite.image.fill(
                            (
                                random.randint(0, 255),
                                random.randint(0, 255),
                                random.randint(0, 255),
                            )
                        )
                if event.key == pygame.K_1:
                    for sprite in all_sprites:
                        sprite.bounce = 0.8
                if event.key == pygame.K_2:
                    for sprite in all_sprites:
                        sprite.bounce = 0.6
                if event.key == pygame.K_3:
                    for sprite in all_sprites:
                        sprite.bounce = 0.4
                if event.key == pygame.K_4:
                    for sprite in all_sprites:
                        sprite.bounce = 0.2
                if event.key == pygame.K_5:
                    for sprite in all_sprites:
                        sprite.bounce = 0

                if event.key == pygame.K_8:
                    rainbow_active = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    for sprite in all_sprites:
                        sprite.image.fill((255, 255, 255))
                if event.key == pygame.K_8:
                    rainbow_active = False
                    for sprite in all_sprites:
                        sprite.image.fill(WHITE)

        # --- Game Logic
        all_sprites.update()

        if rainbow_active:
            for sprite in all_sprites:
                sprite.image.fill(
                    (
                        random.randint(0, 255),
                        random.randint(0, 255),
                        random.randint(0, 255),
                    )
                )

        if drag_active:
            for sprite in all_sprites:
                sprite.rect.centerx = pygame.mouse.get_pos()[0] + random.uniform(
                    -25, 25
                )
                sprite.rect.centery = pygame.mouse.get_pos()[1] + random.uniform(
                    -25, 25
                )
                sprite.y_vel = random.uniform(-6, 6)
                sprite.x_vel = random.uniform(-4, 4)
            # ths is here so it doesnt start counnting down when to let collide while dragging
            time_since_click = 0
        else:
            # time since click is the current time minus the time at click
            time_since_click = pygame.time.get_ticks() - time_at_click
        for sprite in all_sprites:
            if (sprite.rect.bottom + sprite.image.height) >= HEIGHT:
                if abs(sprite.y_vel) < 3 or sprite.rect.bottom < 20:
                    sprite.y_vel = 0
                else:
                    sprite.y_vel = -sprite.bounce * sprite.y_vel

            # if the time elapsed from last tick is > cooldown
            # set the last clicked time to this time
            # run the code below

            if time_since_click > 1500:
                collided = pygame.sprite.spritecollide(sprite, snow_sprites, False)

                if len(collided) > 1:
                    sprite.x_vel = -0.2 * sprite.x_vel

                    for spr in collided:
                        if spr != sprite:
                            spr.x_vel = -0.7 * spr.x_vel

            if sprite.rect.right + sprite.image.width >= WIDTH:
                sprite.x_vel = -sprite.bounce * sprite.x_vel
            if sprite.rect.left <= 0:
                sprite.rect.left = 1
                sprite.x_vel = -sprite.bounce * sprite.x_vel

        # --- Drawing
        screen.fill(BLACK)
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
