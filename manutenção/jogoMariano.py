#!/usr/bin/python


# imports the Pygame library
import pygame
import os
import random


# colors
background_color = (0, 100, 50)
answer_area_color = (255, 225, 255)
circle_color = (90, 210, 140)
rectangle_color = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = ( 255, 30, 30)

pygame.font.init()
fonte=pygame.font.get_default_font()
fontesys=pygame.font.SysFont(fonte, 40)


class Circle(object):
    def __init__(self, (x, y), radius):
        self.x = x
        self.y = y
        self.radius = radius

    @property
    def position(self):
        return self.x, self.y

    def move_ip(self, (dx, dy)):
        self.x += dx
        self.y += dy

    def collidepoint(self, (x, y)):
        """
        Circle-point collision.
        """
        if (self.x - x) ** 2 + (self.y - y) ** 2 <= self.radius ** 2:
            return True
        return False

    def draw(self, surface):
        pygame.draw.circle(surface, circle_color, self.position, self.radius)


class Letra(pygame.sprite.Sprite):
    def __init__(self, startpos, imagem):
        pygame.sprite.Sprite.__init__(self)
        self.path = './letras/'
        self.name = imagem
        self.image, self.rect = load_image(self.path, imagem)
        self.rect.centerx = startpos[0]
        self.rect.centery = startpos[1]
        self.x_origin = startpos[0]
        self.y_origin = startpos[1]
        self.solved = False
        
    @property
    def position(self):
        return self.rect.centerx, self.rect.centery

    def move_ip(self, (dx, dy)):
        self.rect.centerx += dx
        self.rect.centery += dy
        
    def collidepoint(self, (x, y)):
        #if (self.rect.centerx - x) ** 2 + (self.rect.centery - y) ** 2 <= 150:
        if (abs (self.rect.centerx - x)) < 35 and (abs(self.rect.centery - y)) < 35:
            return True
        return False
        
    def return_origin(self):
        self.rect.centerx = self.x_origin
        self.rect.centery = self.y_origin
        

class Botao(pygame.sprite.Sprite):
    def __init__(self, startpos, imagem):
        pygame.sprite.Sprite.__init__(self)
        self.path = './app/'
        self.image, self.rect = load_image(self.path, imagem)
        self.rect.centerx = startpos[0]
        self.rect.centery = startpos[1]
        
    #@property
    def position(self):
        return self.rect.centerx, self.rect.centery
       
    def collidepoint(self, (x, y)):
        if (abs (self.rect.centerx - x)) < 32 and (abs(self.rect.centery - y)) < 32:
            return True
        return False

class Texto(pygame.sprite.Sprite):
    def __init__(self, startpos, nome):
        pygame.sprite.Sprite.__init__(self)
        self.texto= fontesys.render( nome.upper(), 1, WHITE )
        self.rect = pygame.Rect(startpos[0], startpos[1], 60, 40)
        self.rect.centerx = startpos[0] + 60
        self.rect.centery = startpos[1] + 20
         
        
    @property
    def position(self):
        return self.rect.centerx, self.rect.centery
       
    def collidepoint(self, (x, y)):
        if (abs (self.rect.centerx - x)) < 60 and (abs(self.rect.centery - y)) < 25:
            return True
        return False


class Som_obj(pygame.sprite.Sprite):
    def __init__(self, startpos, nome):
        pygame.sprite.Sprite.__init__(self)
        self.img_path = './figs/'
        self.snd_path = './sons/'
        self.nome = nome
        self.image, self.rect = load_image(self.img_path, nome)
        self.image = pygame.transform.scale(self.image, (100,100))
        self.rect = self.image.get_rect()
        self.rect.centerx = startpos[0]
        self.rect.centery = startpos[1]
        
    @property
    def position(self):
        return self.rect.centerx, self.rect.centery
       
    def collidepoint(self, (x, y)):
        if (abs (self.rect.centerx - x)) < 50 and (abs(self.rect.centery - y)) < 50:
            return True
        return False

 
