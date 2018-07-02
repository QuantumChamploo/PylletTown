#! /usr/bin/env python


## Copyright (C) 2001  David Clark

## This program is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License
## as published by the Free Software Foundation; either version 2
## of the License, or (at your option) any later version.
 
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.


import pygame, pygame.image, pygame.mixer, pygame.font
import sys, math, os.path, string, whrandom, getopt
from pygame.locals import *
import pygame.draw


# We use the following sound and image container classes to ensure that
# we don't fill memory with identical surfaces for each on-screen object.

class Img: pass
class Snd: pass


class Player:
    # Our hero
    speed = 60.000     # pixels per second
    # each element of the frame_list tuple is a tuple of animation frames
    # for that state.
    frame_list = ( (pygame.Rect(0, 0, 16, 16), pygame.Rect(0, 0, 16, 16)),
                   (pygame.Rect(16, 0, 16, 16), pygame.Rect(32, 0, 16, 16)),
                   (pygame.Rect(48, 0, 16, 16), pygame.Rect(64, 0, 16, 16)),
                   (pygame.Rect(80, 0, 16, 16), pygame.Rect(96, 0, 16, 16)),
                   (pygame.Rect(112, 0, 16, 16), pygame.Rect(128, 0, 16, 16)) )
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 16, 16)
        self.colliderect = pygame.Rect(4, 0, 8, 16)
        self.position = (0.000, 0.000)
        self.vel_x = 0.000
        self.vel_y = 0.000
        self.frame = 0
        self.state = 0
        self.damaged = 0
        self.health = 100
        self.score = 0
        self.surface = Img.player
        self.weapon_switch_time = 0
        self.weapon_switch_duration = 600
        self.animate_time = 0
        self.animate_time_duration = 100
        self.current_weapon = 0
        self.damage_surface = Img.damage
        self.pain_time = 0
        self.pain_duration = 500
        self.weapons = [Pistol(),
                        Machinegun(),
                        Lasergun(),
                        Rocketlauncher(),
                        Flamethrower(),
                        Grenadethrower(),
                        Bombdropper()]


    def think(self):
        if self.animate_time <= timer.current_time:
            self.animate()
            self.animate_time = timer.current_time + self.animate_time_duration
        return

    
    def draw(self):
        self.rect.topleft = self.position
        self.colliderect.left = self.rect.left + 4
        self.colliderect.top = self.rect.top + 0
        if self.damaged > 0:
            display.blit(self.damage_surface, self.rect.topleft)
        display.blit(self.surface, self.rect.topleft, Player.frame_list[self.state][self.frame])
        dirtyrects.append(self.rect)
        self.damaged -= 1
        return

    
    def erase(self):
        display.blit(background, self.rect.topleft, self.rect)
        dirtyrects.append(pygame.Rect(self.rect))
        return

    
    def move(self, dest_xy):
        # Move player to the supplied coordinates. Does not check for collisions - you
        # could put a player in a wall or outside the map with this.
        self.position = dest_xy
        self.rect.topleft = dest_xy
        self.colliderect.left = self.rect.left + 4
        self.colliderect.top = self.rect.top + 0
        return


    def walk(self):
        # Move player to the supplied coordinates. Only allows movement if the destination
        # is clear.
        new_x = self.position[0] + self.vel_x
        new_y = self.position[1] + self.vel_y
        tmp_rect = pygame.Rect(new_x, new_y, 16, 16)
        tmp_colliderect = pygame.Rect(new_x + 4, new_y + 0, 8, 16)
        for monster in g_monsters:
            if tmp_colliderect.colliderect(monster.colliderect):
                return (0.0, 0.0)
        if tmp_colliderect.collidelist(level.impassable_rects) == -1:
            self.position = (new_x, new_y)
            self.rect.topleft = self.position
            self.colliderect.topleft = tmp_colliderect.topleft
        else:
            return (0.0, 0.0)
        for item in g_items:
            if tmp_colliderect.colliderect(item.rect):
                item.pickup()
        return (self.vel_x, self.vel_y)
        
        

    def animate(self):
        if self.frame == len(self.frame_list[self.state]) - 1:
            self.frame = 0
        else:
            self.frame += 1
        return


    def choose_next_weapon(self):
        if self.weapon_switch_time <= timer.current_time:
            # ok to switch
            while 1:
                self.current_weapon += 1
                if self.current_weapon == 7:
                    self.current_weapon = 0
                if self.weapons[self.current_weapon].ammo > 0:
                    break
            statusbar.draw(1, 1, 0)
            self.weapon_switch_time = timer.current_time + self.weapon_switch_duration
            if sound:
                play_sound(Snd.weapon_switch, 0.5)
        return
    

    def choose_prev_weapon(self):
        if self.weapon_switch_time <= timer.current_time:
            # ok to switch
            while 1:
                self.current_weapon -= 1
                if self.current_weapon == -1:
                    self.current_weapon = 6
                if self.weapons[self.current_weapon].ammo > 0:
                    break
            statusbar.draw(1, 1, 0)
            self.weapon_switch_time = timer.current_time + self.weapon_switch_duration
            if sound:
                play_sound(Snd.weapon_switch, 0.5)
        return


    def take_damage(self, damage):
        if not GOD:                          # This is the best line of code I've ever written :)
            self.health -= damage
            statusbar.draw(0, 0, 1)
            self.damaged = 15
            if self.pain_time <= timer.current_time:
                if sound:
                    play_sound(whrandom.choice(Snd.player_pain), 1.0)
                self.pain_time = timer.current_time + self.pain_duration
        return

    def animate_death(self):
        # we take over the game loop, and draw the player's death. Then we end.
        self.surface = Img.player_death
        if sound:
            play_sound(Snd.player_death, 1.0)
        #background.blit(display, (0,0))
        for src_offset in (0, 16, 32, 48, 64, 80, 96, 112):
            self.erase()
            display.blit(self.surface, self.rect.topleft, (src_offset, 0, 16, 16))
            pygame.display.update(self.rect)
            pygame.time.delay(500)
        # Display Game over and wait 2.5 seconds
        font = pygame.font.Font(os.path.join('images', 'younffp_.ttf'), 24)
        game_over_message = font.render('Game Over!', 1, (255, 255, 255))
        display.fill((0, 0, 216, 255), (256, 220, 128, 40))
        display.fill((0, 0, 128, 255), (260, 224, 120, 32))
        display.blit(game_over_message, (264, 228))
        pygame.display.flip()
        pygame.time.delay(2500)
        return
    
        



class Crosshair:
    # I played with 5 different crosshair movement techniques, and included
    # the best two in the game. The crosshair becomes unusably sluggish under
    # high load, since it's not normalized for frame rate. This should be fixed.
    acceldrag = 0.98
    mousedrag = 0.02
    
    def __init__(self, pos_x, pos_y):
        self.pos_x = float(pos_x)
        self.pos_y = float(pos_y)
        self.move_x = self.move_y = 0.0
        self.rect = pygame.Rect(pos_x, pos_y, 16, 16)
        self.surface = Img.crosshair


    def think(self):
        pass
        
    def draw(self):
        display.blit(self.surface, self.rect.topleft)
        dirtyrects.append(pygame.Rect(self.rect))
        
    def erase(self):
        display.blit(background, self.rect.topleft, self.rect)
        dirtyrects.append(pygame.Rect(self.rect))

    def move(self, mouse_move_x, mouse_move_y, player_movement):
        self.move_x += mouse_move_x * Crosshair.mousedrag 
        self.move_y += mouse_move_y * Crosshair.mousedrag 
        self.pos_x += self.move_x
        self.pos_y += self.move_y
        self.move_x *= Crosshair.acceldrag
        self.move_y *= Crosshair.acceldrag
        if ALT_MOUSE:
            self.pos_x += player_movement[0]
            self.pos_y += player_movement[1]

        if self.pos_x < 0.0:
            self.pos_x = 0.0
        elif self.pos_x > 624.0:
            self.pos_x = 624.0
        if self.pos_y < 0.0:
            self.pos_y = 0.0
        elif self.pos_y > 448.0:
            self.pos_y = 448.0

        self.rect.topleft = (self.pos_x, self.pos_y)


class Statusbar:
    
    def __init__(self):
        self.weapon_rect = pygame.Rect(0, 465, 112, 16)
        self.health_rect = pygame.Rect(490, 465, 150, 16)
        self.ammo_rect = pygame.Rect(300, 465, 150, 16)
        

    def draw(self, weapons_need_updating, ammo_needs_updating, health_needs_updating):
        if weapons_need_updating:
            for weapon_index in range(0, 7):
                if player.current_weapon == weapon_index:
                    display.blit(Img.weapons_selected, (weapon_index * 16, 465),
                                 player.weapons[weapon_index].rect)
                else:
                    display.blit(Img.weapons, (weapon_index * 16, 465),
                                 player.weapons[weapon_index].rect)
            dirtyrects.append(self.weapon_rect)

        if health_needs_updating:
            if player.health <= 1:
                return
            display.blit(Img.health_empty, self.health_rect.topleft)
            display.blit(Img.health_full, self.health_rect.topleft, (0,0, player.health, 16))
            dirtyrects.append(self.health_rect)

        if ammo_needs_updating:
            ammo_font_numbers = ammo_font.render(str(player.weapons[player.current_weapon].ammo),
                                                 1, WHITE)
            display.blit(ammo_font_erase, self.ammo_rect.topleft)
            display.blit(ammo_font_numbers, self.ammo_rect.topleft)
            dirtyrects.append(self.ammo_rect)
        return


    def rampup(self):
        # Animate the health bar increasing from 0 to the player's current health.
        for temphealth in range(0, player.health):
            display.blit(Img.health_full, self.health_rect.topleft, (0,0, temphealth, 16))
            pygame.display.update(self.health_rect)
            pygame.time.delay(10)
        return

    
class Pistol:
    def __init__(self):
        self.reload_duration = 750
        self.reload_time = 0
        self.rect = pygame.Rect(0, 0, 16, 16)
        self.ammo = 999      # unlimited

        
    def fire(self, position_xy, angle):
        if self.reload_time <= timer.current_time:
            if self.ammo > 0:         # not needed since we always have ammo.
                for i in range(0, 3): # more of a shotgun, really.
                    myangle = angle + whrandom.randint(-4, 4)
                    vel_x = (math.cos(math.pi * myangle / 180)) * Bullet.speed 
                    vel_y = (math.sin(math.pi * myangle / 180)) * Bullet.speed
                    bullets.append(Bullet(position_xy[0], position_xy[1], vel_x, vel_y, 1))
                if sound:
                    play_sound(Snd.shotgun, 0.25)
                self.reload_time = timer.current_time + self.reload_duration
                


class Machinegun:
    def __init__(self):
       self.reload_duration = 100
       self.reload_time = 0
       self.rect = pygame.Rect(16, 0, 16, 16)
       self.ammo = 50
       if DEBUG:
           self.ammo = 200
       

    def fire(self, position_xy, angle):
        if self.reload_time <= timer.current_time:
            if self.ammo > 0:
                self.ammo -= 1
                vel_x = (math.cos(math.pi * angle / 180)) * Bullet.speed 
                vel_y = (math.sin(math.pi * angle / 180)) * Bullet.speed
                bullets.append(Bullet(int(position_xy[0]), int(position_xy[1]), vel_x, vel_y, 1))
                self.reload_time = timer.current_time + self.reload_duration
                if sound:
                    play_sound(Snd.machinegun, 0.25)
                statusbar.draw(0, 1, 0)
                

    
class Lasergun:
    def __init__(self):
        self.reload_duration = 1000
        self.reload_time = 0
        self.rect = pygame.Rect(32, 0, 16, 16)
        self.ammo = 5
        if DEBUG:
            self.ammo = 25
        

    def fire(self, position_xy, angle):
        if self.reload_time <= timer.current_time:
            if self.ammo > 0:
                
                self.ammo -= 1
                delta_y = (math.sin(math.pi * angle / 180))
                delta_x = (math.cos(math.pi * angle / 180))
                laserbeams.append(Laserbeam(position_xy[0], position_xy[1], delta_x, delta_y, 1))
                self.reload_time = timer.current_time + self.reload_duration
                if sound:
                    play_sound(Snd.laser, 1.0)
                statusbar.draw(0, 1, 0)
                
        
    
