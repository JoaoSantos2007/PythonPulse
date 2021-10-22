from audioplayer import AudioPlayer
from os import listdir
from os.path import isfile, join
import audioread
import pygame

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

print(Musicas)
print(Music_duration)

dimensoes = (900,900)

backgorundcolor = (120,120,120)

pygame.init()
pygame.display.set_caption("Media Player")

fonte = pygame.font.SysFont("hack", 32)
tela = pygame.display.set_mode((dimensoes))


#Imagens
play = pygame.image.load("/home/joao/Arquivos/media_player/files/play.png")

tela.fill(backgorundcolor)
pygame.draw.rect(tela, (140,0,0), [0,0,900,38])

y = 53

for i in Musicas:
    pygame.draw.rect(tela, (255,255,255), [10,y,880,32])
    tela.blit(play,[843,y])
    music_name = i
    text_name = fonte.render(music_name,True,(0,0,0))
    tela.blit(text_name,[10,y+5])
    y += 47   



pygame.display.update()
player = AudioPlayer("/home/joao/Música/For Me.mp3")#.play()#(block=True)
player.play()
input()