class Rectangle(pygame.Rect):
    def __init__(self, (x, y), (width, height)):
        super(Rectangle, self).__init__(x, y, width, height)

    def draw(self, surface):
        pygame.draw.rect(surface, rectangle_color, self)
      
        
def load_image(path, name):
    """carrega uma imagem na memoria"""
    fullname = os.path.join(path + name+'.png')
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print "Cannot load image:", fullname
        raise SystemExit, message
    return image, image.get_rect()
   
    
def jogo_organiza(screen, clock):
    #carrega imagens
    arquivos_imagens = os.listdir('./figs')
    arquivos_imagens = random.sample(arquivos_imagens, len(arquivos_imagens))
    
    image_paths = {}
    imagens = {}
    for i in arquivos_imagens:
        i0 = i.split('.')[0]
        if len(i0) == 4:
            image_path = os.path.join('./figs/' + i)
            image_paths.update ( {i0 : image_path})
            imagens.update({i0 : pygame.image.load(image_path).convert_alpha()})
            
    botao_proximo = Botao((632,302) , 'proximo' )
    sair = False

    for indice in range(len(imagens)):
        avanca = False
        while avanca == False:
            resposta =  list(imagens.keys()[indice])
            formas_respostas = {}
            
            for i, resp in enumerate(resposta):
                formas_respostas.update({ (str(i) + '-' + resp) :Rectangle((390+(i*130), 150), (97, 100))})
                
            
            letras_path = {}
            
            for i, resp in enumerate(resposta):
                letras_path.update({ (str(i) + '-' + resp) : os.path.join('./letras/'+resp+'.png')})    
            
            imagens_letras = {}
            
            #for i, resp in enumerate(resposta):
            #    imagens_letras.update({ (str(i) + '-' + resp) : pygame.image.load(letras_path[(str(i) + '-' + resp)]).convert_alpha()})  
            
            
            letras_embaralhadas = []
            for i, resp in enumerate(resposta):
                letras_embaralhadas.append(resp+str(i))
                
            letras_embaralhadas = random.sample(letras_embaralhadas, len(letras_embaralhadas))
                
            for i, ltr in enumerate(letras_embaralhadas):
                globals()[ltr] =  Letra((80+(i*70),320) , ltr[0])
            
            # current selection
            current_selection = None

            # is running?
            running = True
            
            music = False
            
            acertou = False

            # main loop (it handles events)
            while running:
                # gets all events from the event queue
                for event in pygame.event.get():
                    # 'QUIT' event
                    if event.type == pygame.QUIT:
                        # stops the loop when the CLOSE button is clicked
                        running = False
                        avanca = True
                        sair = True

                    # 'MOUSEBUTTONDOWN' event
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # press the left mouse button on a shape to set the current selection
                        if event.button == 1:
                            #for shape in letras():#shapes:
                            for i, resp in enumerate(resposta):
                                if globals()[resp+str(i)].collidepoint(event.pos):
                                    current_selection = globals()[resp+str(i)]
                                    break  # only the first shape
                                    
                            if botao_proximo.collidepoint(event.pos):
                                if acertou == True:
                                    avanca = True
                                    running = False
                                                           

                    # 'MOUSEBUTTONUP' event
                    if event.type == pygame.MOUSEBUTTONUP:
                        # release the left mouse button to remove the current selection
                        if event.button == 1:
                            if current_selection != None:
                                letra_fora = True
                                for pos in formas_respostas.keys():
                                    if (event.pos[0] > formas_respostas[pos].x) and  (event.pos[0] < (formas_respostas[pos].x + formas_respostas[pos].width)):
                                        if (event.pos[1] > formas_respostas[pos].y) and  (event.pos[1] < (formas_respostas[pos].y + formas_respostas[pos].height)):
                                            if current_selection.name == (list(pos)[-1]):
                                                if not(current_selection.solved):
                                                    current_selection.solved = True
                                                    current_selection.rect.centerx = formas_respostas[pos].x + formas_respostas[pos].width/2
                                                    current_selection.rect.centery = formas_respostas[pos].y + formas_respostas[pos].height/2
                                                    letra_fora = False
                                                    break
                                        else:
                                            current_selection.return_origin()
                                    else:

                                        current_selection.return_origin()

         
                                if letra_fora:
                                    pygame.mixer.music.load('./app/buzina.mp3')
                                    pygame.mixer.music.play()
                                    pygame.event.wait()
                                current_selection = None
                            

                    # 'MOUSEMOTION' event
                    if event.type == pygame.MOUSEMOTION:
                        # move the mouse by pressing its left button to move the current selection
                        if event.buttons[0] == 1:
                            if current_selection:
                                current_selection.move_ip(event.rel)

                # sets the background color
                screen.fill(background_color)
                
                
                screen.blit(pygame.transform.scale(imagens[imagens.keys()[indice]], (250,250)), (70,30))
                
                for forma in formas_respostas.keys():
                    formas_respostas[forma].draw(screen) 
         
                    
                for ltr in letras_embaralhadas:
                    screen.blit(globals()[ltr].image, globals()[ltr].rect)     
                
                
                test_fim = 0
                for i, resp in enumerate(resposta):
                    if globals()[resp + str(i)].solved:
                        test_fim += 1
                if test_fim == len(resposta):
                    screen.blit(pygame.image.load('./app/parabens.png'), (200,50))
                    acertou = True
                    screen.blit(botao_proximo.image, botao_proximo.rect)
                    

                    if music == False:
                        pygame.mixer.music.load('./app/aplauso.mp3')
                        pygame.mixer.music.play()
                        pygame.event.wait()   
                        music = True
                        avanca = True

                # draws the shapes
                #for shape in reversed(shapes):
                #    shape.draw(screen)

                # updates the screen
                pygame.display.flip()

                # limits the updates up to 40 FPS (frames per second)
                clock.tick(40)
        if sair:
            return True          
    return True     