class Rocketlauncher:
    def __init__(self):
        self.reload_duration = 2000
        self.reload_time = 0
        self.rect = pygame.Rect(48, 0, 16, 16)
        self.ammo = 5
        if DEBUG:
            self.ammo = 25
        
    def fire(self, position_xy, angle):
        if self.reload_time <= timer.current_time:
            if self.ammo > 0:
                self.ammo -= 1
                vel_x = (math.cos(math.pi * angle / 180)) * Rocket.speed 
                vel_y = (math.sin(math.pi * angle / 180)) * Rocket.speed
                g_rockets.append(Rocket(position_xy[0], position_xy[1], vel_x, vel_y, angle, 1))
                self.reload_time = timer.current_time + self.reload_duration
                if sound:
                    play_sound(Snd.rocket, 0.25)
                statusbar.draw(0, 1, 0)
                
                

class Flamethrower:
    def __init__(self):
        self.reload_time = 0
        self.reload_duration = 100
        self.rect = pygame.Rect(64, 0, 16, 16)
        self.ammo = 25
        if DEBUG:
            self.ammo = 100

            
    def fire(self, position_xy, angle):
        if self.reload_time <= timer.current_time:
            if self.ammo > 0:
                self.ammo -= 1
                vel_x = (math.cos(math.pi * angle / 180)) * Flame.speed 
                vel_y = (math.sin(math.pi * angle / 180)) * Flame.speed
                g_flames.append(Flame(position_xy[0], position_xy[1], vel_x, vel_y))
                self.reload_time = timer.current_time + self.reload_duration
                if sound:
                    play_sound(Snd.flame, 0.25)
                statusbar.draw(0, 1, 0)
        
    
        
class Grenadethrower:
    def __init__(self):
        self.reload_time = 0
        self.reload_duration = 750
        self.rect = pygame.Rect(80, 0, 16, 16)
        self.ammo = 10
        if DEBUG:
            self.ammo = 25
        
    def fire(self, origin_xy, target_xy):
        if self.reload_time <= timer.current_time:
            if self.ammo > 0:
                self.ammo -= 1
                g_grenades.append(Grenade(origin_xy[0], origin_xy[1], target_xy[0], target_xy[1]))
                self.reload_time = timer.current_time + self.reload_duration
                if sound:
                    play_sound(Snd.grenade, 0.75)
                statusbar.draw(0, 1, 0)
                
        

class Bombdropper:
    def __init__(self):
        self.reload_time = 0
        self.reload_duration = 3000
        self.rect = pygame.Rect(96, 0, 16, 16)
        self.ammo = 1
        if DEBUG:
            self.ammo = 1
        
    def fire(self, position_xy, angle):
        if self.reload_time <= timer.current_time:
            if self.ammo > 0:
                self.ammo -= 1
                self.reload_time = timer.current_time + self.reload_duration
                g_bombs.append(Bomb(position_xy[0], position_xy[1]))
                statusbar.draw(0, 1, 0)

                
class Bullet:
    speed = 200.000
    def __init__(self, position_x, position_y, vel_x, vel_y, friendly):
        self.rect = pygame.Rect(position_x, position_y, 1, 1)
        self.position_x = position_x
        self.position_y = position_y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.damage = 5
        self.friendly = friendly
        self.alive = 1

    def erase(self):
        display.fill(background.get_at(self.rect.topleft), self.rect)
        dirtyrects.append(pygame.Rect(self.rect))
        
    def draw(self):
        display.fill(WHITE, self.rect)
        dirtyrects.append(self.rect)
        
    def move(self):
        self.position_x += (self.vel_x * timer.frame_duration)
        self.position_y += (self.vel_y * timer.frame_duration)
        self.rect.topleft = (self.position_x, self.position_y)
        if not self.rect.colliderect(screenrect):
            self.alive = 0
        if self.rect.collidelist(level.impassable_rects) != -1:
            self.alive = 0
            g_decals.append(Bullet_Hole(self.rect.topleft))
        if self.friendly:
            for monster in g_monsters:
                if self.rect.colliderect(monster.colliderect):
                    self.alive = 0
                    g_decals.append(Blood(self.rect.topleft))
                    monster.take_damage(self.damage, 0)
        else:
            if self.rect.colliderect(player.colliderect):
                self.alive = 0
                g_decals.append(Blood(self.rect.topleft))
                player.take_damage(self.damage / 4)
        return

    def think(self):
        pass             # bullets don't think
    

class Laserbeam:
    def __init__(self, position_x, position_y, delta_x, delta_y, friendly):
        self.pixels = []
        self.damage = 40
        self.colour_number = 15
        self.fade_duration = 100
        self.fade_time = 0
        self.debug_time = 0
        self.origin_x = position_x
        self.origin_y = position_y
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.friendly = friendly
        self.origin_rect = pygame.Rect((position_x, position_y, 1, 1))
        self.terminus_rect = pygame.Rect((position_x, position_y, 1, 1))
        self.calculate_pixels()
        


    def calculate_pixels(self):
        if (abs(self.delta_x) > abs(self.delta_y)):             # line mainly horizontal
            x = int(self.origin_x)
            y = self.origin_y 
            while 1:
                self.terminus_rect.topleft = (x, y)
                if not screenrect.contains(self.terminus_rect):
                    return
                self.pixels.append(self.terminus_rect.topleft)
                if self.terminus_rect.collidelist(level.impassable_rects) != -1:
                    g_decals.append(Bullet_Hole(self.terminus_rect.topleft))
                    return
                if self.friendly:
                    for monster in g_monsters:
                        if self.terminus_rect.colliderect(monster.colliderect):
                            g_decals.append(Blood(self.terminus_rect.topleft))
                            monster.take_damage(self.damage, 0)
                            return
                else:
                    if self.terminus_rect.colliderect(player.colliderect):
                        g_decals.append(Blood(self.terminus_rect.topleft))
                        player.take_damage(self.damage)
                        return
                if self.delta_x > 0:
                    x += 1
                else:
                    x -= 1
                y += self.delta_y * abs(1/ self.delta_x)
                
                
        else:                                             # line mainly vertical
            x = self.origin_x
            y = int(self.origin_y)
            while 1:
                self.terminus_rect.topleft = (x, y)
                if not screenrect.contains(self.terminus_rect):
                    return
                self.pixels.append(self.terminus_rect.topleft)
                if self.terminus_rect.collidelist(level.impassable_rects) != -1:
                    g_decals.append(Bullet_Hole(self.terminus_rect.topleft))
                    return
                if self.friendly:
                    for monster in g_monsters:
                        if self.terminus_rect.colliderect(monster.colliderect):
                            g_decals.append(Blood(self.terminus_rect.topleft))
                            monster.take_damage(self.damage, 0)
                            return
                else:
                    if self.terminus_rect.colliderect(player.colliderect):
                        g_decals.append(Blood(self.terminus_rect.topleft))
                        player.take_damage(self.damage)
                        return
                if self.delta_y > 0:
                    y += 1
                else:
                    y -= 1
                x += self.delta_x * abs(1 / self.delta_y)
        

    

    def draw(self):
        rect = pygame.draw.line(display, (self.colour_number * 16, 0, 0), self.origin_rect.topleft, self.terminus_rect.topleft)
        dirtyrects.append(rect)
        

    


    def erase(self):
        for pixel in self.pixels:
            display.fill(background.get_at(pixel), (pixel[0], pixel[1], 1, 1))
        dirtyrects.append(self.origin_rect.union(self.terminus_rect))
        
        
    
    def think(self):
        if self.fade_time > timer.current_time:
            return
        else:
            self.colour_number -= 1
            self.fade_time = timer.current_time + self.fade_duration


class Rocket:
    speed = 100.000
    damage = 20
    def __init__(self, position_x, position_y, vel_x, vel_y, angle, friendly):
        self.position_x = position_x - 8 
        self.position_y = position_y - 8
        self.smoke_interval = 200
        self.smoke_time = 0
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.damage = Rocket.damage
        self.surface = Img.rocket
        self.friendly = friendly
        self.rect = pygame.Rect(position_x, position_y, 16, 16)
        self.colliderect = pygame.Rect(self.rect.left + 4, self.rect.top + 4, 8, 8)
        # determine src_rect and colliderect from angle
        # This can be improved, since the checks are sequential.
        if angle < 0:
            angle += 360
        if angle >= 337 or angle < 22:
            self.src_rect = pygame.Rect(0, 0, 16, 16)
        elif angle >= 22 and angle < 67:
            self.src_rect = pygame.Rect(16, 0, 16, 16)
        elif angle >= 67 and angle < 112:
            self.src_rect = pygame.Rect(32, 0, 16, 16)
        elif angle >= 112 and angle < 157:
            self.src_rect = pygame.Rect(48, 0, 16, 16)
        elif angle >= 157 and angle < 202:
            self.src_rect = pygame.Rect(64, 0, 16, 16)
        elif angle >= 202 and angle < 247:
            self.src_rect = pygame.Rect(80, 0, 16, 16)
        elif angle >= 247 and angle < 292:
            self.src_rect = pygame.Rect(96, 0, 16, 16)
        elif angle >= 292 and angle < 337:
            self.src_rect = pygame.Rect(112, 0, 16, 16)
        self.alive = 1
        

    def erase(self):
        display.blit(background, self.rect.topleft, self.rect)
        dirtyrects.append(pygame.Rect(self.rect))
        
    def draw(self):
        display.blit(self.surface, self.rect.topleft, self.src_rect)
        dirtyrects.append(self.rect)
        
    def move(self):
        self.position_x += (self.vel_x * timer.frame_duration)
        self.position_y += (self.vel_y * timer.frame_duration)
        self.rect.topleft = (self.position_x, self.position_y)
        self.colliderect.topleft = (self.rect.left + 4, self.rect.top + 4)
        if not screenrect.contains(self.rect):
            self.alive = 0
        if self.colliderect.collidelist(level.impassable_rects) != -1:
            self.alive = 0
            g_explosions.append(Explosion(self.rect.center, self.friendly))
        if self.friendly:
            for monster in g_monsters:
                if self.colliderect.colliderect(monster.colliderect):
                    self.alive = 0
                    g_explosions.append(Explosion(self.rect.center, self.friendly))
                    monster.take_damage(self.damage, 0)
        if not self.friendly:
            if self.colliderect.colliderect(player.colliderect):
                self.alive = 0
                g_explosions.append(Explosion(self.rect.center, self.friendly))
                player.take_damage(self.damage)
        return

    def think(self):
        if self.smoke_time > timer.current_time:
            return
        else:
            #g_decals.append(Bullet_Hole(self.rect.center))
            g_smokes.append(Smoke(self.rect.center))
            self.smoke_time = timer.current_time + self.smoke_interval
            return


class Flame:
    speed = 150.000
    damage = 5
    
    def __init__(self, position_x, position_y, vel_x, vel_y):
        self.position_x = position_x - 4
        self.position_y = position_y - 4
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.damage = Flame.damage
        self.surface = Img.flame
        self.rect = pygame.Rect(position_x, position_y, 8, 8)
        self.colliderect = pygame.Rect(self.rect.left + 1, self.rect.top + 1, 6, 6)
        self.alive = 1
        self.travel_duration = 750
        self.die_time = timer.current_time + self.travel_duration

    def erase(self):
        display.blit(background, self.rect.topleft, self.rect)
        dirtyrects.append(pygame.Rect(self.rect))
        
        
    def draw(self):
        display.blit(self.surface, self.rect.topleft)
        dirtyrects.append(self.rect)


    def move(self):
        self.position_x += (self.vel_x * timer.frame_duration)
        self.position_y += (self.vel_y * timer.frame_duration)
        self.rect.topleft = (self.position_x, self.position_y)
        self.colliderect.topleft = (self.rect.left + 1, self.rect.top + 1)
        if not screenrect.contains(self.rect):
            self.alive = 0
        if self.colliderect.collidelist(level.impassable_rects) != -1:
            self.alive = 0
            self.check_for_fire(self.rect)
        for monster in g_monsters:
            if self.colliderect.colliderect(monster.colliderect):
                self.alive = 0
                monster.take_damage(self.damage, 0)
                self.check_for_fire(self.rect)
        return

    def think(self):
        if self.die_time > timer.current_time:
            return
        else:
            self.check_for_fire(self.rect)
            self.alive = 0

    def check_for_fire(self, rect):
        for fire in g_fires:
            if rect.colliderect(fire.rect):
                fire.time_to_die = timer.current_time + 3000
                return
        g_fires.append(Fire(rect.center))
        return
        
    
