import pygame as pg
import math
import random
import os


class StartScreen:
    @staticmethod
    def draw(sc):
        tela_sprite = pg.image.load(os.path.join('assets', 'screens', 'StartScreen.png'))
        sc.blit(tela_sprite, (0,0))


class LoreScreen:
    @staticmethod
    def draw(sc):
        tela_sprite = pg.image.load(os.path.join('assets', 'screens', 'LoreScreen.png'))
        sc.blit(tela_sprite, (0,0))


class GameScreen:
    @staticmethod
    def draw():
        pass


class Elemento:
    ELEMENT_LIST = []
    SCREEN_STATE = []
    def __init__(self) -> None:
        self.ELEMENT_LIST.append(self)
        self.horda = 1

    def move(self, velX, velY):
        self.pos[0] += velX
        self.pos[1] += velY
    
    def draw(self, sc, ct):
        if self.SCREEN_STATE == []:
            self.SCREEN_STATE.append(StartScreen)
        if self.SCREEN_STATE[0] != GameScreen:
            self.SCREEN_STATE[0].draw(sc)
            return
        if self.__class__ == Elemento:
            font = pg.font.Font('freesansbold.ttf', 16)
            img = font.render(f'HORDA ATUAL: {self.horda}', True, (0, 255, 0))
            sc.blit(img, (1250, 20))
            return
        sc.blit(self.sprite, self.pos)
        self.beenDrawn(ct)
        self.drawlife(sc)
            
    
    def drawlife(self, sc):
        pass

    def update(self, inp, sc, ct):
        if self.SCREEN_STATE == []:
            self.SCREEN_STATE.append(StartScreen)
        if self.SCREEN_STATE[0] != GameScreen:
            if self.SCREEN_STATE[0] == StartScreen:
                if len(self.ELEMENT_LIST) > 1:
                    for i in range(len(self.ELEMENT_LIST)-1):
                        self.ELEMENT_LIST.remove(self.ELEMENT_LIST[1])

                try:
                    if 40 <= inp['mouse'][1][0] <= 218:
                        if 217 <= inp['mouse'][1][1] <= 360:
                            self.SCREEN_STATE[0] = GameScreen
                except TypeError:
                    pass
                try:
                    if 722 <= inp['mouse'][1][0] <= 899:
                        if 529 <= inp['mouse'][1][1] <= 676:
                            self.SCREEN_STATE[0] = LoreScreen
                except TypeError:
                    pass
            if self.SCREEN_STATE[0] == LoreScreen:
                try:
                    if 1043 <= inp['mouse'][1][0] <= 1347:
                        if 604 <= inp['mouse'][1][1] <= 690:
                            self.SCREEN_STATE[0] = StartScreen
                except TypeError:
                    pass
            return
        if len(self.ELEMENT_LIST) == 1:
            self.jogador = PersonagemGreen((32, 32), (0, 255, 0), [720, 360], "greenChar\\")
            PersonagemYellow((32, 32), (255, 255, 0), self.gerar_posicao(self.jogador), f'yellowChar\\')
            PersonagemRed((32, 32), (255, 0, 0), self.gerar_posicao(self.jogador), f'redChar\\')
            PersonagemBlue((32, 32), (0, 255, 255), self.gerar_posicao(self.jogador), f'blueChar\\')
            PersonagemOrange((32, 32), (255, 127, 0), self.gerar_posicao(self.jogador), f'orangeChar\\')
            PersonagemViolet((32, 32), (139, 0, 255), self.gerar_posicao(self.jogador), f'violetChar\\')
            PersonagemIndigo((32, 32), (0, 0, 255), self.gerar_posicao(self.jogador), f'indigoChar\\')
        
        for element in self.ELEMENT_LIST:
            if element.__class__ == PersonagemGreen:
                element = -1
                break
        if element != -1:
            self.horda = 1
            self.list_pos = []
            self.SCREEN_STATE[0] = StartScreen
            return
        
        if element == -1 and len(self.ELEMENT_LIST) == 2:
            self.jogador.life = 1 + self.horda
            PersonagemYellow((32, 32), (255, 255, 0), self.gerar_posicao(self.jogador), f'yellowChar\\')
            PersonagemRed((32, 32), (255, 0, 0), self.gerar_posicao(self.jogador), f'redChar\\')
            PersonagemBlue((32, 32), (0, 255, 255), self.gerar_posicao(self.jogador), f'blueChar\\')
            PersonagemOrange((32, 32), (255, 127, 0), self.gerar_posicao(self.jogador), f'orangeChar\\')
            PersonagemViolet((32, 32), (139, 0, 255), self.gerar_posicao(self.jogador), f'violetChar\\')
            PersonagemIndigo((32, 32), (0, 0, 255), self.gerar_posicao(self.jogador), f'indigoChar\\')
            for h in range(self.horda):
                h = h % 5
                if h == 0:
                    PersonagemYellow((32, 32), (255, 255, 0), self.gerar_posicao(self.jogador), f'yellowChar\\')
                if h == 1:
                    PersonagemBlue((32, 32), (0, 255, 255), self.gerar_posicao(self.jogador), f'blueChar\\')
                if h == 2:
                    PersonagemOrange((32, 32), (255, 127, 0), self.gerar_posicao(self.jogador), f'orangeChar\\')
                if h == 3:
                    PersonagemViolet((32, 32), (139, 0, 255), self.gerar_posicao(self.jogador), f'violetChar\\')
                if h == 4:
                    PersonagemIndigo((32, 32), (0, 0, 255), self.gerar_posicao(self.jogador), f'indigoChar\\')
            self.horda += 1

        
        current_colisions = self.colisions()
        for colision in current_colisions:
            colision[0].colision(colision[1], ct)

    def colisions(self):
        colision = []
        for element1 in self.ELEMENT_LIST:
            for element2 in self.ELEMENT_LIST:
                if (element1 == element2 or 
                    element1.__class__ in [Elemento, Estilhaco] or 
                    element2.__class__ in [Elemento, Estilhaco]):
                    continue
                hitbox1 = self.hitbox(element1)
                hitbox2 = self.hitbox(element2)
                if (hitbox1["left"] < hitbox2["right"] and 
                    hitbox1["right"] > hitbox2["left"] and
                    hitbox1["up"] < hitbox2["down"] and
                    hitbox1["down"] > hitbox2["up"]):
                    current_colision = [element1, element2]
                    colision.append(current_colision)
        return colision
    
    def hitbox(self, element):
        left = element.pos[0]
        right = element.pos[0] + element.lenght
        up = element.pos[1]
        down = element.pos[1] + element.height
        return {"left": left,
                "right": right,
                "up": up,
                "down": down}
    
    def beenDrawn(self, ct):
        pass

    def colision(self, other, ct):
        pass
    
    list_pos = []
    def gerar_posicao(self, other):
        posicao = [math.ceil(random.random()*1400), math.ceil(random.random()*690)]
        centro = other.pos
        for pos in self.list_pos:
            if self.dist(pos, posicao) < 45:
                return self.gerar_posicao(other)
        if self.dist(posicao, centro) < 400:
            return self.gerar_posicao(other)
        self.list_pos.append(posicao)
        return posicao
    
    def dist(self, list1, list2):
        a = math.sqrt(
            (list1[1] - list2[1]) ** 2 + (list1[0] - list2[0]) ** 2
        )
        return a


