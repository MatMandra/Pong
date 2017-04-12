import pygame , sys
from pygame.locals import *

# inicjacja moduły pygame
pygame.init()
# liczba klatek na sekunde
FPS = 30
# obiekt zegara, który pozwala śledzić czas i odświeżać
fpsClock = pygame.time.Clock()

# szerokość i wysokość okna gry
OKNOGRY_SZER = 800
OKNOGRY_WYS = 400

# przygotowanie powierzchni do rysowania, czyli inicjacja okna gry
OKNOGRY = pygame.display.set_mode((OKNOGRY_SZER , OKNOGRY_WYS), 0, 32)
# tytuł okna gry
pygame.display.set_caption('Prosty Pong')

# kolory wykorzystywane w grzem składowe RG zapisane w tuplach
LT_BLUE = (230, 255, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# szerokość i wysokość paletek
PALETKA_SZER = 100
PALETKA_WYS = 20

# Inicjacja PALETEK:
# utworzenie powierzchni dla obrazka, wypełnienie jej kolorem,
# pobranie prostokątnego obszaru obrazka i ustawienie go na wstępnej pozycji
PALETKA_1_POZ = (350, 360) # początkowa pozycja paletki gracza
paletka1_obr = pygame.Surface([PALETKA_SZER, PALETKA_WYS])
paletka1_obr.fill(BLUE)
paletka1_prost = paletka1_obr.get_rect()
paletka1_prost.x = PALETKA_1_POZ[0]
paletka1_prost.y = PALETKA_1_POZ[1]

PALETKA_2_POZ = (350, 20) # początkowa pozycja paletki npc
paletka2_obr = pygame.Surface([PALETKA_SZER, PALETKA_WYS])
paletka2_obr.fill(RED)
paletka2_prost = paletka2_obr.get_rect()
paletka2_prost.x = PALETKA_2_POZ[0]
paletka2_prost.y = PALETKA_2_POZ[1]

# Rysowanie komunikatów tekstowych
# Liczniki punktów, utworzenie obiektu czcioki
GRACZ_1_PKT = '0'
GRACZ_2_PKT = '0'
fontObj = pygame.font.Font('FSB.ttf', 64)
# Funkcje wyświetlające punkty gracza
def drukuj_punkty_p1():
    tekst_obr1 = fontObj.render(GRACZ_1_PKT, True, (0,0,0))
    tekst_prost1 = tekst_obr1.get_rect()
    tekst_prost1.center = (OKNOGRY_SZER/2, OKNOGRY_WYS - OKNOGRY_WYS/4)
    OKNOGRY.blit(tekst_obr1, tekst_prost1)

def drukuj_punkty_p2():
    tekst_obr2 = fontObj.render(GRACZ_2_PKT, True, (0,0,0))
    tekst_prost2 = tekst_obr2.get_rect()
    tekst_prost2.center = (OKNOGRY_SZER/2, OKNOGRY_WYS/4)
    OKNOGRY.blit(tekst_obr2, tekst_prost2)


AI_PREDKOSC = 5

# inicjacja piłki
# szerokość, wysokość prędkość pozioma(X) i pionowa (Y) piłki
# utworzenie powierzchni dla piłki, narysowanie na niej koła, ustawienie pozycji początkowej
PILKA_SZER = 20
PILKA_WYS = 20
PILKA_PREDKOSC_X = 6
PILKA_PREDKOSC_Y = 6
pilka_obr = pygame.Surface([PILKA_SZER, PILKA_WYS], pygame.SRCALPHA, 32).convert_alpha()
pygame.draw.ellipse(pilka_obr, GREEN, [0, 0, PILKA_SZER, PILKA_WYS])
pilka_prost = pilka_obr.get_rect()
pilka_prost.x = OKNOGRY_SZER/2
pilka_prost.y = OKNOGRY_WYS/2


# główna pętla gry
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEMOTION:
            myszaX, myszaY = event.pos

            przesuniecie = myszaX-(PALETKA_SZER/2)

            if przesuniecie > OKNOGRY_SZER - PALETKA_SZER:
                przesuniecie = OKNOGRY_SZER - PALETKA_SZER
            if przesuniecie < 0:
                przesuniecie = 0
            paletka1_prost.x = przesuniecie

    # AI
    if pilka_prost.centerx > paletka2_prost.centerx:
        paletka2_prost.x += AI_PREDKOSC
    elif pilka_prost.centerx < paletka2_prost.centerx:
         paletka2_prost.x -= AI_PREDKOSC

    # sprawdzaj kolizje piłki z obiektami
    if pilka_prost.right >= OKNOGRY_SZER:
        PILKA_PREDKOSC_X *= -1

    if pilka_prost.left <= 0:
        PILKA_PREDKOSC_X *= -1

    if pilka_prost.colliderect(paletka1_prost) :
        PILKA_PREDKOSC_Y *= -1
        # uwzględni nachodzenie piłki na paletkę
        pilka_prost.bottom = paletka1_prost.top

    if pilka_prost.colliderect(paletka2_prost) :
        PILKA_PREDKOSC_Y *= -1
        # uwzględni nachodzenie piłki na paletkę
        pilka_prost.top = paletka2_prost.bottom
    # Jeśli piłka dotknie top albo bottom okna gry to utaw na pozycji 0.
    if pilka_prost.top <= 0:
        pilka_prost.x = OKNOGRY_SZER/2
        pilka_prost.y = OKNOGRY_WYS/2
        GRACZ_1_PKT = str(int(GRACZ_1_PKT)+1)
    if pilka_prost.bottom >= OKNOGRY_WYS:
        pilka_prost.x = OKNOGRY_SZER/2
        pilka_prost.y = OKNOGRY_WYS/2
        GRACZ_2_PKT = str(int(GRACZ_2_PKT)+1)



    OKNOGRY.fill(LT_BLUE) # kolor okna gry
    drukuj_punkty_p1()
    drukuj_punkty_p2()
    OKNOGRY.blit(paletka1_obr, paletka1_prost)  # narysuj w oknie gry paletkę
    OKNOGRY.blit(paletka2_obr, paletka2_prost)  # narysuj paletkę NPC.
    OKNOGRY.blit(pilka_obr, pilka_prost)  # narysuj piłkę

    # przesun piłke po zdarzeniu
    pilka_prost.x += PILKA_PREDKOSC_X
    pilka_prost.y += PILKA_PREDKOSC_Y
    pygame.display.update()  # zaktualizuj okno i wyświetl
    fpsClock.tick(FPS)  # zaktualizuj zegar po narysowaniu obiektów
# KONIEC