class Grenade:
    speed = 200.000
    
    
    def __init__(self, origin_x, origin_y, target_x, target_y):
        self.position_x = origin_x - 8 
        self.position_y = origin_y - 8
        self.target_x = target_x
        self.target_y = target_y
        self.surface = Img.grenade
        self.src_rect = pygame.Rect((0, 0, 16, 16))
        self.rect = pygame.Rect(self.position_x, self.position_y, 16, 16)
        self.frame_time = 0
        self.frame_interval = 250
        self.vel_x = (target_x - origin_x) / 2
        if self.vel_x > 200:
            self.vel_x = 200
        self.vel_y = (target_y - origin_y) / 2
        if self.vel_y > 200:
            self.vel_y = 200
        self.alive = 1
        

    def erase(self):
        display.blit(background, self.rect.topleft, self.rect)
        dirtyrects.append(pygame.Rect(self.rect))
        
        
    def draw(self):
        display.blit(self.surface, self.rect.topleft, self.src_rect)
        dirtyrects.append(self.rect)


    def move(self):
        self.position_x += (self.vel_x * timer.frame_duration)
        self.position_y += (self.vel_y * timer.frame_duration)
        self.rect.topleft = (self.position_x, self.position_y)
        if not screenrect.contains(self.rect):
            self.alive = 0

    def think(self):
        if self.frame_time > timer.current_time:
            return
        else:
            self.src_rect.left += 16
            if self.src_rect.left > self.surface.get_width():
                self.alive = 0
                g_explosions.append(Explosion(self.rect.center, 1))
            else:
                self.frame_time = timer.current_time + self.frame_interval
            return

class Bomb:
    def __init__(self, position_x, position_y):
        self.position_x = position_x - 8 
        self.position_y = position_y - 8
        self.damage = 190
        self.surface = Img.bomb
        self.src_rect = pygame.Rect((0, 0, 16, 16))
        self.rect = pygame.Rect(position_x, position_y, 16, 16)
        self.frame_time = 0
        self.frame_interval = 750
        self.alive = 1


    def erase(self):
        display.blit(background, self.rect.topleft, self.rect)
        dirtyrects.append(pygame.Rect(self.rect))
        
        
    def draw(self):
        display.blit(self.surface, self.rect.topleft, self.src_rect)
        dirtyrects.append(self.rect)


    def think(self):
        if self.frame_time > timer.current_time:
            return
        else:
            self.src_rect.left += 16
            if self.src_rect.left >= self.surface.get_width():
                self.alive = 0
                self.blast()
            else:
                self.frame_time = timer.current_time + self.frame_interval
            return

    def blast(self):
        if sound:
            play_sound(Snd.bombblast, 0.5)
        # special effects
        tempsurf = pygame.Surface((640, 480))
        tempdisplay = pygame.Surface((640, 480))
        tempdisplay.blit(display, (0, 0))
        tempdisplay.blit(background, self.rect.topleft, self.rect)
        tempsurf.fill((255, 255, 255))
        for myalpha in range(254, 0, -16):
            tempsurf.set_alpha(myalpha)
            display.blit(tempdisplay, (0, 0))
            display.blit(tempsurf, (0, 0))
            pygame.display.update()
        display.blit(tempdisplay, (0, 0))
        pygame.display.update()

        for monster in g_monsters:
            if can_see(self, monster):
                monster.take_damage(self.damage, 1)
            if can_see(self, player):
                player.take_damage(self.damage / 2)
        

class Decal_Point:
    def __init__(self, position_xy):
        self.rect = pygame.Rect((position_xy[0], position_xy[1], 1, 1))
        self.colour_number = 10
        self.fade_time = 0
        self.fade_duration = 250
        self.current_colour = [255, 255, 0]            # overridden by actual class
        self.step = [0, 0, 0]
        

    def calculate_step(self):
        final_colour = background.get_at(self.rect.topleft)
        for index in range(0,3):
            self.step[index] = ((final_colour[index] - self.current_colour[index]) / 10)
    

    def think(self):
        # decals fade to the background colour
        if self.fade_time > timer.current_time:
            return
        else:
            if self.colour_number > 1:
                for index in range(0,3):
                    self.current_colour[index] = self.current_colour[index] + self.step[index]
                self.colour_number -= 1
                self.fade_time = timer.current_time + self.fade_duration
            else:
                self.current_colour = background.get_at(self.rect.topleft)
            return

    def draw(self):
        display.fill(self.current_colour, self.rect)
        dirtyrects.append(self.rect)

        
class Bullet_Hole(Decal_Point):
    def __init__(self, position_xy):
        Decal_Point.__init__(self, position_xy)
        self.current_colour = [255, 255, 0]
        self.calculate_step()
            
        
class Blood(Decal_Point):
    def __init__(self, position_xy):
        Decal_Point.__init__(self, position_xy)
        self.current_colour = [255, 0, 0]
        self.calculate_step()
        self.fade_duration = 500


class Fire:
    def __init__(self, center_xy):
        self.rect = pygame.Rect((0, 0, 16, 16))
        self.rect.center = center_xy
        self.src_rect = pygame.Rect((0, 0, 16, 16))
        self.surface = Img.fire
        self.frame_time = 0
        self.frame_duration = 250
        self.hurt_time = 0
        self.hurt_interval = 250
        self.time_to_die = timer.current_time + 3000
        self.alive = 1
        self.damage = 5

    def think(self):
        if self.time_to_die <= timer.current_time:
            self.alive = 0
            return
        if self.frame_time <= timer.current_time:
            self.frame_time = timer.current_time + self.frame_duration
            if self.src_rect.left == 0:
                self.src_rect.left = 16
            else:
                self.src_rect.left = 0
        if self.hurt_time <= timer.current_time:
            self.hurt_time = timer.current_time + self.hurt_interval
            for monster in g_monsters:
                if self.rect.colliderect(monster.rect):
                    monster.take_damage(self.damage, 0)
            if self.rect.colliderect(player.rect):
                player.take_damage(self.damage)

    def draw(self):
        display.blit(self.surface, self.rect.topleft, self.src_rect)
        dirtyrects.append(self.rect)


    def erase(self):
        display.blit(background, self.rect.topleft, self.rect)
        dirtyrects.append(self.rect)
        
            
class Smoke:
    def __init__(self, center_xy):
        self.rect = pygame.Rect((0, 0, 8, 8))
        self.rect.center = center_xy
        self.fade_steps = (255, 224, 192, 160, 128, 96, 64, 32, 0)
        self.surface = Img.smoke
        self.fade_number = 0
        self.fade_time = 0
        self.fade_duration = 250
        self.alpha = 255
        self.alive = 1
        
        
    def think(self):
        if self.fade_time > timer.current_time:
            return
        else:
            self.alpha = self.fade_steps[self.fade_number]
            self.fade_number += 1
            if self.fade_number == 9:
                self.alive = 0
            self.fade_time = timer.current_time + self.fade_duration
            return

    
        
    def draw(self):
        Img.smoke.set_alpha(self.alpha, pygame.RLEACCEL)
        display.blit(self.surface, self.rect.topleft)
        dirtyrects.append(self.rect)


    def erase(self):
        display.blit(background, self.rect.topleft, self.rect)
        dirtyrects.append(self.rect)
        

class Explosion:
    def __init__(self, center_xy, friendly):
        self.rect = pygame.Rect((0, 0, 64, 64))
        self.colliderect = pygame.Rect((0, 0, 48, 48))
        self.rect.center = center_xy
        self.colliderect.center = center_xy
        self.x_overlap = 0
        self.y_overlap = 0
        if self.rect.left < 0:
            self.x_overlap = abs(self.rect.left)
        if self.rect.top < 0:
            self.y_overlap = abs(self.rect.top)
        self.frame_offset = -64
        self.surface = Img.explosion
        self.frame_time = 0
        self.frame_duration = 60
        self.alive = 1
        self.friendly = friendly
        self.damage = 300
        self.rect = self.rect.clip(screenrect)
        if sound:
            play_sound(Snd.explosion, 0.3)
            
    def think(self):
        if self.frame_time > timer.current_time:
            return
        else:
            if self.friendly:
                for monster in g_monsters:
                    if self.colliderect.colliderect(monster.colliderect):
                        monster.take_damage(self.damage * timer.frame_duration, 0)
            if self.rect.colliderect(player.colliderect):
                player.take_damage(self.damage * timer.frame_duration)
            self.frame_offset += 64
            if self.frame_offset > 1024:
                self.alive = 0
            self.frame_time = timer.current_time + self.frame_duration
            return

        
    def draw(self):
        display.blit(self.surface, self.rect.topleft,
                     (self.frame_offset + self.x_overlap, self.y_overlap,
                      64 - self.x_overlap, 64 - self.y_overlap))
        dirtyrects.append(self.rect)


    def erase(self):
        display.blit(background, self.rect.topleft, self.rect)
        

class Monster:
    def __init__(self, rect, possession):
        self.rect = rect
        self.srcrect = pygame.Rect((0, 0, 16, 16))
        self.possession = possession
        self.alive = 1
        self.frame_time = 0
        self.think_time = 0
        self.position_x = self.rect.left * 1.000
        self.position_y = self.rect.top * 1.000
        self.direction = 0
        self.dying = 0
        self.dying_interval = 250
        self.dying_time = 0
        self.immune_from_explosives = 0
        if sound:
            self.dying_sound = Snd.hunterdeath

    
    def draw(self):
        display.blit(self.surface, self.rect.topleft, self.srcrect)
        dirtyrects.append(self.rect)
        return


    def erase(self):
        display.blit(background, self.rect.topleft, self.rect)
        dirtyrects.append(pygame.Rect(self.rect))
        return


    def take_damage(self, damage, explosive):
        if explosive:
            if self.immune_from_explosives:
                return
        if not self.dying:
            self.health -= damage
            if self.health < 1:
                self.dying = 1
                self.surface = self.dying_surface
                if sound:
                    play_sound(self.dying_sound, 1.0)
        return

        
    def walk(self):
        if not self.dying:
            # calculate the new position
            delta_x = (math.cos(math.pi * self.direction / 180)) * self.speed * timer.frame_duration
            delta_y = (math.sin(math.pi * self.direction / 180)) * self.speed * timer.frame_duration
            new_position_x = self.position_x + delta_x
            new_position_y = self.position_y + delta_y
            # test the new position for collisions:
            test_rect = pygame.Rect((new_position_x, new_position_y, 16, 16))
            test_colliderect = pygame.Rect((test_rect.left + 1, test_rect.top + 1, 14, 14))
            if test_colliderect.collidelist(level.impassable_rects) != -1:
                # We hit a wall; turn 90 degrees and continue
                turn = whrandom.choice((90, -90))
                self.direction += turn
                if self.direction > 360:
                    self.direction -= 360
                elif self.direction < 0:
                    self.direction += 360
                return
            for monster in g_monsters:
                if monster is not self:
                    # We hit a monster; turn 90 degrees and continue
                    if test_colliderect.colliderect(monster.colliderect):
                        turn = whrandom.choice((90, -90))
                        self.direction += turn
                        if self.direction > 360:
                            self.direction -= 360
                        elif self.direction < 0:
                            self.direction += 360
                        return
            if test_colliderect.colliderect(player.colliderect):
                # We ran into the player. Do melee attack if we have one
                if self.damage:
                    player.take_damage(self.damage * timer.frame_duration)
                return
            # no collisions, save the new position
            self.position_x = new_position_x
            self.position_y = new_position_y
            self.rect.topleft = (self.position_x, self.position_y)
            self.colliderect.left = self.rect.left + 1
            self.colliderect.top = self.rect.top + 1
        return  
        

    
