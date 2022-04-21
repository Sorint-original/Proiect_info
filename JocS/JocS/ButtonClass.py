import pygame

import JocS

pygame.display.set_caption("The perfect non-bugged game")

ButtonVec = [];

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

def Button_Press_Quit(self):
    JocS.running = False

def Button_Hover_Enable(self):
    self.Hovering = True

def Button_Hover_Disable(self):
    self.Hovering = False

def Button_Load(self):
    global ButtonVec
    ButtonVec = [];

    string = None
    try:
        string = self.arg
    except:
        string = self

    global currentScene
    currentScene = string

    with open(default_path + string + ".txt", "r") as f:
        arr = list(f)
        for elem in arr:
            wordList = elem.split()
            wordList[13] = wordList[13].replace("~", " ")
            newButton = Button(wordList)
            ButtonVec.append(newButton)

def Button_No(self):
    print(None)

dispatcher = {
    'Button_Press_Quit' : Button_Press_Quit, 
    'Button_Hover_Enable' : Button_Hover_Enable, 
    'Button_Hover_Disable' : Button_Hover_Disable, 
    'Button_Load' : Button_Load, 
    'Button_No' : Button_No
    }

class Button:

    def __init__(self, list):
        self.name = str(list[0])
        self.enabled = StrToBool(str(list[1]))
        self.visible = StrToBool(str(list[2]))
        self.textVisible = StrToBool(str(list[3]))
        self.x = int(list[4])
        self.y = int(list[5])
        self.width = int(list[6])
        self.height = int(list[7])
        self.color = tuple(map(int, list[8].split(',')))
        self.hovercolor = tuple(map(int, list[9].split(',')))
        self.onPress = dispatcher[str(list[10])]
        self.onHover = dispatcher[str(list[11])]
        self.onHoverExit = dispatcher[str(list[12])]
        self.text = str(list[13])
        self.textFont = int(list[14])
        self.textColor = tuple(map(int, list[15].split(',')))
        self.textColorHover = tuple(map(int, list[16].split(',')))
        self.useTextSize = StrToBool(str(list[17]))
        if self.useTextSize == True:
            font = pygame.font.Font("freesansbold.ttf", self.textFont) #font kinda hardcoded ngl
            text = font.render(self.text, True, (0, 0, 0))
            textRect = text.get_rect()
            self.width = textRect.width
            self.height = textRect.height
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
        textRect.center = (self.x + self.width // 2, self.y + self.height // 2)

        if self.textVisible == True:
            JocS.WIN.blit(text, textRect)

def checkButtonClick(x, y):
    for buttonArg in ButtonVec:
        if x >= buttonArg.x and x <= buttonArg.x + buttonArg.width and y >= buttonArg.y and y <= buttonArg.y + buttonArg.height and buttonArg.enabled:
            buttonArg.onPress(buttonArg)

def checkButtonHover(x, y):
    for buttonArg in ButtonVec:
        if x >= buttonArg.x and x <= buttonArg.x + buttonArg.width and y >= buttonArg.y and y <= buttonArg.y + buttonArg.height and buttonArg.enabled:
            buttonArg.onHover(buttonArg)
        else: 
            if buttonArg.Hovering == True:
                buttonArg.onHoverExit(buttonArg)

def displayButtons(screen):
    for buttonArg in ButtonVec:
        buttonArg.drawButton(screen)