class Personagem(Elemento):
    previous = 0
    animation_time = 0.5
    def __init__(self, surface=tuple, color=tuple, pos=list, sprites=str) -> None:
        self.life = 2
        self.total_life = self.life
        self.lenght = surface[0]
        self.height = surface[1]
        self.surface = pg.Surface(surface)
        self.color = color
        self.surface.fill(self.color)
        self.pos = pos
        self.sprites = {}
        i=0
        for sprite in os.listdir(os.path.join('assets', sprites)):
            self.sprites[f'{i}'] = pg.image.load(os.path.join('assets', sprites, sprite))
            i += 1
        self.sprite_time = self.animation_time / i
        self.sprite = self.sprites[str(0)]
        Personagem.ELEMENT_LIST.append(self)
    
    def beenDrawn(self, ct):
        if self.previous == 0:
            self.previous = ct
        self.now_time = ct - self.previous
        if self.now_time < self.sprite_time:
            return
        self.previous = ct
        for key in self.sprites:
            if self.sprites[key] == self.sprite:
                key = int(key) + 1
                break
        try:
            self.sprite = self.sprites[str(key)]
        except:
            self.sprite = self.sprites[str(0)]

    def update(self, inp, sc, ct):
        self.lastpos = [self.pos[0], self.pos[1]]
        self.move(self.velX, self.velY)
    
    def shoot(self, ang):
        Bala(self, ang)
    
    red_cure_cd = 0.15
    previous_red_cure = -1
    def colision(self, other, ct):
        if other.__class__ == Bala:
            if other.shooter == self:
                return
            if self.__class__ != PersonagemGreen and other.shooter.__class__ != PersonagemGreen:
                return
            if self.life <= 0:
                try:
                    self.ELEMENT_LIST.remove(self)
                except ValueError:
                    pass
                if self.__class__ == PersonagemOrange:
                    for el in self.ELEMENT_LIST:
                        if el.__class__ == PersonagemGreen:
                            jg = el
                            break
                    for i in range(40):
                        EstilhacoOrange(self, jg)
                    return
                for i in range(5):
                    Estilhaco(self)
                return
            self.life -= 1
            return
        if other.__class__ == EstilhacoOrange and self.__class__ == PersonagemGreen:
            if self.life <= 0:
                try:
                    self.ELEMENT_LIST.remove(self)
                except ValueError:
                    pass
                return
            self.life -= 1
            return
        if issubclass(other.__class__, Personagem):
            self.pos = [self.lastpos[0], self.lastpos[1]]
            other.pos = [other.lastpos[0], other.lastpos[1]]
            self.ang = math.atan2(other.pos[1] - self.pos[1], other.pos[0] - self.pos[0]) + math.pi
            if self.__class__ != PersonagemGreen:
                vel = self.velT / 1.5
                self.move(vel * math.cos(self.ang), vel * math.sin(self.ang))
                cd_red = ct - self.previous_red_cure
                if other.__class__ == PersonagemRed:
                    if cd_red < self.red_cure_cd:
                        return
                    if self.life < 2:
                        self.life += 1
                        self.cd_red = ct
                return
            if self.life <= 0:
                try:
                    self.ELEMENT_LIST.remove(self)
                except ValueError:
                    pass
                return
            self.life -= 1
            return
              
    def telaColision(self, sc):
        HEIGHT = sc.get_height()
        WIDTH = sc.get_width()
        if self.pos[0] <= 0:
            self.pos[0] = 0
        if self.pos[1] <= 0:
            self.pos[1] = 0
        if self.pos[0] >= WIDTH - self.sprite.get_width():
            self.pos[0] = WIDTH - self.sprite.get_width()
        if self.pos[1] >= HEIGHT - self.sprite.get_height():
            self.pos[1] = HEIGHT - self.sprite.get_height()

    def drawlife(self, sc):
        life_width = 30 / (self.total_life + 1)
        self.life_surface = pg.Surface((life_width * self.life + life_width, 3))
        self.life_surface.fill(self.color)
        sc.blit(self.life_surface, (self.pos[0] + 1, self.pos[1] - 5))


