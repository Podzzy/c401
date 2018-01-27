import random, pygame, sys
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
REVEALSPEED = 8 #how fast cards are revealed
BOXSIZE = 40 #size of cards
GAPSIZE = 10 #gaps between columes and rows
BOARDWIDTH = 4 #columns
BOARDHEIGHT = 4 #rows
tries = 0
assert(BOARDWIDTH * BOARDHEIGHT) % 2 == 0, "Board needs to have even number of matches"
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

#           R   G   B
GRAY     = (100,100,100)
NAVYBLUE = (60,60,100)
WHITE    = (255,255,255)
RED      = (255,0,0)
GREEN    = (0,255,0)
BLUE     = (0,0,255)
YELLOW   = (0,255,255)
ORANGE   = (255,128,0)
PURPLE   = (255, 0, 255)
CYAN     = (0,255,255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE
TEXTCOLOR = CYAN

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'
PLUS = 'plus'

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL, PLUS)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined."

def main():
    global FPSCLOCK, DISPLAYSURF, tries, TEXTCOLOR, BGCOLOR, topText
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("tetrisb.mid")
    pygame.mixer.music.play(-1,0.0)
    myFont = pygame.font.SysFont("monospace",40)
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0 #used for mouse position
    mousey = 0 #used for y mouse position
    pygame.display.set_caption('Memory Game')
    topText = myFont.render("Made by Seth", 1,TEXTCOLOR)

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None #Stores x and y first box clicked

    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainBoard)

    while True: #main game loop
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)

        mouseClicked = False
        topText = myFont.render("MEMORY GAME",1,TEXTCOLOR)
        DISPLAYSURF.fill(BGCOLOR)                 
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey)

        #Redraw the screen and wait a clock tick
        pygame.display.update()
        FPSCLOCK.tick(FPS)

        
def revealBoxesAnimation(board, boxesToReveal):
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)        


def coverBoxesAnimation(board, boxesToCover):
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage)

                        
                          

def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25)
    half = int(BOXSIZE * 0.5)

    left, top = leftTopCoordsOfBox(boxx, boxy) #get pixel coords from the board

    #Draw the shapes
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half),(left + half, top + BOXSIZE - 1),(left, top + half)))

    elif shape == PLUS:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top, half, BOXSIZE))
        pygame.draw.rect(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i),(left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE -1), (left + BOXSIZE -1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))




            
    
def drawBoxCovers(board, boxes, coverage):
    #Draws boxes being covered/revealed. "boxes" is a list.
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])

        if coverage > 0: #only draw the cover if there is a coverage
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))

    pygame.display.update()
    FPSCLOCK.tick(FPS)
                            
        
        
                         


                
def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return(boxx ,boxy)
            
    return(None, None)





def getShapeAndColor(board, boxx, boxy):
    #Shape value for x,y spot is stored in board [x][y][0]
    #Color value for x,y spot is stored in board [x][y][1]
    return board[boxx][boxy][0], board[boxx][boxy][1]


                

def leftTopCoordsOfBox(boxx, boxy):
    #Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return(left, top)


def drawBoard(board, revealed):
    DISPLAYSURF.blit(topText, (90,-8))
    #Draws all boxes in their covered or revealed state
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                #Draw covered box.
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE,BOXSIZE))
            else:
                #Draw the revealed icon
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)
    




def splitIntoGroupsOf(groupSize, theList):
    #split a list into smaller lists that have at most groupSize number of items
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])

        return result


def startGameAnimation(board):
    #randomly reveal boxes 4 at a time.
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range (BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append( (x, y) )

    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(4, boxes)

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)
        
    
    



def generateRevealedBoxesData(val):
    revealedBoxes = []

    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes


def getRandomizedBoard():
    #get a list of every possible shape/color combo
    icons = []

    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append( (shape, color) )

    random.shuffle(icons) #randomize the order of the icons list.
    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2) # calculate how many icons needed
    icons = icons[:numIconsUsed] * 2
    random.shuffle(icons)

    #Create the board structure with randomly placed icons
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range (BOARDHEIGHT):
            column.append(icons[0])
            del icons[0] #After assigning icon to the column, delete it
        board.append(column)
        
    return board
        
    

if __name__== '__main__':
    main()

















    




    









    