class Shooter(Monster):
    think_interval = 750
    speed = 40
    health = 90
    damage = 0


    def __init__(self, rect, possession):
        Monster.__init__(self, rect, possession)
        self.surface = Img.shooter
        self.dying_surface = Img.shooter_dying
        self.colliderect = pygame.Rect(self.rect.left + 1, self.rect.top + 1, 14, 14)
        self.srcrect = pygame.Rect((0, 0, 16, 16))
        self.shoot_time = 0
        self.damage = Shooter.damage
        self.health = Shooter.health
        self.speed = Shooter.speed
    
        
        
    def think(self):
        if not self.dying:
            if timer.current_time >= self.think_time:
                self.think_time = timer.current_time + Hunter.think_interval
                if can_see(self, player):
                    self.direction = calculate_angle(self, player)
                    vel_x = (math.cos(math.pi * self.direction / 180)) * Bullet.speed 
                    vel_y = (math.sin(math.pi * self.direction / 180)) * Bullet.speed
                    bullets.append(Bullet(self.rect.center[0], self.rect.center[1], vel_x, vel_y, 0))
                    if sound:
                        play_sound(Snd.shotgun, 0.25)
                else:
                    self.direction = whrandom.randint(0, 360)
        self.animate()

            
    def animate(self):
        if not self.dying:
            # determine src_rect from direction
            # This can be improved, since the checks are sequential.
            angle = self.direction
            if angle < 0:
                angle += 360
            if angle >= 337 or angle < 22:
                self.srcrect.left = 0
            elif angle >= 22 and angle < 67:
                self.srcrect.left = 16
            elif angle >= 67 and angle < 112:
                self.srcrect.left = 32
            elif angle >= 112 and angle < 157:
                self.srcrect.left = 48
            elif angle >= 157 and angle < 202:
                self.srcrect.left = 64
            elif angle >= 202 and angle < 247:
                self.srcrect.left = 80
            elif angle >= 247 and angle < 292:
                self.srcrect.left = 96
            elif angle >= 292 and angle < 337:
                self.srcrect.left = 112
        else:
            if timer.current_time >= self.dying_time:
                self.dying_time = timer.current_time + self.dying_interval
                self.srcrect.left += 16
                if self.srcrect.left > self.surface.get_width():
                    self.alive = 0
                    if self.possession:
                        g_items.append(self.possession(self.rect.topleft))
        return
    



class Hunter(Monster):
    frame_duration = 200
    think_interval = 1000
    speed = 80
    health = 70
    damage = 40
    
    def __init__(self, rect, possession):
        Monster.__init__(self, rect, possession)
        self.surface = Img.hunter
        self.dying_surface = Img.hunter_dying
        self.colliderect = pygame.Rect(self.rect.left + 1, self.rect.top +1, 14, 14)
        self.damage = Hunter.damage
        self.health = Hunter.health
        self.speed = Hunter.speed
        self.dying_interval = 250
        self.dying_time = 0

        
    def think(self):
        if not self.dying:
            if timer.current_time >= self.frame_time:
                self.frame_time = timer.current_time + Hunter.frame_duration
            if timer.current_time >= self.think_time:
                self.think_time = timer.current_time + Hunter.think_interval
                if can_see(self, player):
                    self.direction = calculate_angle(self, player)
                else:
                    self.direction = whrandom.randint(0, 360)
        self.animate()

            
    def animate(self):
        if not self.dying:
            self.srcrect.left += 16
            if self.srcrect.left == 32:
                self.srcrect.left = 0
        else:
            if timer.current_time >= self.dying_time:
                self.dying_time = timer.current_time + self.dying_interval
                self.srcrect.left += 16
                if self.srcrect.left > self.surface.get_width():
                    self.alive = 0
                    if self.possession:
                        g_items.append(self.possession(self.rect.topleft))
        return




    


class Gunner(Monster):
    think_interval = 200
    speed = 25
    health = 100
    damage = 0

    def __init__(self, rect, possession):
        Monster.__init__(self, rect, possession)
        self.surface = Img.gunner
        self.dying_surface = Img.gunner_dying
        self.colliderect = pygame.Rect(self.rect.left + 1, self.rect.top + 1, 14, 14)
        self.srcrect = pygame.Rect((0, 0, 16, 16))
        self.shoot_time = 0
        self.damage = Gunner.damage
        self.health = Gunner.health
        self.speed = Gunner.speed
        
    def think(self):
        if not self.dying:
            if timer.current_time >= self.think_time:
                self.think_time = timer.current_time + Gunner.think_interval
                if can_see(self, player):
                    self.direction = calculate_angle(self, player)
                    angle = self.direction + whrandom.randint(-5, 5)
                    vel_x = (math.cos(math.pi * angle / 180)) * Bullet.speed 
                    vel_y = (math.sin(math.pi * angle / 180)) * Bullet.speed
                    bullets.append(Bullet(self.rect.center[0], self.rect.center[1], vel_x, vel_y, 0))
                    if sound:
                        play_sound(Snd.machinegun, 0.25)
                else:
                    self.direction = whrandom.randint(0, 360)
        self.animate()

            
    def animate(self):
        if not self.dying:
            # determine src_rect from direction
            # This can be improved, since the checks are sequential.
            angle = self.direction
            if angle < 0:
                angle += 360
            if angle >= 337 or angle < 22:
                self.srcrect.left = 0
            elif angle >= 22 and angle < 67:
                self.srcrect.left = 16
            elif angle >= 67 and angle < 112:
                self.srcrect.left = 32
            elif angle >= 112 and angle < 157:
                self.srcrect.left = 48
            elif angle >= 157 and angle < 202:
                self.srcrect.left = 64
            elif angle >= 202 and angle < 247:
                self.srcrect.left = 80
            elif angle >= 247 and angle < 292:
                self.srcrect.left = 96
            elif angle >= 292 and angle < 337:
                self.srcrect.left = 112
        else:
            if timer.current_time >= self.dying_time:
                self.dying_time = timer.current_time + self.dying_interval
                self.srcrect.left += 16
                if self.srcrect.left > self.surface.get_width():
                    self.alive = 0
                    if self.possession:
                        g_items.append(self.possession(self.rect.topleft))
        return
    

class Spider(Monster):
    speed = 40
    health = 80
    damage = 0

    def __init__(self, rect, possession):
        Monster.__init__(self, rect, possession)
        self.surface = Img.spider
        self.dying_surface = Img.spider_dying
        self.colliderect = pygame.Rect(self.rect.left + 1, self.rect.top + 1, 14, 14)
        self.srcrect = pygame.Rect((0, 0, 16, 16))
        self.turn_time = 0
        self.turn_interval = 500
        self.shoot_time = 0
        self.shoot_interval = 1000
        self.state = 0               # 0 = visible
                                     # 1 = fading
                                     # 2 = invisible
                                     # 3 = unfading
        self.frame_time = 0
        self.frame_interval = 250
        self.frame_number = 0
        self.fade_time = 0
        self.fade_interval = 100
        self.alpha = 255
        self.damage = Spider.damage
        self.health = Spider.health
        self.speed = Spider.speed
 
        

    def think(self):
        # what will the spider do this frame?
        if not self.dying:
            if self.state == 1:
                if self.fade_time <= timer.current_time:
                    self.fade_time = timer.current_time + self.fade_interval
                    self.alpha -= 32
                    if self.alpha <= 0:
                        self.state = 2
                        self.alpha = 0
            if self.state == 3:
                if self.fade_time <= timer.current_time:
                    self.fade_time = timer.current_time + self.fade_interval
                    self.alpha += 32
                    if self.alpha >= 255:
                        self.state = 0
                        self.alpha = 255
            if self.frame_time <= timer.current_time:
                self.frame_time = timer.current_time + self.frame_interval
                if self.frame_number == 1:
                    self.frame_number = 0
                else:
                    self.frame_number = 1
            if self.turn_time <= timer.current_time:
                self.turn_time = timer.current_time + self.turn_interval
                if can_see(self, player):
                    self.direction = calculate_angle(self, player)
                    if self.state == 2:
                        self.state = 3
                else:
                    self.direction = whrandom.randint(0, 360)
                    if self.state == 0:
                        self.state = 1
            if self.shoot_time <= timer.current_time and self.state == 0:
                self.shoot_time = timer.current_time + self.shoot_interval
                angle = calculate_angle(self, player)
                angle += whrandom.randint(-15, 15)
                delta_y = (math.sin(math.pi * angle / 180))
                delta_x = (math.cos(math.pi * angle / 180))
                laserbeams.append(Laserbeam(self.rect.center[0], self.rect.center[1], delta_x, delta_y, 0))
                if sound:
                    play_sound(Snd.laser, 1.0)
        self.animate()
        return


    def draw(self):
        Img.spider.set_alpha(self.alpha, pygame.RLEACCEL)
        display.blit(self.surface, self.rect.topleft, self.srcrect)
        dirtyrects.append(self.rect)
        return
        

    def animate(self):
        # choose frame based on time and direction
        if not self.dying:
            # determine src_rect from direction
            # This can be improved, since the checks are sequential.
            angle = self.direction
            if angle < 0:
                angle += 360
            if angle >= 315 or angle < 45:
                self.srcrect.left = 0
            elif angle >= 45 and angle < 135:
                self.srcrect.left = 32
            elif angle >= 135 and angle < 225:
                self.srcrect.left = 64
            elif angle >= 225 and angle < 315:
                self.srcrect.left = 96
            if self.frame_number == 1:
                self.srcrect.left += 16
        else:
            self.alpha = 255
            if timer.current_time >= self.dying_time:
                self.dying_time = timer.current_time + self.dying_interval
                self.srcrect.left += 16
                if self.srcrect.left > self.surface.get_width():
                    self.alive = 0
                    if self.possession:
                        g_items.append(self.possession(self.rect.topleft))
        return

    
class Robot(Monster):
    speed = 30
    health = 240
    damage = 0

    def __init__(self, rect, possession):
        Monster.__init__(self, rect, possession)
        self.surface = Img.robot
        self.dying_surface = Img.robot_dying
        self.colliderect = pygame.Rect(self.rect.left + 1, self.rect.top + 1, 14, 14)
        self.srcrect = pygame.Rect((0, 0, 16, 16))
        self.turn_time = 0
        self.turn_interval = 500
        self.shoot_time = 0
        self.shoot_interval = 1000
        self.frame_time = 0
        self.frame_interval = 250
        self.frame_number = 0
        self.damage = Robot.damage
        self.health = Robot.health
        self.speed = Robot.speed
        self.immune_from_explosives = 1
 
        

    def think(self):
        # what will the robot do this frame?
        if not self.dying:
            if self.frame_time <= timer.current_time:
                self.frame_time = timer.current_time + self.frame_interval
                if self.frame_number == 1:
                    self.frame_number = 0
                else:
                    self.frame_number = 1
            if self.turn_time <= timer.current_time:
                self.turn_time = timer.current_time + self.turn_interval
                if can_see(self, player):
                    self.direction = calculate_angle(self, player)
                else:
                    self.direction = whrandom.randint(0, 360)
            if self.shoot_time <= timer.current_time:
                self.shoot_time = timer.current_time + self.shoot_interval
                if can_see(self, player):
                    angle = calculate_angle(self, player)
                    rocketangle = angle + whrandom.randint(-30, 30)
                    vel_x = (math.cos(math.pi * rocketangle / 180)) * Rocket.speed 
                    vel_y = (math.sin(math.pi * rocketangle / 180)) * Rocket.speed
                    g_rockets.append(Rocket(self.rect.center[0], self.rect.center[1], vel_x, vel_y, rocketangle, 0))
                    rocketangle = angle + whrandom.randint(-30, 30)
                    vel_x = (math.cos(math.pi * rocketangle / 180)) * Rocket.speed 
                    vel_y = (math.sin(math.pi * rocketangle / 180)) * Rocket.speed
                    g_rockets.append(Rocket(self.rect.center[0], self.rect.center[1], vel_x, vel_y, rocketangle, 0))
                    if sound:
                        play_sound(Snd.rocket, 0.25)
        self.animate()
        return
        

    

    def animate(self):
        # choose frame based on time and direction
        if not self.dying:
            # determine src_rect from direction
            # This can be improved, since the checks are sequential.
            angle = self.direction
            if angle < 0:
                angle += 360
            if angle >= 315 or angle < 45:
                self.srcrect.left = 0
            elif angle >= 45 and angle < 135:
                self.srcrect.left = 32
            elif angle >= 135 and angle < 225:
                self.srcrect.left = 64
            elif angle >= 225 and angle < 315:
                self.srcrect.left = 96
            if self.frame_number == 1:
                self.srcrect.left += 16
        else:
            if timer.current_time >= self.dying_time:
                self.dying_time = timer.current_time + self.dying_interval
                self.srcrect.left += 16
                if self.srcrect.left > self.surface.get_width():
                    self.alive = 0
                    if self.possession:
                        g_items.append(self.possession(self.rect.topleft))
        return


