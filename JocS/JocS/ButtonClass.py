import pygame
import os

pygame.init()
screen = pygame.display.Info()
w = screen.current_w
h = screen.current_h
del screen

#Things for text font
vw = 0.01 * w
vh = 0.01 * h
vr = min(vw, vh)

default_path = "buttons/"

currentScene = "MainMenu"

def StrToBool(string):
    if string == "True":
        return True
    elif string == "False":
        return False
    else:
        return None

#Button Functions

def Button_Press_Quit(button):
    pygame.quit()
    os._exit(0)

def Button_Hover_Enable(button):
    button.Hovering = True

def Button_Hover_Disable(button):
    button.Hovering = False

def Button_Load(argument, vector):
    vector.clear()
    string = None
    try:
        string = argument.arg
    except:
        string = argument
    global currentScene
    currentScene = string

    with open(default_path + string + ".txt", "r") as f:
        arr = list(f)
        for elem in arr:
            wordList = elem.split()
            wordList[0] = wordList[0].replace("~", " ")
            newButton = Button(wordList)
            vector.append(newButton)

def Button_Change_Scene(button, arg):
    if type(arg) == tuple:
        func_dispatcher = {
            'Lobby' : arg[0][0]
        }
        func_dispatcher[button.arg](arg[1], arg[2], arg[3], arg[4])
    else: 
        raise Exception("Argument is not tuple")

def Button_Back(button, arg):
    if arg == None:
        raise Exception("Argument is None, so it's not ok")
    else:
        return False;

def Button_No(button):
    print(None)

def Change_MWeapon (button) :
    weapons = {'Rifle':'Shotgun' , 'Shotgun':'SMG' , 'SMG' :'Rifle'}
    button.text = weapons[button.text]

dispatcher = {
    'Button_Press_Quit' : Button_Press_Quit, 
    'Button_Hover_Enable' : Button_Hover_Enable, 
    'Button_Hover_Disable' : Button_Hover_Disable, 
    'Button_Load' : Button_Load, 
    'Button_Change_Scene' : Button_Change_Scene,
    'Button_Back' : Button_Back,
    'Button_No' : Button_No,
    'Change_MWeapon' : Change_MWeapon
    }

class Button:

    def __init__(self, list):
        self.text = str(list[0])
        self.enabled = StrToBool(str(list[1]))
        self.visible = StrToBool(str(list[2]))
        self.textVisible = StrToBool(str(list[3]))
        self.x = eval(str(list[4]))
        self.y = eval(str(list[5]))
        self.width = eval(str(list[6]))
        self.height = eval(str(list[7]))
        self.color = tuple(map(int, list[8].split(',')))
        self.hovercolor = tuple(map(int, list[9].split(',')))
        self.onPress = dispatcher[str(list[10])]
        self.onHover = dispatcher[str(list[11])]
        self.onHoverExit = dispatcher[str(list[12])]
        self.textAlignment = str(list[13]) #Aligns the text relative to button dimensions: "Center", "Left", "Right"
        self.textFont = int(list[14]) #Relative to screen dimension, NOT the actual text font
        self.textFont = int(self.textFont * vr)
        self.textColor = tuple(map(int, list[15].split(',')))
        self.textColorHover = tuple(map(int, list[16].split(',')))
        self.useTextSize = StrToBool(str(list[17])) #Use text's rectangle size for the button size if set to True 
        if self.useTextSize == True:
            font = pygame.font.Font("freesansbold.ttf", self.textFont) #font kinda hardcoded ngl
            text = font.render(self.text, True, (0, 0, 0))
            textRect = text.get_rect()
            self.width = textRect.width
            self.height = textRect.height
        #Additional argument can be specified if needed
        try:
            self.arg = str(list[18])
        except:
            self.arg = None
  
    Hovering = False

    def drawButton(self, screen):
        if self.visible == True:
            pygame.draw.rect(screen, self.hovercolor * self.Hovering or self.color, pygame.Rect(self.x, self.y, self.width, self.height))

        font = pygame.font.Font("freesansbold.ttf", self.textFont) #font kinda hardcoded ngl
        text = font.render(self.text, True, self.textColorHover * self.Hovering or self.textColor)
        textRect = text.get_rect()

        if self.textAlignment == "Center":
            textRect.center = (self.x + self.width // 2, self.y + self.height // 2)
        elif self.textAlignment == "Left":
            textRect.left = self.x
            textRect.centery = self.y + self.height // 2
        elif self.textAlignment == "Right":
            textRect.right = self.x + self.width
            textRect.centery = self.y + self.height // 2

        if self.textVisible == True:
            screen.blit(text, textRect)

def checkButtonClick(x, y, VecORButton, arg = None):
    try:
        for buttonArg in VecORButton:
            if x >= buttonArg.x and x <= buttonArg.x + buttonArg.width and y >= buttonArg.y and y <= buttonArg.y + buttonArg.height and buttonArg.enabled:
                try:
                    try:
                        buttonArg.onPress(buttonArg, VecORButton)
                    except:
                        return buttonArg.onPress(buttonArg, arg)
                except:
                    buttonArg.onPress(buttonArg)
    except:
        if x >= VecORButton.x and x <= VecORButton.x + VecORButton.width and y >= VecORButton.y and y <= VecORButton.y + VecORButton.height and VecORButton.enabled:
            try:
                VecORButton.onPress(VecORButton, arg)
            except:
                VecORButton.onPress(VecORButton)

def checkButtonHover(x, y, VecORButton):
    try:
        for buttonArg in VecORButton:
            if x >= buttonArg.x and x <= buttonArg.x + buttonArg.width and y >= buttonArg.y and y <= buttonArg.y + buttonArg.height and buttonArg.enabled:
                buttonArg.onHover(buttonArg)
                break
            else: 
                if buttonArg.Hovering == True:
                    buttonArg.onHoverExit(buttonArg)
                    break
    except:
        if x >= VecORButton.x and x <= VecORButton.x + VecORButton.width and y >= VecORButton.y and y <= VecORButton.y + VecORButton.height and VecORButton.enabled:
                VecORButton.onHover(VecORButton)
        else: 
            if VecORButton.Hovering == True:
                VecORButton.onHoverExit(VecORButton)

def displayButtons(screen, arg):
    try:
        for buttonArg in arg:
            buttonArg.drawButton(screen)
    except:
        arg.drawButton(screen)