class PersonagemGreen(Personagem):
    def __init__(self, surface=tuple, color=tuple, pos=list, sprites=str) -> None:
        super().__init__(surface, color, pos, sprites)
    
    previous_shoot_time = -1
    shoot_cd = 0.25
    def update(self, inp, sc, ct):
        self.lastpos = [self.pos[0], self.pos[1]]
        self.move(inp)
        self.telaColision(sc)
        cd = ct - self.previous_shoot_time
        if inp["mouse"][0] == 1:
            if cd < self.shoot_cd:
                return
            self.shoot(inp)
            self.previous_shoot_time = ct

    def move(self, inp):
        vel = 7
        inp = inp['keyboard']
        if inp[1] == "UP":
            velY = -vel
        if inp[1] == "DOWN":
            velY = vel
        if not(inp[1] == "UP" or inp[1] == "DOWN"):
            velY = 0
        if inp[0] == "LEFT":
            velX = -vel
        if inp[0] == "RIGHT":
            velX = vel
        if not(inp[0] == "LEFT" or inp[0] == "RIGHT"):
            velX = 0
        if inp == [None, None] or inp is None:
            velX = velY = 0
        self.pos[0] += velX
        self.pos[1] += velY

    def shoot(self, inp):
        inp = inp["mouse"]
        ang = math.atan2(inp[1][1] - self.pos[1], inp[1][0] - self.pos[0])
        Bala(self, ang, self.color)


