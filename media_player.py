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

#Variáveis
backgorundcolor = (120,120,120)
toplay = False
ismuted = False
isplaying = False
torepeat = False
init_music = False
ispause = False
temp_pause = 0
temp_pause_tot = 0
volume = 40
index = ''
y = 53
d_x = []
d_y = []
dimensoes = (700,700)
player = AudioPlayer('')

pygame.init()
pygame.display.set_caption("Media Player")

fonte = pygame.font.SysFont("hack", 32)
tela = pygame.display.set_mode((dimensoes))
tela.fill(backgorundcolor)

#Imagens
play = pygame.image.load("/home/joao/Arquivos/media_player/files/play.png")
pause = pygame.image.load("/home/joao/Arquivos/media_player/files/pause.png")
up_volume = pygame.image.load("/home/joao/Arquivos/media_player/files/add.png")
down_volume = pygame.image.load("/home/joao/Arquivos/media_player/files/remove.png")
umute = pygame.image.load("/home/joao/Arquivos/media_player/files/umute.png")
mute = pygame.image.load("/home/joao/Arquivos/media_player/files/mute.png")
next = pygame.image.load("/home/joao/Arquivos/media_player/files/next.png")
back = pygame.image.load("/home/joao/Arquivos/media_player/files/back.png")
repeat = pygame.image.load("/home/joao/Arquivos/media_player/files/repeat.png")
go = pygame.image.load("/home/joao/Arquivos/media_player/files/continue.png")

#Desenhar Músicas
for i in Musicas:
    pygame.draw.rect(tela, (255,255,255), [10,y,680,32])
    tela.blit(play,[643,y])
    d_x.append(str('643'+':'+'675'))
    d_y.append(str(y)+':'+str(y+32))
    music_name = i
    text_name = fonte.render(music_name,True,(0,0,0))
    tela.blit(text_name,[10,y+5])
    y += 47   

#Executar comandos
def comandos(mouse, index, volume, ismuted, isplaying,torepeat,toplay):
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
                    toplay = True

            # Back and Next
            if 147 <= mouse[0] <= 179 and 3 <= mouse[1] <= 35:
                index -= 1
                toplay = True
            if 204 <= mouse[0] <= 236 and 3 <= mouse[1] <= 35:
                index += 1
                toplay = True

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

            # Repeat / Continue
            if 325 <= mouse[0] <= 357 and 3 <= mouse[1] <= 35:
                if torepeat == True:
                    torepeat = False
                else:
                    torepeat = True

    return index, toplay, volume, ismuted, isplaying,torepeat

#Desenhar APP BAR
def desenhar_tela(isplaying,ismuted,torepeat):
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

    # Repeat / Continue
    if torepeat == False:
        tela.blit(repeat,(325,3))
    else:
        tela.blit(go,(325,3))

#Tempo atual
def tempo():
    timestamp = int(round(time() * 1))
    return timestamp

tempo_init = 0

#Tocar Músicas
def play_music(index, toplay,player,volume,ismuted,torepeat,tempo_init,init_music,isplaying):
    if toplay == True:
        player = AudioPlayer('/home/joao/Música/'+Musicas[index])
        player.play()
        tempo_init = tempo()
        init_music = True
        isplaying = True
        toplay = False

    if init_music == True and ispause == False:
        if tempo() - tempo_init - temp_pause_tot >= Music_duration[index]:
            if torepeat == True:
                toplay = True
            else:
                index = index + 1
                toplay = True
            

    if ismuted == False:
        player.volume = volume
    else:
        player.volume = 0
    return player, tempo_init, init_music, toplay, index,isplaying

while True:
    mouse = pygame.mouse.get_pos()
    index,toplay,volume,ismuted,isplaying,torepeat = comandos(mouse,index,volume,ismuted,isplaying,torepeat,toplay)
    player,tempo_init, init_music, toplay, index, isplaying = play_music(index,toplay, player,volume,ismuted,torepeat,tempo_init,init_music,isplaying)
    if isplaying == False and init_music == True:
        if once_time == True:
            time_init_pause = tempo()
            once_time = False
        temp_pause = tempo() - time_init_pause 
        ispause = True
        player.pause()  
    elif isplaying == True and init_music == False:
        index = 0
        toplay = True     
    else:
        if ispause == True:
            temp_pause_tot += temp_pause
            ispause = False
            player.resume()
        once_time = True
                
    desenhar_tela(isplaying,ismuted,torepeat)
    pygame.display.update()