class Gun:
    def __init__(self):
        self.rect = pygame.Rect((0, 0, 2, 2))
    
    
    

class Boss(Monster):
    def __init__(self, rect, possession):
        Monster.__init__(self, rect, possession)
        self.surface = Img.boss
        self.dying_surface = Img.boss_dying
        self.colliderect = pygame.Rect(self.rect.left + 12, self.rect.top, 36, 64)
        self.srcrect = pygame.Rect((0, 0, 64, 64))
        self.turn_time = 0
        self.turn_interval = 500
        self.guns_shoot_time = 0
        self.guns_shoot_interval = 125
        self.rockets_shoot_time = 0
        self.rockets_shoot_interval = 3000
        self.frame_time = 0
        self.frame_interval = 250
        self.frame_number = 0
        self.damage = 20
        self.health = 800
        self.speed = 20
        self.gun1 = Gun()
        self.gun2 = Gun()
        self.death_count = 32
        self.immune_from_explosives = 1
        
        
    def animate(self):
        # choose frame based on time and direction
        if not self.dying:
            # determine src_rect from direction
            # This can be improved, since the checks are sequential.
            angle = self.direction
            if angle < 0:
                angle += 360
            if angle >= 315 or angle < 45:
                self.srcrect.left = 0
                self.gun1.rect.left = self.rect.left + 45
                self.gun1.rect.top = self.rect.top + 28
                self.gun2.rect.left = self.rect.left + 52
                self.gun2.rect.top = self.rect.top + 27
            elif angle >= 45 and angle < 135:
                self.srcrect.left = 256
                self.gun1.rect.left = self.rect.left + 7
                self.gun1.rect.top = self.rect.top + 24
                self.gun2.rect.left = self.rect.left + 52
                self.gun2.rect.top = self.rect.top + 25
            elif angle >= 135 and angle < 225:
                self.srcrect.left = 512
                self.gun1.rect.left = self.rect.left + 17
                self.gun1.rect.top = self.rect.top + 28
                self.gun2.rect.left = self.rect.left + 12
                self.gun2.rect.top = self.rect.top + 27
            elif angle >= 225 and angle < 315:
                self.srcrect.left = 768
                self.gun1.rect.left = self.rect.left + 7
                self.gun1.rect.top = self.rect.top + 24
                self.gun2.rect.left = self.rect.left + 52
                self.gun2.rect.top = self.rect.top + 25
            if self.frame_number > 0:
                self.srcrect.left += 64 * self.frame_number
        else:
            if timer.current_time >= self.dying_time:
                self.dying_time = timer.current_time + self.dying_interval
                if self.death_count > 0:
                    self.death_count -= 1
                    myx = whrandom.randint(self.rect.left, self.rect.right)
                    myy = whrandom.randint(self.rect.top, self.rect.bottom)
                    g_explosions.append(Explosion((myx, myy), 1))
                else:
                    self.alive = 0
                    end_game_victory()
        return
    
    def think(self):
        # what will the robot do this frame?
        if not self.dying:
            if self.frame_time <= timer.current_time:
                self.frame_time = timer.current_time + self.frame_interval
                if self.frame_number == 3:
                    self.frame_number = 0
                else:
                    self.frame_number += 1
            if self.turn_time <= timer.current_time:
                self.turn_time = timer.current_time + self.turn_interval
                self.direction = calculate_angle(self, player)
               
            if self.guns_shoot_time <= timer.current_time:
                self.guns_shoot_time = timer.current_time + self.guns_shoot_interval
                angle1 = calculate_angle(self.gun1, player)
                angle2 = calculate_angle(self.gun2, player)
                vel_x = (math.cos(math.pi * angle1 / 180)) * Bullet.speed 
                vel_y = (math.sin(math.pi * angle1 / 180)) * Bullet.speed
                bullets.append(Bullet(self.gun1.rect.center[0], self.gun1.rect.center[1], vel_x, vel_y, 0))
                vel_x = (math.cos(math.pi * angle2 / 180)) * Bullet.speed 
                vel_y = (math.sin(math.pi * angle2 / 180)) * Bullet.speed
                bullets.append(Bullet(self.gun2.rect.center[0], self.gun2.rect.center[1], vel_x, vel_y, 0))
                if sound:
                    play_sound(Snd.machinegun, 0.25)
            if self.rockets_shoot_time <= timer.current_time:
                self.rockets_shoot_time = timer.current_time + self.rockets_shoot_interval
                angle = calculate_angle(self, player)
                rocketangle = angle
                vel_x = (math.cos(math.pi * rocketangle / 180)) * Rocket.speed * 1
                vel_y = (math.sin(math.pi * rocketangle / 180)) * Rocket.speed * 1
                g_rockets.append(Rocket(self.rect.center[0], self.rect.center[1], vel_x, vel_y, rocketangle, 0))
                rocketangle = angle + whrandom.randint(-30, 30)
                vel_x = (math.cos(math.pi * rocketangle / 180)) * Rocket.speed * 1
                vel_y = (math.sin(math.pi * rocketangle / 180)) * Rocket.speed * 1
                g_rockets.append(Rocket(self.rect.center[0], self.rect.center[1], vel_x, vel_y, rocketangle, 0))
                rocketangle = angle - 50
                vel_x = (math.cos(math.pi * rocketangle / 180)) * Rocket.speed * 1
                vel_y = (math.sin(math.pi * rocketangle / 180)) * Rocket.speed * 1
                g_rockets.append(Rocket(self.rect.center[0], self.rect.center[1], vel_x, vel_y, rocketangle, 0))
                rocketangle = angle + 50
                vel_x = (math.cos(math.pi * rocketangle / 180)) * Rocket.speed * 1
                vel_y = (math.sin(math.pi * rocketangle / 180)) * Rocket.speed * 1
                g_rockets.append(Rocket(self.rect.center[0], self.rect.center[1], vel_x, vel_y, rocketangle, 0))
                rocketangle = angle - 80
                vel_x = (math.cos(math.pi * rocketangle / 180)) * Rocket.speed * 1 
                vel_y = (math.sin(math.pi * rocketangle / 180)) * Rocket.speed * 1
                g_rockets.append(Rocket(self.rect.center[0], self.rect.center[1], vel_x, vel_y, rocketangle, 0))
                rocketangle = angle + 80
                vel_x = (math.cos(math.pi * rocketangle / 180)) * Rocket.speed * 1 
                vel_y = (math.sin(math.pi * rocketangle / 180)) * Rocket.speed * 1
                g_rockets.append(Rocket(self.rect.center[0], self.rect.center[1], vel_x, vel_y, rocketangle, 0))
                if sound:
                    play_sound(Snd.rocket, 0.25)
        self.animate()
        return




    def walk(self):
        if not self.dying:
            # calculate the new position
            delta_x = (math.cos(math.pi * self.direction / 180)) * self.speed * timer.frame_duration
            delta_y = (math.sin(math.pi * self.direction / 180)) * self.speed * timer.frame_duration
            new_position_x = self.position_x + delta_x
            new_position_y = self.position_y + delta_y
            # test the new position for collisions:
            test_rect = pygame.Rect((new_position_x, new_position_y, 64, 64))
            test_colliderect = pygame.Rect((test_rect.left + 4, test_rect.top + 4, 56, 56))
            if test_colliderect.collidelist(level.impassable_rects) != -1:
                # We hit a wall; turn 90 degrees and continue
                turn = whrandom.choice((90, -90))
                self.direction += turn
                if self.direction > 360:
                    self.direction -= 360
                elif self.direction < 0:
                    self.direction += 360
                return
            if test_colliderect.colliderect(player.colliderect):
                # We ran into the player. Do melee attack if we have one
                if self.damage:
                    player.take_damage(self.damage * timer.frame_duration)
                return
            # no collisions, save the new position
            self.position_x = new_position_x
            self.position_y = new_position_y
            self.rect.topleft = (self.position_x, self.position_y)
            self.colliderect.left = self.rect.left + 1
            self.colliderect.top = self.rect.top + 1
        return  



    
class Item:
    def __init__(self, location):
        self.rect = pygame.Rect((location, (16, 16)))
        self.alive = 1

    def draw(self):
        display.blit(self.surface, self.rect.topleft)
        dirtyrects.append(self.rect)
        return

    def erase(self):
        display.blit(background, self.rect.topleft, self.rect)
        dirtyrects.append(self.rect)
        return
    


class BulletAmmo(Item):
    def __init__(self, location):
        Item.__init__(self, location)
        self.surface = Img.bulletammo

    def pickup(self):
        weapon = player.weapons[1]
        if self.alive:
            if sound:
                play_sound(Snd.pickup, 0.5)
            self.alive = 0
            weapon.ammo += 40
            if weapon.ammo > 200:
                weapon.ammo = 200
            statusbar.draw(0, 1, 0)
        return
    


class LaserAmmo(Item):
    def __init__(self, location):
        Item.__init__(self, location)
        self.surface = Img.laserammo

    def pickup(self):
        weapon = player.weapons[2]
        if self.alive:
            if sound:
                play_sound(Snd.pickup, 0.5) 
            self.alive = 0
            weapon.ammo += 5
            if weapon.ammo > 25:
                weapon.ammo = 25
            statusbar.draw(0, 1, 0)
        return


class FlamerAmmo(Item):
    def __init__(self, location):
        Item.__init__(self, location)
        self.surface = Img.flamerammo

    def pickup(self):
        weapon = player.weapons[4]
        if self.alive:
            if sound:
                play_sound(Snd.pickup, 0.5)
            self.alive = 0
            weapon.ammo += 25
            if weapon.ammo > 100:
                weapon.ammo = 100
            statusbar.draw(0, 1, 0)
        return
    


class GrenadeAmmo(Item):
    def __init__(self, location):
        Item.__init__(self, location)
        self.surface = Img.grenadeammo

    def pickup(self):
        weapon = player.weapons[5]
        if self.alive:
            if sound:
                play_sound(Snd.pickup, 0.5)
            self.alive = 0
            weapon.ammo += 5
            if weapon.ammo > 25:
                weapon.ammo = 25
            statusbar.draw(0, 1, 0)
        return
    


class BombAmmo(Item):
    def __init__(self, location):
        Item.__init__(self, location)
        self.surface = Img.bombammo

    def pickup(self):
        weapon = player.weapons[6]
        if self.alive:
            if sound:
                play_sound(Snd.pickup, 0.5)
            self.alive = 0
            weapon.ammo += 1
            if weapon.ammo > 1:
                weapon.ammo = 1
            statusbar.draw(0, 1, 0)
        return
    pass


class RocketAmmo(Item):
    def __init__(self, location):
        Item.__init__(self, location)
        self.surface = Img.rocketammo

    def pickup(self):
        rl = player.weapons[3]
        if self.alive:
            if sound:
                play_sound(Snd.pickup, 0.5)
            self.alive = 0
            rl.ammo += 5
            if rl.ammo > 25:
                rl.ammo = 25
            statusbar.draw(0, 1, 0)
        return


class HealthKit(Item):
    def __init__(self, location):
        Item.__init__(self, location)
        self.surface = Img.healthkit

    def pickup(self):
        if self.alive:
            if sound:
                play_sound(Snd.pickup_health, 1.0)
            self.alive = 0
            player.health += 25
            if player.health > 100:
                player.health = 100
            statusbar.draw(0, 0, 1)
        return

class Key(Item):
    def __init__(self, location):
        Item.__init__(self, location)
        self.surface = Img.key

    def pickup(self):
        if self.alive:
            self.alive = 0
            for exit_gate in level.exit_gates:
                exit_gate.up()
                exit_gate.draw()
                dirtyrects.append(exit_gate.rect)
        







        