class PersonagemRed(Personagem):
    velT = 8
    def __init__(self, surface=tuple, color=tuple, pos=list, sprites=str) -> None:
        self.togo = [None, None]
        super().__init__(surface, color, pos, sprites)

    def search_friend(self):
        element_life = {}
        for element in self.ELEMENT_LIST:
            if (element.__class__ != PersonagemGreen and
                issubclass(element.__class__, Personagem) and
                element != self):
                element_life[element] = element.life
        self.lower_life = [None]
        for key in element_life:
            if self.lower_life[0] is None:
                self.lower_life = [key]
                continue
            if element_life[key] == self.lower_life[0].life:
                self.lower_life.append(key)
                continue
            if element_life[key] < self.lower_life[0].life:
                self.lower_life = [key]
        if self.lower_life[0] is None:
            return
        self.next_lower_life()
    
    def next_lower_life(self):
        element_dist = -1
        element_togo = None
        for element in self.lower_life:
            dist_sqr = (element.pos[1] - self.pos[1]) ** 2 + (element.pos[0] - self.pos[0]) ** 2
            if element_dist == -1:
                element_togo = element
                element_dist = dist_sqr
                continue
            if dist_sqr < element_dist:
                element_togo = element
        self.togo = [element_togo.pos[0], element_togo.pos[1]]

    def update(self, inp, sc, ct):
        self.search_friend()
        self.ang = math.atan2(self.togo[1] - self.pos[1], self.togo[0] - self.pos[0])
        self.velX = self.velT * math.cos(self.ang)
        self.velY = self.velT * math.sin(self.ang)
        self.lastpos = [self.pos[0], self.pos[1]]
        self.move(self.velX, self.velY)
        self.telaColision(sc)
        

class PersonagemOrange(Personagem):
    velT = 6
    def __init__(self, surface=tuple, color=tuple, pos=list, sprites=str) -> None:
        self.togo = [None, None]
        super().__init__(surface, color, pos, sprites)
    
    def search_player(self):
        for element in self.ELEMENT_LIST:
            if element.__class__ == PersonagemGreen:
                togoX = element.pos[0]
                togoY = element.pos[1]
                togo = [togoX, togoY]
                return togo
    
    def update(self, inp, sc, ct):
        self.togo = self.search_player()
        if self.togo is None:
            return
        self.ang = math.atan2(self.togo[1] - self.pos[1], self.togo[0] - self.pos[0])
        self.velX = self.velT * math.cos(self.ang)
        self.velY = self.velT * math.sin(self.ang)
        self.lastpos = [self.pos[0], self.pos[1]]
        self.move(self.velX, self.velY)
        self.telaColision(sc)