def jogo_sons(screen, clock):

    mouse_position = (0, 0)
    drawing = False
    screen.fill(background_color)
    botao_proximo = Botao((632,302) , 'proximo' )
    arquivos_sons = os.listdir('./sons')
    
    sons = {}
    
    for i in arquivos_sons:
        i0 = i.split('.')[0]
        sons.update ( {i0 : Som_obj((0,0), i0)})

    nome_som = {}
    sons_3 = random.sample(sons.keys(), 3)
    for idx, i in enumerate(random.sample(sons_3, 3)):
        nome_som.update({ i : Texto((600, 80+idx*120), i)})
        
    last_pos = None
    running = True
    correto = False
    sair = False
    music = False
    init_pos = 0
    current_selection = None
    ligados = {}
    audio = False
    lig = 0
    



    for idx, i in enumerate(sons_3):
        sons[i].rect.centerx, sons[i].rect.centery = 120, (80+(idx*120))
    


    while (running):
        while not(sair):
            if not drawing:
                screen.fill(background_color)
                for i in sons_3:
                    screen.blit(sons[i].image, sons[i].rect)
                    screen.blit(nome_som[i].texto, nome_som[i])
                for i in ligados:
                    pygame.draw.line(screen, RED, ligados[i][0], ligados[i][1], 3)
            
            if not(audio):
                pygame.mixer.music.load(sons[sons_3[lig]].snd_path + sons[sons_3[lig]].nome+'.mp3')
                pygame.mixer.music.play()
                pygame.event.wait()
                audio = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sair = True

                elif event.type == pygame.MOUSEMOTION:
                    if (drawing):
                        mouse_position = pygame.mouse.get_pos()
                        screen.fill(background_color)
                        for i in sons_3:
                            screen.blit(sons[i].image, sons[i].rect)
                            screen.blit(nome_som[i].texto, nome_som[i])
                        for i in ligados:
                            pygame.draw.line(screen, RED, ligados[i][0], ligados[i][1], 3)
                        pygame.draw.line(screen, YELLOW, init_pos, mouse_position, 3)
                        
                        #if last_pos is not None:
                        #    pygame.draw.line(screen, WHITE, last_pos, mouse_position, 3)
                        #last_pos = mouse_position
                elif event.type == pygame.MOUSEBUTTONUP:
                    if (drawing):
                        for i in nome_som:
                            if nome_som[i].collidepoint(event.pos):
                                if current_selection.nome == i:
                                    ligados.update({ i : [init_pos, (nome_som[i].rect.centerx - 35, nome_som[i].rect.centery - 15)]})
                                    audio = False
                                else:
                                    pygame.mixer.music.load('./app/buzina.mp3')
                                    pygame.mixer.music.play()
                                    pygame.event.wait()

                    mouse_position = (0, 0)
                    drawing = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i in sons_3:
                        if sons[i].collidepoint(event.pos):
                            if sons[i].nome == sons_3[lig]:
                                current_selection = sons[i]
                                drawing = True
                                init_pos = current_selection.rect.centerx + 48, current_selection.rect.centery
                                
                            else:
                                pygame.mixer.music.load('./app/buzina.mp3')
                                pygame.mixer.music.play()
                                pygame.event.wait()
            clock.tick(40)
            pygame.display.update()
            lig = len(ligados)
            if lig > 2:
                sair = True
                correto = True

                
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_proximo.collidepoint(event.pos):
                    running = False
        if (correto):
            screen.blit(pygame.image.load('./app/parabens.png'), (200,50))
            screen.blit(botao_proximo.image, botao_proximo.rect)
            if music == False:
                pygame.mixer.music.load('./app/aplauso.mp3')
                pygame.mixer.music.play()
                pygame.event.wait()   
                music = True
        clock.tick(40)
        pygame.display.update()
    return True    