class Level:
    def __init__(self, number):
        self.number = number
        self.tiles = []
        self.entrance_gates = []
        self.exit_gates = []
        self.spawntiles = []
        self.impassable_rects = []
        self.los_blocking_rects = []
        self.start_tile = None
        self.entry_tile = None
        self.exit_tile = None
        self.monster_queue = {}
        self.spawn_time = 0
        self.spawn_interval = 5000
        self.spawn_interval_number = -1
        
        
    def load_map_file(self, number):
        # establish the platform-independent filename
        filename = os.path.join('levels', str(number) + '.lvl')
        try:
            map_file = open(filename, 'r')
        except IOError:
            # raise SystemExit, "Fatal Error: Filename %s not found. Could not load map" % filename
            hld = 8

        section = None
        rownum = 0
        while 1:
            # per line
            line = map_file.readline()
            if line == '':
                break
            else:
                line = line.strip()
            if line == '' or line.startswith('#'):
                continue
            if line.startswith(':Map'):
                section = 'map'
                continue
            elif line.startswith(':Monsters'):
                section = 'monsters'
                continue
            if section == 'map':
                # parse map line
                if len(line) != 40:         # 40 columns plus an \n
                   # raise SystemExit, "Fatal Error: Map row number %s has illegal length: %s." % (str(rownum), str(len(line)))
                   hld = 10
                charnum = 0
                for char in line:
                    if char == "X":
                        self.tiles.append(Block(charnum, rownum))
                    elif char == ".":
                        self.tiles.append(Blank(charnum,rownum))
                    elif char == "I":
                        this_tile = Entrance(charnum, rownum)
                        self.tiles.append(this_tile)
                        self.entry_tile = this_tile
                    elif char == "O":
                        this_tile = Exit(charnum, rownum)
                        self.tiles.append(this_tile)
                        self.exit_tile = this_tile
                    elif char == "G":
                        this_tile = Entrance_gate(charnum, rownum)
                        self.tiles.append(this_tile)
                        self.entrance_gates.append(this_tile)
                    elif char == "g":
                        this_tile = Exit_gate(charnum, rownum)
                        self.tiles.append(this_tile)
                        self.exit_gates.append(this_tile)
                    elif char == "S":
                        this_tile = Blank(charnum, rownum)
                        self.tiles.append(this_tile)
                        self.start_tile = this_tile
                    elif char == "M":
                        this_tile = Blank(charnum, rownum)
                        self.tiles.append(this_tile)
                        self.spawntiles.append(this_tile)
                    else:
                     #   raise SystemExit, "Map read error - Unknown character: " + str(charnum)
                    # except RuntimeError:
        #raise SystemExit,  pygame.get_error()
                        hld = 11
                    charnum += 1
                rownum += 1
                    
            elif section == 'monsters':
                # parse monster line

                # turn entry into a list of monsters, free from crap
                monsters = line.split(',')
                monsters = [monster.strip() for monster in monsters]

                for monster in monsters:
                    # Do input checking

                    # Which 5-second interval?
                    try:
                        turn = int(monster[0:-2])
                    except ValueError:
                      #  raise SystemExit, "Map read error: Invalid turn number for monster %s. Must be 0+." % monster
                      hld = 10

                    # Store pointer to monster's class
                    type = monster[-2:-1]
                    if not type in 'shgarB-':
                       # raise SystemExit, "Map read error: Invalid monster type: %s." % type
                       hld = 10

                    if type == 's':
                        type = Shooter
                        image = Img.shooter
                    elif type == 'h':
                        type = Hunter
                        image = Img.hunter
                    elif type == 'g':
                        type = Gunner
                        image = Img.gunner
                    elif type == 'a':
                        type = Spider
                        image = Img.spider
                    elif type == 'r':
                        type = Robot
                        image = Img.robot
                    elif type == 'B':
                        type = Boss
                        image = Img.boss
                    
                    elif type == '-':
                        type = None
                        image = None
                    
                    
                    # What's he carrying? '-' means nothing.
                    possession = monster[-1:]
                    if not possession in 'blfgBr-k+':
                      #  raise SystemExit, "Map read error: Invalid monster possession type: %s." % possession
                       hld = 10

                    if possession == 'b':
                        possession = BulletAmmo
                        possession_image = Img.bulletammo
                    elif possession == 'l':
                        possession = LaserAmmo
                        possession_image = Img.laserammo
                    elif possession == 'f':
                        possession = FlamerAmmo
                        possession_image = Img.flamerammo
                    elif possession == 'g':
                        possession = GrenadeAmmo
                        possession_image = Img.grenadeammo
                    elif possession == 'B':
                        possession = BombAmmo
                        possession_image = Img.bombammo
                    elif possession == 'r':
                        possession = RocketAmmo
                        possession_image = Img.rocketammo
                    elif possession == '+':
                        possession = HealthKit
                        possession_image = Img.healthkit
                    elif possession == '-':
                        possession = None
                        possession_image = None
                    elif possession == 'k':
                        possession = Key
                        possession_image = Img.key

                    # load the monster into g_monsterqueue

                    if self.monster_queue.has_key(turn):
                        self.monster_queue[turn].append((type, image, possession, possession_image))
                    else:
                        self.monster_queue[turn] = [(type, image, possession, possession_image)]

        # Check for common mapmaking errors.
        
        if self.start_tile == None:
            # raise SystemExit, "Fatal Error: Map # %s load error: No player start position" % str(number)
            hld = 10
        if self.entry_tile == None:
            # raise SystemExit, "Fatal Error: Map # %s load error: No player entry position" % str(number)
            hld = 10
        if len(self.tiles) != 1160:
           # raise SystemExit, "Fatal Error: Wrong number of map tiles: %s (should be 1160)." % str(len(self.tiles))
            hld = 10
        return
        

    def calculate_impassable_rects(self):
        self.impassable_rects = []
        for tile in self.tiles:
            if tile.walkable == 0:
                self.impassable_rects.append(tile.rect)
        return


    def calculate_los_blocking_rects(self):
        self.los_blocking_rects = []
        for tile in self.tiles:
            if (tile.column > 0 and tile.column < 39 and tile.row > 0 and tile.row < 28):
                if tile.walkable == 0:
                    self.los_blocking_rects.append(tile.rect)
        return
                
    
    
    def draw_to_display(self):
        for tile in self.tiles:
            if tile.visible:
                tile.draw()


    def introduce(self):
        background.fill(BLACK)
        display.blit(background, (0, 0))
        if sound:
            play_sound(Snd.level_intro_music, 1.0, -1)
            
        # Display level number and wait 2.5 seconds
        font = pygame.font.Font(os.path.join('images', 'younffp_.ttf'), 24)
        level_intro_message = font.render('Level: ' + str(current_level_number), 1, (255, 255, 255))
        display.fill((0, 0, 216, 255), (272, 220, 96, 40))
        display.fill((0, 0, 128, 255), (276, 224, 88, 32))
        display.blit(level_intro_message, (280, 228))
        pygame.display.flip()
        if not DEBUG:
            pygame.time.delay(2500)

        # draw level, gates down
        
        self.draw_to_display()
        
        # If this is the last level, draw the boss
        
        if self.number == 10:
            hisrect = pygame.Rect((296, 64, 64, 64))
            display.blit(Img.boss, hisrect.topleft, (320, 0, 64, 64))
            g_monsters.append(Boss(hisrect, None))

        pygame.display.flip()
        if not DEBUG:
            pygame.time.delay(2500)

        # draw level, entrance gates up
        
        for entrance_gate in self.entrance_gates:
            entrance_gate.up()
            entrance_gate.draw()
            pygame.display.update(entrance_gate.rect)

        
        # draw player at the level's entry point, move and animate
        # him to the start point, then return.    
        player.move(self.entry_tile.rect.topleft)
        
        # set the player's state depending on his location relative
        # to the start point.
        
        if self.entry_tile.rect.left == self.start_tile.rect.left:
            player.vel_x = 0
            if self.entry_tile.rect.top > self.start_tile.rect.top:
                player.state = 1
                player.vel_y = -1
            else:
                player.state = 3
                player.vel_y = 1
        else:
            player.vel_y = 0
            if self.entry_tile.rect.left < self.start_tile.rect.left:
                player.state = 2
                player.vel_x = 1
            else:
                player.state = 4
                player.vel_x = -1

        # Get him to the start tile
        while player.rect.topleft != self.start_tile.rect.topleft:
            dirtyrects = []
            player.erase()
            dirtyrects.append(pygame.Rect(player.rect))
            player.walk()
            if player.animate_time <= timer.current_time:
                player.animate()
                player.animate_time = timer.current_time + player.animate_time_duration
            player.draw()
            dirtyrects.append(player.rect)
            pygame.display.update(dirtyrects)
            if not DEBUG:
                pygame.time.delay(25)
            timer.set_current_time()

            # check for quit
            if pygame.event.peek(pygame.QUIT):
                end_game_quit()
            keys = pygame.key.get_pressed()
            for key in keymap.KEY_ESC:
                if keys[key]:
                    end_game_quit()
            
        for entrance_gate in self.entrance_gates:
            entrance_gate.down()
            entrance_gate.draw()
            pygame.display.update(entrance_gate.rect)
        
        player.state = 0
        player.vel_x = 0
        player.vel_y = 0
        player.animate()
        player.erase()
        player.draw()
        statusbar.rampup()
        statusbar.draw(1, 1, 1)

        if sound:
            Snd.level_intro_music.fadeout(2000)
        
        
    def unload_map(self):
        self = None


    def check_to_spawn(self, current_time):
        if len(self.spawntiles) == 0:
            return
        if current_time < self.spawn_time:
            return
        self.spawn_interval_number += 1
        self.spawn_time = timer.current_time + self.spawn_interval
        try:
            monsters = self.monster_queue[self.spawn_interval_number]
            if sound:
                play_sound(Snd.spawngate, 1.0)
            for monster in monsters:
                g_spawngates.append(Spawngate(monster[0], monster[1], monster[2], monster[3]))
        except KeyError:
            return
        
        
        
class Tile:
    def __init__(self, column, row):
        self.rect = pygame.Rect(column * 16, row * 16, 16, 16)
        self.walkable = 0
        self.visible = 1
        self.column = column
        self.row = row
        
    def draw(self):
        display.blit(self.surface, self.rect.topleft)
        background.blit(self.surface, self.rect.topleft)

        
class Block(Tile):
    def __init__(self, column, row):
        Tile.__init__(self, column, row)
        self.surface = Img.block
        self.walkable = 0

        
class Blank(Tile):
    def __init__(self, column, row):
        Tile.__init__(self, column, row)
        self.walkable = 1
        self.surface = Img.blank


        
class Entrance(Tile):
    def __init__(self, column, row):
        Tile.__init__(self, column, row)
        self.surface = Img.blank
        self.walkable = 1


        
class Exit(Tile):
    def __init__(self, column, row):
        Tile.__init__(self, column, row)
        self.surface = Img.blank
        self.walkable = 1
        
        
class Gate(Tile):
    def __init__(self, column, row):
        Tile.__init__(self, column, row)
        self.surface = Img.gate
        self.walkable = 0


    def up(self):
        if sound:
            Snd.gate_up.stop()
            play_sound(Snd.gate_up, 1.0)
        self.walkable = 1
        self.surface = Img.blank
        level.calculate_impassable_rects()
        level.calculate_los_blocking_rects()
        


    def down(self):
        if sound:
            Snd.gate_down.stop()
            play_sound(Snd.gate_down, 0.75)
        self.walkable = 0
        self.surface = Img.gate
        level.calculate_impassable_rects()
        level.calculate_los_blocking_rects()
        

class Entrance_gate(Gate):
    pass


class Exit_gate(Gate):
    pass


class Spawngate:
    def __init__(self, monster_type, monster_image, monster_possession, monster_possession_image):
        self.monster_type = monster_type
        self.monster_possession = monster_possession
        self.monster_surface = monster_image
        self.monster_possession_surface = monster_possession_image
        self.surface = Img.spawngate
        self.rect = pygame.Rect((-1, -1, 16, 16))
        self.srcrect = pygame.Rect((0, 0, 16, 16))
        self.frame_duration = 100
        self.frame_time = 0
        self.alive = 1

        # find a location for the spawngate

        while 1:
            self.rect.topleft = whrandom.choice(level.spawntiles).rect.topleft
            good_position = 1
            if self.rect.colliderect(player.rect):
                good_position = 0
                continue
            for monster in g_monsters:
                if self.rect.colliderect(monster.rect):
                    good_position = 0
            for spawngate in g_spawngates:
                if spawngate is not self:
                    if self.rect.colliderect(spawngate.rect):
                        good_position = 0
            if good_position:
                break
            else:
                continue
        return


    def draw(self):
        if self.srcrect.left > 127:
            if self.monster_type != None:
                display.blit(self.monster_surface, self.rect.topleft, (0, 0, 16, 16))
            elif self.monster_possession != None:
                display.blit(self.monster_possession_surface, self.rect.topleft)
        display.blit(self.surface, self.rect.topleft, self.srcrect)
        dirtyrects.append(self.rect)
        return


    def erase(self):
        display.blit(background, self.rect.topleft, self.rect)
        return


    def animate(self):
        self.srcrect.left += 16
        if self.srcrect.left >= 240:
            self.alive = 0
            self.spawn_monster()
        self.frame_time = timer.current_time + self.frame_duration
        


    def think(self):
        if timer.current_time <= self.frame_time:
            return
        else:
            self.animate()
        

    def spawn_monster(self):
        if self.monster_type:
            g_monsters.append(self.monster_type(self.rect, self.monster_possession))
        elif self.monster_possession:
            g_items.append(self.monster_possession(self.rect.topleft))
        