class PersonagemYellow(Personagem):
    velT = 6
    def __init__(self, surface=tuple, color=tuple, pos=list, sprites=str) -> None:
        self.togo = [None, None]
        super().__init__(surface, color, pos, sprites)

    def search_player(self):
        for element in self.ELEMENT_LIST:
            if element.__class__ == PersonagemGreen:
                togoX = element.pos[0]
                togoY = element.pos[1]
                togo = [togoX, togoY]
                return togo

    def update(self, inp, sc, ct):
        self.togo = self.search_player()
        if self.togo is None:
            return
        self.ang = math.atan2(self.togo[1] - self.pos[1], self.togo[0] - self.pos[0])
        self.velX = self.velT * math.cos(self.ang)
        self.velY = self.velT * math.sin(self.ang)
        self.lastpos = [self.pos[0], self.pos[1]]
        self.move(self.velX, self.velY)
        self.telaColision(sc)
        

class PersonagemBlue(PersonagemYellow):
    velT = 5
    previous_run_time = -1
    now_run_time = 0
    run_cd = 1.5
    max_running_time = 0.75
    is_running = False
    def update(self, inp, sc, ct):
        super().update(inp, sc, ct)
        cd = ct - self.previous_run_time
        tr = ct - self.now_run_time
        if not(self.is_running) and cd < self.run_cd:
            return
        if not(self.is_running) and cd >= self.run_cd:
            self.run()
            self.now_run_time = ct
            return
        if self.is_running and tr <= self.max_running_time:
            return
        self.stop_running()
        self.previous_run_time = ct
        self.now_run_time = 0
    
    def run(self):
        self.velT = 10
        self.is_running = True

    def stop_running(self):
        self.velT = 5
        self.is_running = False


class PersonagemViolet(Personagem):
    velT = 6
    def __init__(self, surface=tuple, color=tuple, pos=list, sprites=str) -> None:
        self.togo = [None, None]
        super().__init__(surface, color, pos, sprites)
    
    def search_player(self):
        for element in self.ELEMENT_LIST:
            if element.__class__ == PersonagemGreen:
                togoX = element.pos[0]
                togoY = element.pos[1]
                togo = [togoX, togoY]
                break
        try:
            dist_sqr = (togo[1] - self.pos[1]) ** 2 + (togo[0] - self.pos[0]) ** 2
        except UnboundLocalError:
            return
        if math.sqrt(dist_sqr) <= 500:
            return self.pos
        return togo
    
    previous_shoot_time = -1
    shoot_cd = 0.5
    def update(self, inp, sc, ct):
        self.togo = self.search_player()
        if self.togo is None:
            return
        self.ang = math.atan2(self.togo[1] - self.pos[1], self.togo[0] - self.pos[0])
        self.velX = self.velT * math.cos(self.ang)
        self.velY = self.velT * math.sin(self.ang)
        self.lastpos = [self.pos[0], self.pos[1]]
        self.move(self.velX, self.velY)
        self.telaColision(sc)
        self.shoot_angle = self.search_target()
        cd = ct - self.previous_shoot_time
        if cd < self.shoot_cd:
            return
        self.shoot(self.shoot_angle)
        self.previous_shoot_time = ct

    def search_target(self):
        for element in self.ELEMENT_LIST:
            if element.__class__ == PersonagemGreen:
                break
        return math.atan2(element.pos[1] + element.height / 2 - self.pos[1], element.pos[0] + element.lenght / 2 - self.pos[0])

    def shoot(self, pa):
        Bala(self, pa, self.color)   


