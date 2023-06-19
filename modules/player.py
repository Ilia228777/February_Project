import modules.settings as settings
import modules.object as object
import modules.npc as npc
import modules.sound as sound
# import modules.enemy as enemy

import pygame


class Player(object.Object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.HEALTH = 5
        self.GRAVITY = False
        self.INVENTORY = []

        
        self.MAX_JUMP = 240
        self.SPEED_JUMP = 4

    def move(self, area):       

        self.gravity(area)

        event = pygame.key.get_pressed()

        self.col_up(area)



        if event[pygame.K_d]:
            self.col_right(area)
            self.DIRECTION = "R"
            if self.MOVE_RIGHT == True:
                self.X += 5
                self.RECT.x += 5

            if sound.sound_repeat % 20 == 0:
                if self.MOVE_DOWN == False:
                    sound.sound("walk.wav", 0.1)
            self.direction()
            self.animation("Player", 1, 4)


        if event[pygame.K_a]:
            self.col_left(area)
            self.DIRECTION = "L"
            if self.MOVE_LEFT == True:
                self.X -= 5
                self.RECT.x -= 5
            
            if sound.sound_repeat % 20 == 0:
                if self.MOVE_DOWN == False:
                    sound.sound("walk.wav", 0.1)
            self.direction()
            self.animation("Player", 1, 4)


        if event[pygame.K_w] and self.JUMP == False and self.GRAVITY == False:
            self.JUMP = True


        if event[pygame.K_e]:   
            if settings.scene == "loc1":
                if self.X + 10 >= settings.lever.X and self.Y == settings.lever.Y:
                    settings.lever.NAME_IMG = "images\lever.png"
                    settings.lever.load_image()
                    if settings.trapdoor_pressed == False:
                        settings.trapdoor_pressed = True

                if self.X + 10 >= settings.lever2.X and self.Y == settings.lever2.Y:
                    settings.lever2.NAME_IMG = "images\lever.png"
                    settings.lever2.load_image()
                    if settings.laser_pressed == False:
                        settings.laser_pressed = True
            

            
            if settings.scene == "loc2":
                if settings.need_keys == True:
                    if self.X < settings.keys.X and self.Y > settings.keys.Y:
                        if self.X + 50 >= settings.keys.X and self.Y - 20 <= settings.keys.Y:
                            if not "keys" in self.INVENTORY:
                                self.INVENTORY.append("keys")
                    if self.X > settings.keys.X and self.Y > settings.keys.Y:        
                        if self.X - 50 <= settings.keys.X and self.Y - 20 <= settings.keys.Y:
                            if not "keys" in self.INVENTORY:
                                self.INVENTORY.append("keys")

                if self.X < settings.medkit.X and self.Y >= settings.medkit.Y:
                    if self.X + 50 >= settings.medkit.X and self.Y - 20 <= settings.medkit.Y:
                        self.HEALTH = 5
                        sound.sound('health.wav', 0.1)
                if self.X > settings.medkit.X and self.Y >= settings.medkit.Y:        
                    if self.X - 50 <= settings.medkit.X and self.Y - 20 <= settings.medkit.Y:
                        self.HEALTH = 5
                        sound.sound('health.wav', 0.1)
            
            if settings.scene == "loc3":
                if self.X < settings.computer.X:
                    if self.X + 50 >= settings.computer.X and self.Y == settings.computer.Y:
                        settings.scene = "computer"
                if self.X > settings.computer.X:
                    if self.X - 50 <= settings.computer.X and self.Y == settings.computer.Y:
                        settings.scene = "computer"
                if settings.need_vending_machine == True:
                    if self.X < settings.vending_machine.X:
                        if self.X + 50 >= settings.vending_machine.X and self.Y == settings.vending_machine.Y:
                            settings.scene = "vending machine"
                            if settings.vending_machine_pressed == False:
                                settings.vending_machine_pressed = True
    
                    if self.X > settings.vending_machine.X:
                        if self.X - 50 <= settings.vending_machine.X and self.Y == settings.vending_machine.Y:
                            settings.scene = "vending machine"
                            if settings.vending_machine_pressed == False:
                                settings.vending_machine_pressed = True

                if self.X > settings.elec.X:
                    if self.X - 10 <= settings.elec.X and self.Y == settings.elec.Y:
                        if "screwdriver" in self.INVENTORY:
                            settings.scene = "wires"

                if self.X < settings.elec.X:
                    if self.X + 10 >= settings.elec.X and self.Y == settings.elec.Y:
                        if "screwdriver" in self.INVENTORY:
                            settings.scene = "wires"
            if settings.scene == "loc4":
                if self.X < settings.spaceship.X:
                    if self.X + 50 >= settings.spaceship.X:
                        if self.Y >= settings.spaceship.Y:
                            if self.Y - 50 <= settings.spaceship.Y:
                                settings.scene = "cutscene2"

                if self.X > settings.spaceship.X:
                    if self.X - 50 <= settings.spaceship.X:
                        if self.Y >= settings.spaceship.Y:
                            if self.Y - 50 <= settings.spaceship.Y:
                                settings.scene = "cutscene2" 
                

        # if siren.ENEMY_MOVE == True:
        #     self.col_right(siren_list)
        #     if self.MOVE_RIGHT == False:
        #         print(self.MOVE_RIGHT)
        #         self.HEALTH -= 1 
        #     self.col_left(siren_list)
        #     if self.MOVE_LEFT == False:
        #         # print(self.MOVE_RIGHT)
        #         self.HEALTH -= 1 
              

        if self.JUMP == True:
            self.col_up(area)
            self.RECT.y -= self.SPEED_JUMP
            self.Y -= self.SPEED_JUMP
            self.MAX_JUMP -= self.SPEED_JUMP
            self.GRAVITY = False
            print(self.MAX_JUMP)
            if self.MAX_JUMP == 0:
                self.JUMP = False
                self.MAX_JUMP = 280
                self.GRAVITY = True
    
        if self.JUMP == False:
            self.MAX_JUMP = 280

        if self.MOVE_DOWN == True:
            self.GRAVITY = True

     

        if not event:
            self.NAME_IMG = "images\Player\\0.png"
            self.direction()
        
    

    def show_dialog(self, npc_object):
        event = pygame.key.get_pressed()
        if event[pygame.K_e]:
            
            if npc_object.SHOW_DIALOG == False and self.RECT.x + 50 >= npc_object.RECT.x and self.Y == npc_object.Y:
                npc_object.SHOW_DIALOG = True
            if npc_object.SHOW_DIALOG == False and self.RECT.x - 50 <= npc_object.RECT.x and self.Y == npc_object.Y:
                npc_object.SHOW_DIALOG = True
            
        if npc_object.SHOW_DIALOG == True and self.RECT.x - 50 > npc_object.RECT.x:
            npc_object.SHOW_DIALOG = False
        
        if npc_object.SHOW_DIALOG == True and self.RECT.x + 50 < npc_object.RECT.x:
            npc_object.SHOW_DIALOG = False


    def exit(self, area, enemy, win):
        for door in area.list_door_right:
            if self.RECT.x >= door.RECT.x and self.RECT.y >= door.RECT.y:
                area.list_block_area.clear()
                # area.list_block_rect.clear()
                area.list_door_right.clear()
                # area.list_door_right_rect.clear()
                area.list_door_left.clear()
                # area.list_door_left_rect.clear()
                area.list_turrets.clear()
                # area.list_turrets_rect.clear()
                area.list_bullet.clear()
                area.list_npc.clear()
                area.list_lever.clear()
                area.list_ladder.clear()
                area.list_bed.clear()
                area.list_siren.clear()
                area.list_vending_machine.clear()
                area.list_computer.clear()
                area.list_balloon.clear()
                area.list_medkit.clear()
                
                self.CURRENT_LEVEL += 1 

                if self.CURRENT_LEVEL == 1:
                    settings.scene = "loc2"
                    enemy.turret.shoot(win, "L", 200)
                if self.CURRENT_LEVEL == 2:
                    settings.scene = "loc3"
                if self.CURRENT_LEVEL == 3:
                    if settings.terminal == False:
                        settings.scene = "terminal"
                    else:
                        settings.scene = "loc4"
                area.create_area(0,0)
                        

        for door in area.list_door_left:
            if self.RECT.x <= door.RECT.x and self.RECT.y >= door.RECT.y:
                area.list_block_area.clear()
                area.list_door_right.clear()
                area.list_door_left.clear()
                # area.list_door_left_rect.clear()
                area.list_turrets.clear()
                # area.list_turrets_rect.clear()
                area.list_bullet.clear()
                area.list_lever.clear()
                area.list_ladder.clear()
                area.list_bed.clear()
                area.list_npc.clear()
                area.list_siren.clear()
                area.list_vending_machine.clear()
                area.list_computer.clear()
                area.list_balloon.clear()
                area.list_shkaf.clear()
                area.list_medkit.clear()
                
                self.CURRENT_LEVEL -= 1

                if self.CURRENT_LEVEL == 0:
                    settings.bg1.blit_sprite(win)
                    settings.scene = "loc1"
                    area.create_area(600, 540)
                    enemy.turret.shoot(win, "R", 200)
                if self.CURRENT_LEVEL == 1:
                    settings.scene = "loc2"
                    enemy.turret.shoot(win, "L", 200)
                    area.create_area(660, 0)
                if self.CURRENT_LEVEL == 2:
                    settings.scene = "loc3"
                    area.create_area(600,120)
                if self.CURRENT_LEVEL == 3:
                    settings.scene = "loc4"
                    area.create_area(0,0)

    def health_font(self, win):
        self.load_image()
        bg_health = settings.Settings(
            width = 270,
            height = 200, 
            x = -75,
            y = -80,
            name_img="images\Player\health_bg.png",
            color = "yellow"
        )
        bg_health.blit_sprite(win)
        font = pygame.font.Font('fonts\\PixelFont.ttf', 70)
        text = font.render(str(self.HEALTH), 1, (225,22,25), None)
        win.blit(text, (70, 0))
        heart_sprite = settings.Settings(
            width = 60,
            height = 60, 
            x = 5,
            y = 10,
            name_img="images\Player\health.png",
            color = "yellow"
        )    
        heart_sprite.blit_sprite(win)


    def die(self):
        settings.scene = "game_over"
    
    
hero = Player(
    width = 45,
    height = 55,
    x = 0,
    y = 0,
    name_img = "images\\Player\\0.png",
    color = "red"
) 