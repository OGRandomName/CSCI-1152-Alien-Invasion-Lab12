import pygame
import sys
import pytest

# Initialize pygame
pygame.init()

# Screen setup
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ship Movement")

# Ship setup
ship_image = pygame.image.load("Assets/images/ship.png").convert_alpha()
ship_rect = ship_image.get_rect(center=(screen_width // 2, screen_height // 2))
ship_speed = 5

# Laser setup
laser_image = pygame.image.load("Assets/images/laserBlast.png").convert_alpha()
laser_speed = 10
lasers = []  # list to hold active lasers

# 🔊 Load laser sound (linked to your mp3 file)
laser_sound = pygame.mixer.Sound("Assets/sound/laser.mp3")

# 🔧 Shooting cooldown
laser_cooldown = 180  # milliseconds between shots
last_shot_time = 0

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        ship_rect.x -= ship_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        ship_rect.x += ship_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        ship_rect.y -= ship_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        ship_rect.y += ship_speed

    # 🚀 Continuous shooting when holding SPACE
    if keys[pygame.K_SPACE]:
        current_time = pygame.time.get_ticks()
        if current_time - last_shot_time > laser_cooldown:
            laser_rect = laser_image.get_rect(midbottom=ship_rect.midtop)
            lasers.append(laser_rect)
            laser_sound.play()  # 🔊 play sound
            last_shot_time = current_time

    # Update lasers
    for laser in lasers[:]:
        laser.y -= laser_speed
        if laser.bottom < 0:  # remove if off-screen
            lasers.remove(laser)

    # Drawing
    screen.fill((0, 0, 0))  # Black background
    screen.blit(ship_image, ship_rect)
    for laser in lasers:
        screen.blit(laser_image, laser)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()