class PersonagemIndigo(PersonagemViolet):
    previous_shoot_time = -1
    macro_shoot_cd = 1.5
    shoot_cd = 0.1
    shoot_max = 4
    shoot_count = 0
    def update(self, inp, sc, ct):
        self.togo = self.search_player()
        if self.togo is None:
            return
        self.ang = math.atan2(self.togo[1] - self.pos[1], self.togo[0] - self.pos[0])
        self.velX = self.velT * math.cos(self.ang)
        self.velY = self.velT * math.sin(self.ang)
        self.lastpos = [self.pos[0], self.pos[1]]
        self.move(self.velX, self.velY)
        self.telaColision(sc)
        self.shoot_angle = self.search_target()
        cd = ct - self.previous_shoot_time
        if cd < self.shoot_cd:
            return
        if self.shoot_count > self.shoot_max:
            if cd < self.macro_shoot_cd:
                return
            self.shoot_count = 0
        self.shoot(self.shoot_angle)
        self.previous_shoot_time = ct
        self.shoot_count += 1


class Bala(Elemento):
    velT = 15
    def __init__(self, player, ang=float, color='yellow') -> None:
        self.lenght = 8
        self.height = 8
        self.surface = pg.Surface((self.lenght, self.height))
        self.color = color
        self.surface.fill(self.color)
        self.shooter = player
        self.pos = [player.pos[0], player.pos[1]]
        self.ang = ang
        self.velX = self.velT * math.cos(self.ang)
        self.velY = self.velT * math.sin(self.ang)
        self.sprite = self.surface
        self.ELEMENT_LIST.append(self)

    def update(self, inp, sc, ct):
        self.move(self.velX, self.velY)
        self.telaColision(sc)
    
    def telaColision(self, sc):
        HEIGHT = sc.get_height()
        WIDTH = sc.get_width()
        if (self.pos[0] <= 0 - self.sprite.get_width() or self.pos[0] >= WIDTH or
            self.pos[1] <= 0 - self.sprite.get_height() or self.pos[1] >= HEIGHT ):
            try:
                self.ELEMENT_LIST.remove(self)
            except ValueError:
                pass
    
    def colision(self, other, ct):
        if issubclass(other.__class__, Personagem) and self.shooter != other:
                if self.shooter.__class__ != PersonagemGreen and other.__class__ != PersonagemGreen:
                    return
                try:
                    self.ELEMENT_LIST.remove(self)
                except ValueError:
                    pass


class Estilhaco(Elemento):
    def __init__(self, element) -> None:
        posx = element.pos[0] + element.lenght / 2
        posy = element.pos[1] + element.height / 2
        self.pos = [math.ceil(posx), math.ceil(posy)]
        self.color = element.color
        self.surface = pg.Surface((6, 6))
        self.surface.fill(self.color)
        self.ang = 2 * math.pi * random.random()
        self.velT = 5 + 10 * random.random()
        self.velX = self.velT * math.cos(self.ang)
        self.velY = self.velT * math.sin(self.ang)
        self.sprite = self.surface
        Elemento.ELEMENT_LIST.append(self)

    def update(self, inp, sc, ct):
        self.move(self.velX, self.velY)
        self.telaColision(sc)
    
    def telaColision(self, sc):
        HEIGHT = sc.get_height()
        WIDTH = sc.get_width()
        if ((self.pos[0] <= 0 or self.pos[0] >= WIDTH - self.sprite.get_width()) or
            (self.pos[1] <= 0 or self.pos[1] >= HEIGHT - self.sprite.get_height())):
            try:
                self.ELEMENT_LIST.remove(self)
            except ValueError:
                pass


class EstilhacoOrange(Estilhaco):
    def __init__(self, element, player) -> None:
        super().__init__(element)
        self.lenght = 6
        self.height = 6
        self.perfect_ang = math.atan2(player.pos[1] + player.height / 2 - self.pos[1], player.pos[0] + player.lenght / 2 - self.pos[0])
        self.ang =  (random.random() - 0.5) * math.pi / 2 + self.perfect_ang
        self.velT = 5 + 10 * random.random()
        self.velX = self.velT * math.cos(self.ang)
        self.velY = self.velT * math.sin(self.ang)
    
    def colision(self, other, ct):
        if issubclass(other.__class__, Personagem):
                try:
                    self.ELEMENT_LIST.remove(self)
                except ValueError:
                    pass