class Timer:
    def __init__(self):
        self.last_frame_ms = 0
        self.this_frame_ms = 0
        self.frame_duration = 0.000
        self.current_time = 0


    def calculate_frame_duration(self):
        self.this_frame_ms = pygame.time.get_ticks()
        self.frame_duration = ((self.this_frame_ms - self.last_frame_ms) / 1000.000)
        self.last_frame_ms = self.this_frame_ms
        return


    def set_current_time(self):
        self.current_time = pygame.time.get_ticks()
    
        
class Keymap:
    def __init__(self):
        self.KEY_UP = (K_KP8, K_w, K_UP)
        self.KEY_DOWN = (K_KP2, K_s, K_DOWN)
        self.KEY_LEFT = (K_KP4, K_a, K_LEFT)
        self.KEY_RIGHT = (K_KP6, K_d, K_RIGHT)
        self.KEY_ESC = (K_ESCAPE,)
        self.KEY_NEXTWEAPON = (K_KP_ENTER, K_e, K_RSHIFT)
        self.KEY_PREVWEAPON = (K_KP_PLUS, K_q, K_RCTRL)
        self.KEY_SCREENSHOT = (K_F5,)

            
# Defined Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)
LASER_RED = (255, 0, 0, 255)


# command-line options
GOD = 0
DEBUG = 0
WINDOWSTYLE = 0
ALT_MOUSE = 0

def show_title_screen():

    
    
    if sound:
        pygame.mixer.music.load(os.path.join('sound', 'schizo.xm'))
        pygame.mixer.music.play(-1)
    display.blit(Img.titlescreen, (0,0))
    textborder = pygame.Surface((404, 42)).convert()
    textborder.fill((180, 180, 180))
    display.blit(textborder, (118, 418))
    pygame.display.update()
    
    # Title text
    titlerect = pygame.Rect((192, 110, 248, 90))
    titleback = pygame.Surface((248, 90)).convert()
    titleback.fill(BLACK)
    titletext = title_font.render('Twitch', 0, (216, 216, 216), (BLACK))
    

    # story text
    intro_text = ("                                         ....TWITCH....                  " +
                  ".......Rescue the fair Penelope from the evil clutches of the cybernetic " +
                  "overlord Hippopoticus and his army of bio-robotic monsters! Arrow keys or " +
                  "asdw keys to move, mouse to aim, and left mouse button to fire. ESC to " +
                  "quit. q and e or right shift and ctrl to change weapons. By David Clark: " +
                  "silenus@telus.net. Props to ShredWheat, slouken, Tusker, Mark Baker and #sdl......")
    
    textrect = pygame.Rect((120, 420, 400, 34))
    textback = pygame.Surface((400, 34)).convert()
    
    textback.fill(BLACK)
    text_surface = text_font.render(intro_text, 0, (180, 180, 180), BLACK)
    
    text_offset = 0.0
    
    while 1:
        display.blit(titleback, (192, 110))
        x = 240 + whrandom.randint(0, 4)
        y = 114 + whrandom.randint(0, 4)
        display.blit(titletext, (x, y))

        display.blit(textback, (textrect.topleft))
        display.blit(text_surface, (textrect.left, textrect.top + 4), (text_offset, 0, 400, 34))
        text_offset += 0.5
        if text_offset > text_surface.get_width():
            text_offset = 0.0

        
        pygame.display.update((titlerect, textrect))

        pygame.event.peek()
       
        keys = pygame.key.get_pressed()
        for key in keymap.KEY_ESC:
            if keys[key]:
                end_game_quit()

        if pygame.mouse.get_pressed()[0]:
            if sound:
                pygame.mixer.music.fadeout(1000)
            pygame.time.delay(1000)
            break
        
    return


def end_game_victory():
    if sound:
        pygame.mixer.music.load(os.path.join('sound', 'fealingnull.xm'))
        pygame.mixer.music.play(-1)
    display.fill(BLACK)

    # display victory message
    
    font = pygame.font.Font(os.path.join('images', 'younffp_.ttf'), 24)
    level_intro_message = font.render('Victory! ', 1, (255, 255, 255))
    display.fill((0, 0, 216, 255), (272, 220, 96, 40))
    display.fill((0, 0, 128, 255), (276, 224, 88, 32))
    display.blit(level_intro_message, (280, 228))
    pygame.display.flip()
    if not DEBUG:
        pygame.time.delay(2500)

    # draw player

    display.blit(Img.player, (272, 100), (48, 0, 16, 16))
    
    # draw penelope
    
    display.blit(Img.penelope, (352, 100), (0, 0, 16, 16))

    pygame.display.flip()
    
    # fade in heart.
    blackback = pygame.Surface((16, 16))
    blackback.fill(BLACK)
    
    for alpha in range (0, 256, 2):
        Img.heart.set_alpha(alpha)
        display.blit(blackback, (312, 100), (0, 0, 16, 16))
        display.blit(Img.heart, (312, 100), (0, 0, 16, 16))
        pygame.display.update((312, 100, 16, 16))
        pygame.time.delay(50)
        
   
       
    while 1:
        pygame.event.peek()
        keys = pygame.key.get_pressed()
        for key in keymap.KEY_ESC:
            if keys[key]:
                end_game_quit()
            

def play_sound(sound, volume, loop = 0):
    if sound:
        try:
            sound.play(loop).set_volume(volume)
        except AttributeError:   # no free channel
            pass                 # play nothing.
    return


# Constants for line-segment tests
DONT_INTERSECT = 0
COLINEAR = -1

def have_same_signs(a, b):
    return ((a ^ b) >= 0)



def line_seg_intersect(line1point1, line1point2, line2point1, line2point2):
    x1 = line1point1[0]
    y1 = line1point1[1]
    x2 = line1point2[0]
    y2 = line1point2[1]
    x3 = line2point1[0]
    y3 = line2point1[1]
    x4 = line2point2[0]
    y4 = line2point2[1]

    a1 = y2 - y1  
    b1 = x1 - x2  
    c1 = (x2 * y1) - (x1 * y2)

    r3 = (a1 * x3) + (b1 * y3) + c1  
    r4 = (a1 * x4) + (b1 * y4) + c1

    if ((r3 != 0) and (r4 != 0) and have_same_signs(r3, r4)):
        return(DONT_INTERSECT)

    a2 = y4 - y3  
    b2 = x3 - x4  
    c2 = x4 * y3 - x3 * y4

    r1 = a2 * x1 + b2 * y1 + c2  
    r2 = a2 * x2 + b2 * y2 + c2

    if ((r1 != 0) and (r2 != 0) and have_same_signs(r1, r2)):  
         return(DONT_INTERSECT)

    denom = (a1 * b2) - (a2 * b1)  
    if denom == 0:  
        return(COLINEAR)
    elif denom < 0:
        offset = (-1 * denom / 2)
    else:
        offset = denom / 2
    
    num = (b1 * c2) - (b2 * c1)
    if num < 0:
        x = (num - offset) / denom
    else:
        x = (num + offset) / denom

    num = (a2 * c1) - (a1 * c2)  
    if num <0:
        y = (num - offset) / denom
    else:
        y = (num - offset) / denom

    return (x, y)


def can_see(source, target):
    los_line_p1 = source.rect.center
    los_line_p2 = target.rect.center
 

    # check each candidate rect against this los line. If any of them
    # intersect, the los is blocked.

    for rect in level.los_blocking_rects:
        block_p1 = rect.topleft
        block_p2 = rect.bottomright
        if line_seg_intersect(los_line_p1, los_line_p2, block_p1, block_p2):
            return 0
        block_p1 = rect.topright
        block_p2 = rect.bottomleft
        if line_seg_intersect(los_line_p1, los_line_p2, block_p1, block_p2):
            return 0
    return 1


def debug_wait():                      # DEBUG
    #wait for user to hit enter at the console
    raw_input()

    
def load_image(file, transparent = 0):
    # Cross - platform image file loading as a utility function.
    # load_image( filename as a string, transparent toggle as boolean
    #             1 = transparent, 0 = opaque.)
    file = os.path.join('images', file)
    try:
        surface = pygame.image.load(file)
    except RuntimeError:
       # raise SystemExit,  pygame.get_error()
       hld = 10
    if transparent:
        corner = surface.get_at((0, 0))
        surface.set_colorkey(corner, pygame.RLEACCEL)
    return surface.convert()


def process_input():
    if pygame.event.peek(pygame.QUIT):
        end_game_quit()
    keystate = pygame.key.get_pressed()

    
    for key in keymap.KEY_ESC:
        if keystate[key]:
            end_game_quit()

    player.vel_x = 0.000
    player.vel_y = 0.000
    player.state = 0
    player_vel = timer.frame_duration * Player.speed
    for key in keymap.KEY_UP: 
        if keystate[key]:
            player.vel_y -= player_vel
            player.state = 1
    for key in keymap.KEY_DOWN:
        if keystate[key]:
            player.vel_y += player_vel
            player.state = 3
    for key in keymap.KEY_LEFT:
        if keystate[key]:
            player.vel_x -= player_vel
            player.state = 4
    for key in keymap.KEY_RIGHT:
        if keystate[key]:
            player.vel_x += player_vel
            player.state = 2

    for key in keymap.KEY_NEXTWEAPON:
        if keystate[key]:
            player.choose_next_weapon()
    for key in keymap.KEY_PREVWEAPON:    
        if keystate[key]:
            player.choose_prev_weapon()


    if pygame.mouse.get_pressed()[0]:
        if player.current_weapon == 5:
            player.weapons[5].fire(player.rect.center, crosshair.rect.center)
        else:
            player.weapons[player.current_weapon].fire(player.rect.center, calculate_angle(player, crosshair))

    for key in keymap.KEY_SCREENSHOT:
        if keystate[key]:
            take_screenshot()
    pygame.event.pump()
    return


def calculate_angle(source_obj, target_obj):
    delta_x = target_obj.rect.left - source_obj.rect.left * 1.000
    delta_y = target_obj.rect.top - source_obj.rect.top * 1.000
    if delta_x == 0:
        delta_x = 0.1
    angle = int(math.atan(delta_y / delta_x) * 180 / math.pi)
    if delta_x < 0:
        angle += 180
    if angle < 0:
        angle += 360
    return angle


def calculate_range(source_obj, target_obj):
    delta_x = target_obj.rect.left - source_obj.rect.left * 1.000
    delta_y = target_obj.rect.top - source_obj.rect.top * 1.000
    range = math.sqrt(delta_x**2 + delta_y**2)
    return range

def process_options():
    global GOD 
    global DEBUG
    global WINDOWSTYLE
    global ALT_MOUSE
    global current_level_number
    global sound
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hgdfmsl:")
    except getopt.GetoptError:
        # print help information and exit:
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        if o in ("-g", "--god"):
            GOD = 1
        if o in ("-d", "--debug"):
            DEBUG = 1
        if o in ("-f", "--fullscreen"):
            WINDOWSTYLE = pygame.FULLSCREEN
        if o in ("-m", "--altmouse"):
            ALT_MOUSE = 1
        if o in ("-l", "--level"):
            current_level_number = int(a) - 1
        if o in ("-s", "--silent"):
            sound = 0
    return
            
def usage():
    print ("Twitch.py - A cross-platform topdown shooter for pygame and SDL.")
    print ("usage: twitch.py [options]")
    print ("\n")
    print ("Option:   -h or --help :       Print this help text.")
    print ("          -d or --debug :      Debug mode (eliminates pauses).")
    print ("          -g or --god :        God mode (player takes no damage).")
    print ("          -f or --fullscreen : Fullscreen mode.")
    print ("          -m or --altmouse:    Relative mouse mode.")
    print ("          -s or --silent:      No sound.")
    print ("          -l levelnumber or --level levelnumber: Start at given level number (1-10)")
    sys.exit(0)
    


