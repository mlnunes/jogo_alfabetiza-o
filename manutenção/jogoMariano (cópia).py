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
        
    @property
    def position(self):
        return self.rect.centerx, self.rect.centery
       
    def collidepoint(self, (x, y)):
        if (abs (self.rect.centerx - x)) < 32 and (abs(self.rect.centery - y)) < 32:
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


def main():
    # initializes Pygame
    pygame.init()
    pygame.mixer.init()

    # creates the window and sets its properties
    pygame.display.set_caption('Jogo do Mariano')  # title
    screen = pygame.display.set_mode((900, 400))  # size

    
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
                
                
            

            # creates a clock
            clock = pygame.time.Clock()
            
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
        

    # finalizes Pygame
    pygame.quit()


if __name__ == '__main__':
    main()
