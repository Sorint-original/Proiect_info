import pygame
import os


pygame.display.set_caption("The perfect non-bugged game")

default_path = "buttons/"

currentScene = "MainMenu"
# Acum avem global latimea si inaltimea ecranului
pygame.init()
screen = pygame.display.Info()
w = screen.current_w
h = screen.current_h
del screen

def StrToBool(string):
    if string == "True":
        return True
    elif string == "False":
        return False
    else:
        return None

#Button Functions

#def Button_Press_Quit(button):
    #JocS.running = False

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
            wordList[13] = wordList[13].replace("~", " ")
            newButton = Button(wordList)
            vector.append(newButton)

def Button_Load_Bidimensional(argument, vector):
    print(vector[0][0]) #so it doesn't crash :P
    vector.clear()
    string = None
    try:
        string = argument.arg
    except:
        string = argument
    global currentScene
    currentScene = string

    for filename in os.listdir(default_path + string):
        with open(default_path + string + '/' + filename) as f:
            newVec = []
            arr = list(f)
            for elem in arr:
                wordList = elem.split()
                wordList[13] = wordList[13].replace("~", " ")
                newButton = Button(wordList)
                newVec.append(newButton)
        vector.append(newVec)
        print(vector)

def Button_No(button):
    print(None)

dispatcher = {
    #'Button_Press_Quit' : Button_Press_Quit, 
    'Button_Hover_Enable' : Button_Hover_Enable, 
    'Button_Hover_Disable' : Button_Hover_Disable, 
    'Button_Load' : Button_Load, 
    'Button_Load_Bidimensional' : Button_Load_Bidimensional,
    'Button_No' : Button_No
    }

class Button:

    def __init__(self, list):
        self.name = str(list[0])
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
            screen.blit(text, textRect)

def checkButtonClick(x, y, arg, bidimensional = [[]]):
    try:
        for buttonArg in arg:
            if x >= buttonArg.x and x <= buttonArg.x + buttonArg.width and y >= buttonArg.y and y <= buttonArg.y + buttonArg.height and buttonArg.enabled:
                try:
                    try:
                        buttonArg.onPress(buttonArg, arg)
                        break
                    except:
                        buttonArg.onPress(buttonArg, bidimensional)
                        break
                except:
                    buttonArg.onPress(buttonArg)
                    break
    except:
        if x >= arg.x and x <= arg.x + arg.width and y >= arg.y and y <= arg.y + arg.height and arg.enabled:
                arg.onPress(arg)

def checkButtonHover(x, y, arg, bidimensional = [[]]):
    try:
        for buttonArg in arg:
            if x >= buttonArg.x and x <= buttonArg.x + buttonArg.width and y >= buttonArg.y and y <= buttonArg.y + buttonArg.height and buttonArg.enabled:
                buttonArg.onHover(buttonArg)
                break
            else: 
                if buttonArg.Hovering == True:
                    buttonArg.onHoverExit(buttonArg)
                    break
    except:
        if x >= arg.x and x <= arg.x + arg.width and y >= arg.y and y <= arg.y + arg.height and arg.enabled:
                arg.onHover(arg)
        else: 
            if arg.Hovering == True:
                arg.onHoverExit(arg)

def displayButtons(screen, arg):
    try:
        for buttonArg in arg:
            buttonArg.drawButton(screen)
    except:
        arg.drawButton(screen)