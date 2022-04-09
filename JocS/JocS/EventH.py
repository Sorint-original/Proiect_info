import pygame
import os



def exit(event) :
    if event.type == pygame.QUIT :
        pygame.quit()
        os._exit(0)

#Nu functioneaza cum ar trebui 
def controller_verify(event,joysticks) :
    if event.type == pygame.JOYDEVICEADDED :
        joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    elif event.type == pygame.JOYDEVICEREMOVED :
        joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
