#Bibliotecas
from audioplayer import AudioPlayer
from os import listdir
from os.path import isfile, join
import audioread
import pygame
from time import time

path = '/home/joao/Música/'
files = [f for f in listdir(path) if isfile(join(path, f))]
Musicas = []
Music_duration = []

for i in files:
    music_ext = (i.split("."))[1]
    if music_ext == 'mp3':
        Musicas.append(i)
        with audioread.audio_open(str(path + i)) as sound:
            Music_duration.append(sound.duration)

dimensoes = (700,700)

pygame.init()
pygame.display.set_caption("Media Player")

fonte = pygame.font.SysFont("hack", 32)
tela = pygame.display.set_mode((dimensoes))




#Variáveis
backgorundcolor = (120,120,120)
toplay = False
ismuted = False
isplaying = False
volume = 40

#Imagens
play = pygame.image.load("/home/joao/Arquivos/media_player/files/play.png")
pause = pygame.image.load("/home/joao/Arquivos/media_player/files/pause.png")
up_volume = pygame.image.load("/home/joao/Arquivos/media_player/files/add.png")
down_volume = pygame.image.load("/home/joao/Arquivos/media_player/files/remove.png")
umute = pygame.image.load("/home/joao/Arquivos/media_player/files/umute.png")
mute = pygame.image.load("/home/joao/Arquivos/media_player/files/mute.png")
next = pygame.image.load("/home/joao/Arquivos/media_player/files/next.png")
back = pygame.image.load("/home/joao/Arquivos/media_player/files/back.png")

tela.fill(backgorundcolor)

y = 53
d_x = []
d_y = []

for i in Musicas:
    pygame.draw.rect(tela, (255,255,255), [10,y,680,32])
    tela.blit(play,[643,y])
    d_x.append(str('643'+':'+'675'))
    d_y.append(str(y)+':'+str(y+32))
    music_name = i
    text_name = fonte.render(music_name,True,(0,0,0))
    tela.blit(text_name,[10,y+5])
    y += 47   

def comandos(mouse, index, volume, ismuted, isplaying):
    play = False
    for event in pygame.event.get():
        #Sair
        if event.type == pygame.QUIT:
            raise Exception
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(Musicas)):
                dx = str(d_x[i]).split(':')
                dx1 = int(dx[0])
                dx2 = int(dx[1])

                dy = str(d_y[i]).split(':')
                dy1 = int(dy[0])
                dy2 = int(dy[1])
                
                if dx1 <= mouse[0] <= dx2 and dy1 <= mouse[1] <= dy2:
                    index = i
                    play = True

            # Back and Next
            if 147 <= mouse[0] <= 179 and 3 <= mouse[1] <= 35:
                index -= 1
                play = True
            if 204 <= mouse[0] <= 236 and 3 <= mouse[1] <= 35:
                index += 1
                play = True

            # UP_Volume / Down_Volume
            if 513 <= mouse[0] <= 545 and 3 <= mouse[1] <= 35:
                volume -= 10
            if 456 <= mouse[0] <= 488 and 3 <= mouse[1] <= 35:
                volume += 10
            
            #Mute / Unmute
            if 663 <= mouse[0] <= 695 and 3 <= mouse[1] <= 35:
                if ismuted == True:
                    ismuted = False
                else:
                    ismuted = True
            
            # Play / Pause
            if 15 <= mouse[0] <= 47 and 3 <= mouse[1] <= 35:
                if isplaying == True:
                    isplaying = False
                else:
                    isplaying = True

    return index, play, volume, ismuted, isplaying

def get_time():
    tempo = time.time()
    return tempo

player = AudioPlayer('')

def play_music(index, toplay,player,volume,ismuted):
    if toplay == True:
        player = AudioPlayer('/home/joao/Música/'+Musicas[index])
        player.play()

    if ismuted == False:
        player.volume = volume
    else:
        player.volume = 0
    return player

def desenhar_tela(isplaying,ismuted):
    pygame.draw.rect(tela, (140,0,0), [0,0,700,38])

    # Mute / Umute
    if ismuted == True:
        tela.blit(umute,(663,3))
    else:
        tela.blit(mute,(663,3))

    # Play / Pause
    if isplaying == True:
        tela.blit(pause,(15,3))
    else:
        tela.blit(play,(15,3))

    # Up / Down
    tela.blit(down_volume,(513,3))
    tela.blit(up_volume,(456,3))

    # Next / Back
    tela.blit(back,(147,3))
    tela.blit(next,(204,3))


index = ''
while True:
    mouse = pygame.mouse.get_pos()
    index,toplay,volume,ismuted,isplaying = comandos(mouse,index,volume,ismuted,isplaying)
    player = play_music(index,toplay, player,volume,ismuted)
    desenhar_tela(isplaying,ismuted)
    pygame.display.update()