def take_screenshot():
    try:
        display.save('screenshot.bmp')
    except pygame.error:
        print ("Error: couldn't write screenshot.bmp to current directory.")

        
def end_game_quit():
    print ("Exit - quitting.")
    sys.exit()






if __name__ == "__main__":
    
    current_level_number = 0
    sound = 1
    
    # process command-line arguments
    process_options()

    if DEBUG:
        if DEBUG:
            print ("Debug mode ON.")
        if GOD:
            print ("God mode ON.")
        if WINDOWSTYLE == pygame.FULLSCREEN:
            print ("Fullscreen mode ON.")
        if ALT_MOUSE:
            print ("Alt mouse mode activated.")
    
    
    # Prepares the video and sound subsystems
    try:
        pygame.display.init()
        display = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT), WINDOWSTYLE )
    except:
        #raise SystemExit, "Unable to acquire 640 x 480 video surface. Sorry."
        hld = 10
    background = pygame.Surface( ( SCREEN_WIDTH, SCREEN_HEIGHT) )
    screenrect = pygame.Rect(0, 0, SCREEN_WIDTH, (SCREEN_HEIGHT - 16))
    if sound:
        try:
            pygame.mixer.init()
            sound = 1
        except:
            print ("Unable to initialize sound subsystem. Proceeding without sound.")
            sound = 0
    try:
        pygame.font.init()
    except:
       # raise SystemExit, "Twitch requires font support. Please see README"
       hld = 10

    # make the mouse behave

    pygame.event.set_grab(1)
    pygame.mouse.set_visible(0)

    # Load keymap from the disk
    keymap = Keymap()

    # suppress the mouse pointer if we're fullscreen
    if WINDOWSTYLE == pygame.FULLSCREEN:
        pygame.mouse.set_visible(0)

 

    # Load video and sound resources from disk
    Img.titlescreen = load_image('title.png', 0)
    Img.player = load_image('player.png', 1)
    Img.damage = load_image('damage.png', 1)
    Img.player_death = load_image('player_death.png', 1)
    Img.gate = load_image('gate.png', 1)
    Img.weapons = load_image('weapons.png', 0)
    Img.weapons_selected = load_image('weaponsel.png', 0)
    Img.health_full = load_image('healthfull.png', 0)
    Img.health_empty = load_image('healthempty.png', 0)
    Img.crosshair = load_image('crosshair.png', 1)
    Img.spawngate = load_image('spawngate.png', 1)
    Img.hunter = load_image('hunter.png', 1)
    Img.hunter_dying = load_image('hunter_dying.png', 1)
    Img.shooter = load_image('shooter.png', 1)
    Img.shooter_dying = load_image('shooter_dying.png', 1)
    Img.gunner = load_image('gunner.png', 1)
    Img.gunner_dying = load_image('gunner_dying.png', 1)
    Img.spider = load_image('spider.png', 1)
    Img.spider_dying = load_image('spider_dying.png', 1)
    Img.robot = load_image('robot.png', 1)
    Img.robot_dying = load_image('robot_dying.png', 1)
    Img.boss = load_image('boss.png', 1)
    Img.boss_dying = load_image('boss_dying.png', 1)
    Img.rocket = load_image('rocket.png', 1)
    Img.grenade = load_image('grenade.png', 1)
    Img.bomb = load_image('bomb.png', 1)
    Img.flame = load_image('flame.png', 1)
    Img.fire = load_image('fire.png', 1)
    Img.smoke = load_image('smoke.png', 1)
    Img.explosion = load_image('explosion.png', 1)
    Img.key = load_image('key.png', 1)
    Img.healthkit = load_image('healthkit.png', 1)
    Img.bulletammo = load_image('bulletammo.png', 1)
    Img.laserammo = load_image('laserammo.png', 1)
    Img.rocketammo = load_image('rocketammo.png', 1)
    Img.flamerammo = load_image('flamerammo.png', 1)
    Img.grenadeammo = load_image('grenadeammo.png', 1)
    Img.bombammo = load_image('bombammo.png', 1)
    Img.heart = load_image('heart.png', 1)
    Img.penelope = load_image('penelope.png', 1)
    title_font = pygame.font.Font(os.path.join('images', 'younffp_.ttf'), 48)
    text_font = pygame.font.Font(os.path.join('images', 'younffp_.ttf'), 28)
    ammo_font = pygame.font.Font(os.path.join('images', 'younffp_.ttf'), 16)
    ammo_font_erase = ammo_font.render('    ', 0, BLACK, BLACK)
    if sound:
        Snd.level_intro_music = pygame.mixer.Sound(os.path.join('sound', 'levelintro.wav'))
        Snd.rocket = pygame.mixer.Sound(os.path.join('sound', 'rocket.wav'))
        Snd.laser = pygame.mixer.Sound(os.path.join('sound', 'laser.wav'))
        Snd.shotgun = pygame.mixer.Sound(os.path.join('sound', 'shotgun.wav'))
        Snd.machinegun = pygame.mixer.Sound(os.path.join('sound', 'mg.wav'))
        Snd.grenade = pygame.mixer.Sound(os.path.join('sound', 'gchuck.wav'))
        Snd.spawngate = pygame.mixer.Sound(os.path.join('sound', 'spawngate.wav'))
        Snd.bombblast = pygame.mixer.Sound(os.path.join('sound', 'bombblast.wav'))
        Snd.pickup = pygame.mixer.Sound(os.path.join('sound', 'pickup.wav'))
        Snd.pickup_health = pygame.mixer.Sound(os.path.join('sound', 'pickuphealth.wav'))
        Snd.hunterdeath = pygame.mixer.Sound(os.path.join('sound', 'hunterdeath.wav'))
        Snd.explosion = pygame.mixer.Sound(os.path.join('sound', 'explosion.wav'))
        Snd.flame = pygame.mixer.Sound(os.path.join('sound', 'flame.wav'))
        Snd.weapon_switch = pygame.mixer.Sound(os.path.join('sound', 'weaponswitch.wav'))
        Snd.player_death = pygame.mixer.Sound(os.path.join('sound', 'playerdeath.wav'))
        Snd.player_pain = []
        Snd.player_pain.append(pygame.mixer.Sound(os.path.join('sound', 'pain1.wav')))
        Snd.player_pain.append(pygame.mixer.Sound(os.path.join('sound', 'pain2.wav')))
        Snd.player_pain.append(pygame.mixer.Sound(os.path.join('sound', 'pain3.wav')))
        Snd.gate_down = pygame.mixer.Sound(os.path.join('sound', 'gatedown.wav'))
        Snd.gate_up = pygame.mixer.Sound(os.path.join('sound', 'gateup.wav'))
        
                               
    
    show_title_screen()

    # Create dirtyrects[] global for easy access
    dirtyrects = []
    
    player = Player()
    statusbar = Statusbar()
    crosshair = Crosshair(320, 240)
    timer = Timer()
    
    while 1:
        bullets = []
        laserbeams = []
        g_rockets = []
        g_grenades = []
        g_bombs = []
        g_items = []
        g_decals = []
        g_smokes = []
        g_explosions = []
        g_monsters = []
        g_spawngates = []
        g_flames = []
        g_fires = []

        current_level_number += 1

        # load current block and blank graphics

        if current_level_number >= 1 and current_level_number < 4:
            Img.blank = load_image('blank1.png', 0)
            Img.block = load_image('block1.png', 0)
        elif current_level_number >= 4 and current_level_number < 7:
            Img.blank = load_image('blank2.png', 0)
            Img.block = load_image('block2.png', 0)
        elif current_level_number >= 7 and current_level_number < 10:
            Img.blank = load_image('blank3.png', 0)
            Img.block = load_image('block3.png', 0)
        else:
            Img.blank = load_image('blank4.png', 0)
            Img.block = load_image('block4.png', 0)
        level = Level(current_level_number)
        level.load_map_file(current_level_number)
        level.calculate_impassable_rects()
        
        
        level.introduce()
        pygame.display.flip()
        pygame.event.pump()
        
        timer.set_current_time()
        timer.calculate_frame_duration()      # compensate for 1st frame weirdness when changing levels
        timer.calculate_frame_duration()
        # Action loop
        while 1:
            timer.set_current_time()
            
            dirtyrects = []
            
            # let everyone think
            
            player.think()
            crosshair.think()
            [monster.think() for monster in g_monsters]
            [decal.think() for decal in g_decals]
            [smoke.think() for smoke in g_smokes]
            [explosion.think() for explosion in g_explosions]
            [laserbeam.think() for laserbeam in laserbeams]
            [rocket.think() for rocket in g_rockets]
            [grenade.think() for grenade in g_grenades]
            [spawngate.think() for spawngate in g_spawngates]
            [bomb.think() for bomb in g_bombs]
            [fire.think() for fire in g_fires]
            [flame.think() for flame in g_flames]

            # see whether we want to spawn in a monster
            level.check_to_spawn(timer.current_time)

                
            process_input()
            mouse_delta_x, mouse_delta_y = pygame.mouse.get_rel()

            # erase everything
            
            player.erase()
            crosshair.erase()
            [item.erase() for item in g_items]
            [monster.erase() for monster in g_monsters]
            [bullet.erase() for bullet in bullets]
            [laserbeam.erase() for laserbeam in laserbeams if laserbeam.colour_number <= 0]
            [rocket.erase() for rocket in g_rockets]
            [grenade.erase() for grenade in g_grenades]
            [bomb.erase() for bomb in g_bombs]
            [smoke.erase() for smoke in g_smokes]
            [explosion.erase() for explosion in g_explosions]
            [spawngate.erase() for spawngate in g_spawngates]
            [flame.erase() for flame in g_flames]
            [fire.erase() for fire in g_fires]
            
            # move everything
            
            movement = player.walk()
            crosshair.move(mouse_delta_x, mouse_delta_y, movement)
            [monster.walk() for monster in g_monsters]
            [bullet.move() for bullet in bullets]
            [rocket.move() for rocket in g_rockets]
            [grenade.move() for grenade in g_grenades]
            [flame.move() for flame in g_flames]

            # draw everything

        
            player.draw()
            crosshair.draw()
            [item.draw() for item in g_items if item.alive]
            [monster.draw() for monster in g_monsters]
            [bullet.draw() for bullet in bullets if bullet.alive]
            [rocket.draw() for rocket in g_rockets if rocket.alive]
            [grenade.draw() for grenade in g_grenades if grenade.alive]
            [laserbeam.draw() for laserbeam in laserbeams if laserbeam.colour_number > 0]
            [decal.draw() for decal in g_decals]
            [flame.draw() for flame in g_flames if flame.alive]
            [fire.draw() for fire in g_fires if fire.alive]
            [bomb.draw() for bomb in g_bombs if bomb.alive]
            [smoke.draw() for smoke in g_smokes if smoke.alive]
            [explosion.draw() for explosion in g_explosions if explosion.alive]
            [spawngate.draw() for spawngate in g_spawngates]
            
            # Draw all our pretty pictures
                
            pygame.display.update(dirtyrects)

            # Cull the dead
            
            g_monsters = [monster for monster in g_monsters if monster.alive]
            bullets = [bullet for bullet in bullets if bullet.alive]
            laserbeams = [laserbeam for laserbeam in laserbeams if laserbeam.colour_number > 0]
            g_rockets = [rocket for rocket in g_rockets if rocket.alive]
            g_grenades = [grenade for grenade in g_grenades if grenade.alive]
            g_bombs = [bomb for bomb in g_bombs if bomb.alive]
            g_decals = [decal for decal in g_decals if decal.colour_number > 1]
            g_smokes = [smoke for smoke in g_smokes if smoke.alive]
            g_explosions = [explosion for explosion in g_explosions if explosion.alive]
            g_spawngates = [spawngate for spawngate in g_spawngates if spawngate.alive]
            g_flames = [flame for flame in g_flames if flame.alive]
            g_fires = [fire for fire in g_fires if fire.alive]
            
            timer.calculate_frame_duration()

            # check for end-of-level
            if level.number != 10:
                if player.colliderect.colliderect(level.exit_tile.rect):
                    break

            # check for player death

            if player.health < 1:
                player.animate_death()
                end_game_quit()

            
        
    end_game_quit()