def main():
    # initializes Pygame
    pygame.init()
    pygame.mixer.init()

    clock = pygame.time.Clock()

    # creates the window and sets its properties
    pygame.display.set_caption('Jogo do Mariano')  # title
    screen = pygame.display.set_mode((900, 400))  # size
    
    botao_jogo_organiza = Botao((300,200) , 'organiza' )
    txt_organiza = fontesys.render('Forma palavras', 1, (255,255,255))
    
    botao_jogo_sons = Botao((600,200) , 'sons' )
    txt_sons = fontesys.render('Descubra o som', 1, (255,255,255))
    
    main_screen = True
    running = True
    while running:
        screen.fill(background_color)
        for event in pygame.event.get():
            # 'QUIT' event
            if event.type == pygame.QUIT:
                # stops the loop when the CLOSE button is clicked
                running = False

            # 'MOUSEBUTTONDOWN' event
            if event.type == pygame.MOUSEBUTTONDOWN:
                # press the left mouse button on a shape to set the current selection
                if event.button == 1:
                    #for shape in letras():#shapes:
                    if main_screen == True:
                        if botao_jogo_organiza.collidepoint(event.pos):
                            main_screen = False
                            main_screen = jogo_organiza(screen, clock)
                        
                        if botao_jogo_sons.collidepoint(event.pos):
                            main_screen = False
                            main_screen = jogo_sons(screen, clock)


        screen.blit(botao_jogo_organiza.image, botao_jogo_organiza.rect)
        screen.blit(txt_organiza,(200, 250))
        screen.blit(botao_jogo_sons.image, botao_jogo_sons.rect)
        screen.blit(txt_sons,(490, 250))
        
        pygame.display.flip()
    
    # finalizes Pygame
    pygame.quit()


if __name__ == '__main__':
    main()
