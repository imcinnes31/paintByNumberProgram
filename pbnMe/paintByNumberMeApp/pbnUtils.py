from asyncio.windows_events import NULL
from pickle import TRUE
from PIL import Image
from pathlib import Path

import os

def convert(pictureFile):

    # 1 to 100
    difficultyChoice = 100
    difficulty = ((105 - difficultyChoice) / 5)**3

    fileName = pictureFile.replace('/media','media')
    fileName2 = fileName.replace('.jpg','')
    openedFile = fileName2.replace('/', '/result') + '1.png'
    renderedFile = fileName2.replace('/', '/result') + '2.png'
    outlinedFile = fileName2.replace('/', '/result') + '3.png'
    altrenderedFile = fileName2.replace('/', '/result') + '4.png'
    altoutlinedFile = fileName2.replace('/', '/result') + '5.png'

    im = Image.open(fileName)

    #resize image
    xSize = im.size[0]
    ySize = im.size[1]
    if xSize > 1000 or ySize > 1000:  #orig 1000
        print('resizing image...')
        if xSize >= ySize:
            newXSize = 1000 / xSize * xSize
            newYSize = 1000 / xSize * ySize
        else:
            newXSize = 1000 / ySize * xSize
            newYSize = 1000 / ySize * ySize
        newsize = (int(newXSize), int(newYSize))
        im = im.resize(newsize)
    xSize = im.size[0]
    ySize = im.size[1]
    pix = im.load()

    colorList = []
    colorListOrig = set()
    imageStatus = [[0 for x in range(ySize)] for y in range(xSize)] 

    #rerender picture based on number of original colors
    for x in range(0,xSize):
        for y in range(0,ySize):
            colorListOrig.add(pix[x,y])
    print(len(colorListOrig))

    if len(colorListOrig) > 280000:
        depthFactor = 40 #orig 40
        darkFactor = 35 #orig 50
    elif len(colorListOrig) > 200000:
        depthFactor = 40 #orig 40
        darkFactor = 35 #orig 50
    elif len(colorListOrig) > 160000:
        depthFactor = 30 #orig 40
        darkFactor = 35 #orig 50        
    elif len(colorListOrig) > 60000:
        depthFactor = 25 #orig 40
        darkFactor = 35 #orig 50
    else:
        depthFactor = 20 #orig 40
        darkFactor = 30 #orig 50


    cutFactor = 15 #orig 15
    signDiff = 100 #orig 100

    for x in range(0,xSize):
        for y in range(0,ySize):
            red = int((pix[x,y][0] - cutFactor) / depthFactor) * depthFactor + cutFactor
            green = int((pix[x,y][1] - cutFactor) / depthFactor) * depthFactor + cutFactor
            blue = int((pix[x,y][2] - cutFactor) / depthFactor) * depthFactor + cutFactor
            if red < darkFactor:
                red = 0
            if green < darkFactor:
                green = 0
            if blue < darkFactor:
                blue = 0
            pix[x,y] = (red,green,blue)
            if pix[x,y] not in colorList:
                colorList.append(pix[x,y])

    im.save(openedFile)

    # get rid of pixel squares
    if difficultyChoice >= 60:
        maxFactor = 4
    elif difficultyChoice >= 30:
        maxFactor = 5
    else:
        maxFactor = 6

    for redo in range(1,2):

        for factor in range(1,maxFactor):

            print('getting rid of ' + str(factor) + ' size pixels...')
            for x in range(0,xSize):
                for y in range(0,ySize):

                    orig = pix[x,y]

                    if y == 0:
                        v1 = pix[x,y+factor]
                    else:
                        v1 = pix[x,y-1]

                    if ySize - y <= factor:
                        v2 = pix[x,y-1]
                    else:
                        v2 = pix[x,y+factor]

                    v1Diff = abs(v1[0]-orig[0]) + abs(v1[1]-orig[1]) + abs(v1[2]-orig[2])
                    v2Diff = abs(v2[0]-orig[0]) + abs(v2[1]-orig[1]) + abs(v2[2]-orig[2])

                    if orig != v1 and orig != v2:
                        # is it grey?
                        if orig[0] == orig[1] == orig[2]:
                            imageStatus[x][y] = 'outline'
                        else:
                            # is it significantly different than the other two?
                            if v1Diff > signDiff and v2Diff > signDiff:
                                greyColor = int((orig[0] + orig[1] + orig[2])/3)
                                if greyColor != 255:
                                    greyColor = int((greyColor - 8) / 10) * 10 + 8
                                pix[x,y] = (greyColor,greyColor,greyColor)
                                imageStatus[x][y] = 'outline'
                            else:
                                if v1Diff <= v2Diff:
                                    orig = v1
                                    pix[x,y] = v1
                                else:
                                    orig = v2
                                    pix[x,y] = v2
    #
            for x in range(0,xSize):
                for y in range(0,ySize):

                    orig = pix[x,y]

                    if y == 0:
                        v1 = pix[x,y+factor]
                    else:
                        v1 = pix[x,y-1]

                    if ySize - y <= factor:
                        v2 = pix[x,y-1]
                    else:
                        v2 = pix[x,y+factor]

                    if x == 0:
                        h1 = pix[x+factor,y]
                    else:
                        h1 = pix[x-1,y]

                    if xSize - x <= factor:
                        h2 = pix[x-1,y]
                    else:
                        h2 = pix[x+factor,y]

                    h1Diff = abs(h1[0]-orig[0]) + abs(h1[1]-orig[1]) + abs(h1[2]-orig[2])
                    h2Diff = abs(h2[0]-orig[0]) + abs(h2[1]-orig[1]) + abs(h2[2]-orig[2])

                    if orig != h1 and orig != h2:
                        # is it grey?
                        if orig[0] == orig[1] == orig[2]:
                            imageStatus[x][y] = 'outline'
                        else:
                            # is it significantly different than the other two?
                            if h1Diff > signDiff and h2Diff > signDiff:
                                greyColor = int((orig[0] + orig[1] + orig[2])/3)
                                if greyColor != 255:
                                    greyColor = int((greyColor - 8) / 10) * 10 + 8
                                pix[x,y] = (greyColor,greyColor,greyColor)
                                imageStatus[x][y] = 'outline'
                            else:
                                if h1Diff <= h2Diff:
                                    orig = h1
                                    pix[x,y] = h1
                                else:
                                    orig = h2
                                    pix[x,y] = h2

            for x in range(0,xSize):
                for y in range(0,ySize):
                    orig = pix[x,y]

                    if x == 0:
                        h1 = pix[x+factor,y]
                    else:
                        h1 = pix[x-1,y]

                    if xSize - x <= factor:
                        h2 = pix[x-1,y]
                    else:
                        h2 = pix[x+factor,y]

        for x in range(0,xSize):
            for y in range(0,ySize):

                orig = pix[x,y]

                if x == 0:
                    h1 = pix[x+factor,y]
                else:
                    h1 = pix[x-1,y]

                if xSize - x <= factor:
                    h2 = pix[x-1,y]
                else:
                    h2 = pix[x+factor,y]

                if y == 0:
                    v1 = pix[x,y+factor]
                else:
                    v1 = pix[x,y-1]

                if ySize - y <= factor:
                    v2 = pix[x,y-1]
                else:
                    v2 = pix[x,y+factor]


                if (orig != h1 and orig != h2) or (orig != v1 and orig != v2):
                    if orig[0] == orig[1] == orig[2]:
                        imageStatus[x][y] = 'outline'

    allColors = []
    colorList = []

    for x in range(0,xSize):
        for y in range(0,ySize):
            if imageStatus[x][y] != 'outline':
                allColors.append(pix[x,y])
                if pix[x,y] not in colorList and not (pix[x,y][0] == pix[x,y][1] and pix[x,y][1] == pix[x,y][2]):
                    colorList.append(pix[x,y])

    print(len(colorList))
    reduced = False
    # if len(colorList) > 100 or difficulty < 100:
    if difficultyChoice < 100:
        reduced = True
        print('need to further reduce image')
        allColors.sort()
        commonColors = []
        rareColors = []
        currentColor = allColors[0]
        colorNumber = 1
        for color in allColors:
            if color != currentColor:
                reduceFactor = 100000000 / ((len(colorList)) * 2)
                reduceFactor /= difficulty
                if colorNumber < (xSize * ySize / reduceFactor): 
                    rareColors.append(color)
                else:
                    commonColors.append(color)
                colorNumber = 1
                currentColor = color
            else:
                colorNumber += 1

        for x in range(0,xSize):
            for y in range(0,ySize):
                if imageStatus[x][y] != 'outline' and not (pix[x,y][0] == pix[x,y][1] and pix[x,y][1] == pix[x,y][2]):
                    if pix[x,y] in rareColors:
                        currentColorDiff = 1000
                        mostSimilarColor = NULL
                        for color in commonColors:
                            redDifference = pix[x,y][0] - color[0]
                            greenDifference = pix[x,y][1] - color[1]
                            blueDifference = pix[x,y][2] - color[2]
                            if (abs(redDifference) + abs(greenDifference) + abs(blueDifference)) < currentColorDiff:
                                currentColorDiff = abs(redDifference) + abs(greenDifference) + abs(blueDifference)
                                mostSimilarColor = color
                        if mostSimilarColor:
                            pix[x,y] = mostSimilarColor


            


    newGreyList = []
    for x in range(0,xSize):
        for y in range(0,ySize):       
            if pix[x,y][0] == pix[x,y][1] and pix[x,y][0] == pix[x,y][2] and pix[x,y] != 0:
                newGrey = int((pix[x,y][0] - 15) / 20) * 20 + 15
                if newGrey not in newGreyList:
                    newGreyList.append(newGrey)
                pix[x,y] = (newGrey,newGrey,newGrey)

    if len(newGreyList) > 10:
        print('need to reduce number of greys')
        for x in range(0,xSize):
            for y in range(0,ySize):       
                if pix[x,y][0] == pix[x,y][1] and pix[x,y][0] == pix[x,y][2] and pix[x,y] != 0:
                    newGrey = int((pix[x,y][0] - 15) / 40) * 40 + 15
                    pix[x,y] = (newGrey,newGrey,newGrey)

    colorList = []
    greyList = []

    print('getting new number of colors...')
    for x in range(0,xSize):
        for y in range(0,ySize):
            if imageStatus[x][y] != 'outline' and not (pix[x,y][0] == pix[x,y][1] == pix[x,y][2]) and pix[x,y] not in colorList:
                colorList.append(pix[x,y])
            if imageStatus[x][y] != 'outline' and pix[x,y][0] == pix[x,y][1] == pix[x,y][2] and pix[x,y] not in greyList:
                greyList.append(pix[x,y])

    colorList.sort()
    # print(len(colorList))
    greyList.sort()
    # print(len(greyList))

    print((len(colorList) + len(greyList)))

    im.save(renderedFile)

    im2 = Image.open(renderedFile)
    pix2 = im2.load()

    for x in range(0,xSize):
        for y in range(0,ySize):
            if imageStatus[x][y] != 'outline':
                if pix[x,y][2] == pix[x,y][0] and pix[x,y][2] == pix[x,y][1]:
                    imageStatus[x][y] = 'greyScale'
                else:
                    imageStatus[x][y] = 'notAGrey'

    for x in range(0,xSize):
        for y in range(0,ySize):
            if imageStatus[x][y] != 'outline' and imageStatus[x][y] != 'bigBorder':
                makeBorder = False
                if y < ySize-1 and imageStatus[x][y+1] != 'outline' and imageStatus[x][y+1] != 'bigBorder' and imageStatus[x][y] != imageStatus [x][y+1]:
                    pix2[x,y] = (175,175,175)
                    pix2[x,y+1] = (175,175,175)
                    imageStatus[x][y+1] = 'bigBorder'
                    makeBorder = True
                if x < xSize-1 and imageStatus[x+1][y] != 'outline' and imageStatus[x+1][y] != 'bigBorder' and imageStatus[x][y] != imageStatus [x+1][y]:
                    pix2[x,y] = (175,175,175)
                    pix2[x+1,y] = (175,175,175)
                    imageStatus[x+1][y] = 'bigBorder'
                    makeBorder = True
                if makeBorder == True:
                    imageStatus[x][y] = 'bigBorder'

    for x in range(0,xSize):
        for y in range(0,ySize):
            # if imageStatus[x][y] == 'bigBorder':
            #     imageStatus[x][y] == '25'
            # elif imageStatus[x][y] != 'outline':
            if imageStatus[x][y] != 'outline':
                if pix[x,y][0] > pix[x,y][1] and pix[x,y][0] > pix[x,y][2]:
                    imageStatus[x][y] = '0'
                elif pix[x,y][1] > pix[x,y][0] and pix[x,y][1] > pix[x,y][2]:
                    imageStatus[x][y] = '2'
                elif pix[x,y][2] > pix[x,y][0] and pix[x,y][2] > pix[x,y][1]:
                    imageStatus[x][y] = '4'
                elif pix[x,y][0] == pix[x,y][1] and pix[x,y][0] > pix[x,y][2]:
                    imageStatus[x][y] = '1'
                elif pix[x,y][1] == pix[x,y][2] and pix[x,y][1] > pix[x,y][0]:
                    imageStatus[x][y] = '3'
                elif pix[x,y][2] == pix[x,y][0] and pix[x,y][2] > pix[x,y][1]:
                    imageStatus[x][y] = '5'

    for x in range(0,xSize):
        for y in range(0,ySize):
            if imageStatus[x][y] != 'outline' and imageStatus[x][y] != 'greyScale':
                makeBorder = False
                if y < ySize-1 and imageStatus[x][y+1] != 'outline' and imageStatus[x][y] != 'bigBorder' and imageStatus[x][y+1] != 'bigBorder' and imageStatus[x][y+1] != 'greyScale' and abs(int(imageStatus[x][y]) - int(imageStatus[x][y + 1])) != 5 and abs(int(imageStatus[x][y]) - int(imageStatus[x][y + 1])) > 1:
                    pix2[x,y] = (175,175,175)
                    pix2[x,y+1] = (175,175,175)
                    imageStatus[x][y+1] = 'bigBorder'
                    makeBorder = True
                if x < xSize-1 and imageStatus[x+1][y] != 'outline' and imageStatus[x][y] != 'bigBorder' and imageStatus[x+1][y] != 'bigBorder' and imageStatus[x+1][y] != 'greyScale' and abs(int(imageStatus[x][y]) - int(imageStatus[x + 1][y])) != 5 and abs(int(imageStatus[x][y]) - int(imageStatus[x + 1][y])) > 1:
                    pix2[x,y] = (175,175,175)
                    pix2[x+1,y] = (175,175,175)
                    imageStatus[x+1][y] = 'bigBorder'
                    makeBorder = True
                if makeBorder == True:
                    imageStatus[x][y] = 'bigBorder'

    for x in range(0,xSize):
        for y in range(0,ySize):
            nextXDiff = 0
            nextYDiff = 0
            orig = pix[x,y]
            if imageStatus[x][y] != 'outline' and imageStatus[x][y] != 'bigBorder':
                if x < xSize - 1:
                    nextXPixel = pix[x+1,y]
                    nextXDiff = abs(pix[x,y][0] - nextXPixel[0]) + abs(pix[x,y][1] - nextXPixel[1]) + abs(pix[x,y][2] - nextXPixel[2])
                if y < ySize - 1:
                    nextYPixel = pix[x,y+1]
                    nextYDiff = abs(pix[x,y][0] - nextYPixel[0]) + abs(pix[x,y][1] - nextYPixel[1]) + abs(pix[x,y][2] - nextYPixel[2])



            if pix[x,y] == (255,255,255):
                imageStatus[x][y] = 'outline'

            if imageStatus[x][y] == 'outline':
                pix2[x,y] = pix[x,y]

            if imageStatus[x][y] != 'bigBorder' and imageStatus[x][y] != 'outline':
                if nextXDiff > 0 and x < xSize - 1 and imageStatus[x + 1][y] != 'outline':
                    borderGrey = 255 - (int(nextXDiff/15) - 1) * 10
                    # if nextXDiff >= 75:
                    #     borderGrey = 195
                    # elif nextXDiff >= 45:
                    #     borderGrey = 225
                    # elif nextXDiff >= 30:
                    #     borderGrey = 255
                    # elif nextXDiff >= 15:
                    #     borderGrey = 255
                    # else:
                    #     borderGrey = 255
                    pix2[x,y] = (borderGrey,borderGrey,borderGrey)
                    imageStatus[x][y] = 'border'
                    pix2[x + 1,y] = (borderGrey,borderGrey,borderGrey)
                    imageStatus[x + 1][y] = 'border'
                if nextYDiff > 0 and y < ySize - 1 and imageStatus[x][y + 1] != 'outline':
                    borderGrey = 255 - (int(nextYDiff/15) - 1) * 10

                    # if nextYDiff >= 75:
                    #     borderGrey = 195
                    # elif nextYDiff >= 45:
                    #     borderGrey = 225
                    # elif nextYDiff >= 30:
                    #     borderGrey = 255
                    # elif nextXDiff >= 15:
                    #     borderGrey = 255
                    # else:
                    #     borderGrey = 255                
                    pix2[x,y] = (borderGrey,borderGrey,borderGrey)
                    imageStatus[x][y] = 'border'
                    pix2[x,y + 1] = (borderGrey,borderGrey,borderGrey)
                    imageStatus[x][y + 1] = 'border'
                
            if imageStatus[x][y] != 'border' and imageStatus[x][y] != 'outline' and imageStatus[x][y] != 'bigBorder':
                pix2[x,y] = (255,255,255)

    im2.save(outlinedFile)
    print(outlinedFile + ': ' + str(len(colorList) + len(greyList)) + ' ' + str(len(greyList)) + ' grey,' + str(reduced))







































    # im = Image.open(openedFile) # Can be many different formats.
    # pix = im.load()
    # imageStatus = [[0 for x in range(ySize)] for y in range(xSize)] 
    # for redo in range(1,2):

    #     for factor in range(1,4):

    #         print('getting rid of ' + str(factor) + ' size pixels...')
    #         for x in range(0,xSize):
    #             for y in range(0,ySize):

    #                 orig = pix[x,y]

    #                 if y == 0:
    #                     v1 = pix[x,y+factor]
    #                 else:
    #                     v1 = pix[x,y-1]

    #                 if ySize - y <= factor:
    #                     v2 = pix[x,y-1]
    #                 else:
    #                     v2 = pix[x,y+factor]

    #                 v1Diff = abs(v1[0]-orig[0]) + abs(v1[1]-orig[1]) + abs(v1[2]-orig[2])
    #                 v2Diff = abs(v2[0]-orig[0]) + abs(v2[1]-orig[1]) + abs(v2[2]-orig[2])

    #                 if orig != v1 and orig != v2:
    #                     # is it grey?
    #                     if orig[0] == orig[1] == orig[2]:
    #                         imageStatus[x][y] = 'outline'
    #                     else:
    #                         # is it significantly different than the other two?
    #                         if v1Diff > signDiff and v2Diff > signDiff:
    #                             greyColor = int((orig[0] + orig[1] + orig[2])/3)
    #                             if greyColor != 255:
    #                                 greyColor = int((greyColor - 8) / 10) * 10 + 8
    #                             pix[x,y] = (greyColor,greyColor,greyColor)
    #                             imageStatus[x][y] = 'outline'
    #                         else:
    #                             if v1Diff <= v2Diff:
    #                                 orig = v1
    #                                 pix[x,y] = v1
    #                             else:
    #                                 orig = v2
    #                                 pix[x,y] = v2
    # #
    #         for x in range(0,xSize):
    #             for y in range(0,ySize):

    #                 orig = pix[x,y]

    #                 if y == 0:
    #                     v1 = pix[x,y+factor]
    #                 else:
    #                     v1 = pix[x,y-1]

    #                 if ySize - y <= factor:
    #                     v2 = pix[x,y-1]
    #                 else:
    #                     v2 = pix[x,y+factor]

    #                 if x == 0:
    #                     h1 = pix[x+factor,y]
    #                 else:
    #                     h1 = pix[x-1,y]

    #                 if xSize - x <= factor:
    #                     h2 = pix[x-1,y]
    #                 else:
    #                     h2 = pix[x+factor,y]

    #                 h1Diff = abs(h1[0]-orig[0]) + abs(h1[1]-orig[1]) + abs(h1[2]-orig[2])
    #                 h2Diff = abs(h2[0]-orig[0]) + abs(h2[1]-orig[1]) + abs(h2[2]-orig[2])

    #                 if orig != h1 and orig != h2:
    #                     # is it grey?
    #                     if orig[0] == orig[1] == orig[2]:
    #                         imageStatus[x][y] = 'outline'
    #                     else:
    #                         # is it significantly different than the other two?
    #                         if h1Diff > signDiff and h2Diff > signDiff:
    #                             greyColor = int((orig[0] + orig[1] + orig[2])/3)
    #                             if greyColor != 255:
    #                                 greyColor = int((greyColor - 8) / 10) * 10 + 8
    #                             pix[x,y] = (greyColor,greyColor,greyColor)
    #                             imageStatus[x][y] = 'outline'
    #                         else:
    #                             if h1Diff <= h2Diff:
    #                                 orig = h1
    #                                 pix[x,y] = h1
    #                             else:
    #                                 orig = h2
    #                                 pix[x,y] = h2

    #         for x in range(0,xSize):
    #             for y in range(0,ySize):
    #                 orig = pix[x,y]

    #                 if x == 0:
    #                     h1 = pix[x+factor,y]
    #                 else:
    #                     h1 = pix[x-1,y]

    #                 if xSize - x <= factor:
    #                     h2 = pix[x-1,y]
    #                 else:
    #                     h2 = pix[x+factor,y]

    #     for x in range(0,xSize):
    #         for y in range(0,ySize):

    #             orig = pix[x,y]

    #             if x == 0:
    #                 h1 = pix[x+factor,y]
    #             else:
    #                 h1 = pix[x-1,y]

    #             if xSize - x <= factor:
    #                 h2 = pix[x-1,y]
    #             else:
    #                 h2 = pix[x+factor,y]

    #             if y == 0:
    #                 v1 = pix[x,y+factor]
    #             else:
    #                 v1 = pix[x,y-1]

    #             if ySize - y <= factor:
    #                 v2 = pix[x,y-1]
    #             else:
    #                 v2 = pix[x,y+factor]


    #             if (orig != h1 and orig != h2) or (orig != v1 and orig != v2):
    #                 if orig[0] == orig[1] == orig[2]:
    #                     imageStatus[x][y] = 'outline'

    # allColors = []
    # colorList = []

    # for x in range(0,xSize):
    #     for y in range(0,ySize):
    #         if imageStatus[x][y] != 'outline':
    #             allColors.append(pix[x,y])
    #             if pix[x,y] not in colorList and not (pix[x,y][0] == pix[x,y][1] and pix[x,y][1] == pix[x,y][2]):
    #                 colorList.append(pix[x,y])

    # print(len(colorList))
    # reduced = False
    # # if len(colorList) > 100 or difficulty < 100:
    # rareColors = []
    # commonColors = []
    # if difficultyChoice < 100:
    #     reduced = True
    #     print('need to further reduce image')
    #     allColors.sort()
    #     currentColor = allColors[0]
    #     colorNumber = 1
    #     for color in allColors:
    #         if color != currentColor:
    #             reduceFactor = 100000000 / ((len(colorList)) * 2)
    #             reduceFactor /= difficulty
    #             if colorNumber < (xSize * ySize / reduceFactor): 
    #                 rareColors.append(color)
    #             else:
    #                 commonColors.append(color)
    #             colorNumber = 1
    #             currentColor = color
    #         else:
    #             colorNumber += 1

    #     # for x in range(0,xSize):
    #     #     for y in range(0,ySize):
    #     #         if imageStatus[x][y] != 'outline' and not (pix[x,y][0] == pix[x,y][1] and pix[x,y][1] == pix[x,y][2]):
    #     #             if pix[x,y] in rareColors:
    #     #                 currentColorDiff = 1000
    #     #                 mostSimilarColor = NULL
    #     #                 for color in commonColors:
    #     #                     redDifference = pix[x,y][0] - color[0]
    #     #                     greenDifference = pix[x,y][1] - color[1]
    #     #                     blueDifference = pix[x,y][2] - color[2]
    #     #                     if (abs(redDifference) + abs(greenDifference) + abs(blueDifference)) < currentColorDiff:
    #     #                         currentColorDiff = abs(redDifference) + abs(greenDifference) + abs(blueDifference)
    #     #                         mostSimilarColor = color
    #     #                 if mostSimilarColor:
    #     #                     pix[x,y] = mostSimilarColor


            


    # newGreyList = []
    # for x in range(0,xSize):
    #     for y in range(0,ySize):       
    #         if pix[x,y][0] == pix[x,y][1] and pix[x,y][0] == pix[x,y][2] and pix[x,y] != 0:
    #             newGrey = int((pix[x,y][0] - 15) / 20) * 20 + 15
    #             if newGrey not in newGreyList:
    #                 newGreyList.append(newGrey)
    #             pix[x,y] = (newGrey,newGrey,newGrey)

    # if len(newGreyList) > 10:
    #     print('need to reduce number of greys')
    #     for x in range(0,xSize):
    #         for y in range(0,ySize):       
    #             if pix[x,y][0] == pix[x,y][1] and pix[x,y][0] == pix[x,y][2] and pix[x,y] != 0:
    #                 newGrey = int((pix[x,y][0] - 15) / 40) * 40 + 15
    #                 pix[x,y] = (newGrey,newGrey,newGrey)

    # colorList = []
    # greyList = []

    # print('getting new number of colors...')
    # for x in range(0,xSize):
    #     for y in range(0,ySize):
    #         if imageStatus[x][y] != 'outline' and not (pix[x,y][0] == pix[x,y][1] == pix[x,y][2]) and pix[x,y] not in colorList:
    #             colorList.append(pix[x,y])
    #         if imageStatus[x][y] != 'outline' and pix[x,y][0] == pix[x,y][1] == pix[x,y][2] and pix[x,y] not in greyList:
    #             greyList.append(pix[x,y])

    # colorList.sort()
    # # print(len(colorList))
    # greyList.sort()
    # # print(len(greyList))

    # print((len(colorList) + len(greyList)))

    # im.save(altrenderedFile)

    # im2 = Image.open(altrenderedFile)
    # pix2 = im2.load()

    # for x in range(0,xSize):
    #     for y in range(0,ySize):
    #         if imageStatus[x][y] != 'outline':
    #             if pix[x,y][2] == pix[x,y][0] and pix[x,y][2] == pix[x,y][1]:
    #                 imageStatus[x][y] = 'greyScale'
    #             else:
    #                 imageStatus[x][y] = 'notAGrey'

    # for x in range(0,xSize):
    #     for y in range(0,ySize):
    #         if imageStatus[x][y] != 'outline' and imageStatus[x][y] != 'bigBorder':
    #             makeBorder = False
    #             if y < ySize-1 and imageStatus[x][y+1] != 'outline' and imageStatus[x][y+1] != 'bigBorder' and imageStatus[x][y] != imageStatus [x][y+1]:
    #                 pix2[x,y] = (175,175,175)
    #                 pix2[x,y+1] = (175,175,175)
    #                 imageStatus[x][y+1] = 'bigBorder'
    #                 makeBorder = True
    #             if x < xSize-1 and imageStatus[x+1][y] != 'outline' and imageStatus[x+1][y] != 'bigBorder' and imageStatus[x][y] != imageStatus [x+1][y]:
    #                 pix2[x,y] = (175,175,175)
    #                 pix2[x+1,y] = (175,175,175)
    #                 imageStatus[x+1][y] = 'bigBorder'
    #                 makeBorder = True
    #             if makeBorder == True:
    #                 imageStatus[x][y] = 'bigBorder'

    # for x in range(0,xSize):
    #     for y in range(0,ySize):
    #         # if imageStatus[x][y] == 'bigBorder':
    #         #     imageStatus[x][y] == '25'
    #         # elif imageStatus[x][y] != 'outline':
    #         if imageStatus[x][y] != 'outline':
    #             if pix[x,y][0] > pix[x,y][1] and pix[x,y][0] > pix[x,y][2]:
    #                 imageStatus[x][y] = '0'
    #             elif pix[x,y][1] > pix[x,y][0] and pix[x,y][1] > pix[x,y][2]:
    #                 imageStatus[x][y] = '2'
    #             elif pix[x,y][2] > pix[x,y][0] and pix[x,y][2] > pix[x,y][1]:
    #                 imageStatus[x][y] = '4'
    #             elif pix[x,y][0] == pix[x,y][1] and pix[x,y][0] > pix[x,y][2]:
    #                 imageStatus[x][y] = '1'
    #             elif pix[x,y][1] == pix[x,y][2] and pix[x,y][1] > pix[x,y][0]:
    #                 imageStatus[x][y] = '3'
    #             elif pix[x,y][2] == pix[x,y][0] and pix[x,y][2] > pix[x,y][1]:
    #                 imageStatus[x][y] = '5'

    # for x in range(0,xSize):
    #     for y in range(0,ySize):
    #         if imageStatus[x][y] != 'outline' and imageStatus[x][y] != 'greyScale':
    #             makeBorder = False
    #             if y < ySize-1 and imageStatus[x][y+1] != 'outline' and imageStatus[x][y] != 'bigBorder' and imageStatus[x][y+1] != 'bigBorder' and imageStatus[x][y+1] != 'greyScale' and abs(int(imageStatus[x][y]) - int(imageStatus[x][y + 1])) != 5 and abs(int(imageStatus[x][y]) - int(imageStatus[x][y + 1])) > 1:
    #                 pix2[x,y] = (175,175,175)
    #                 pix2[x,y+1] = (175,175,175)
    #                 imageStatus[x][y+1] = 'bigBorder'
    #                 makeBorder = True
    #             if x < xSize-1 and imageStatus[x+1][y] != 'outline' and imageStatus[x][y] != 'bigBorder' and imageStatus[x+1][y] != 'bigBorder' and imageStatus[x+1][y] != 'greyScale' and abs(int(imageStatus[x][y]) - int(imageStatus[x + 1][y])) != 5 and abs(int(imageStatus[x][y]) - int(imageStatus[x + 1][y])) > 1:
    #                 pix2[x,y] = (175,175,175)
    #                 pix2[x+1,y] = (175,175,175)
    #                 imageStatus[x+1][y] = 'bigBorder'
    #                 makeBorder = True
    #             if makeBorder == True:
    #                 imageStatus[x][y] = 'bigBorder'

    # for x in range(0,xSize):
    #     for y in range(0,ySize):
    #         nextXDiff = 0
    #         nextYDiff = 0
    #         orig = pix[x,y]
    #         if imageStatus[x][y] != 'outline' and imageStatus[x][y] != 'bigBorder':
    #             if x < xSize - 1:
    #                 nextXPixel = pix[x+1,y]
    #                 nextXDiff = abs(pix[x,y][0] - nextXPixel[0]) + abs(pix[x,y][1] - nextXPixel[1]) + abs(pix[x,y][2] - nextXPixel[2])
    #             if y < ySize - 1:
    #                 nextYPixel = pix[x,y+1]
    #                 nextYDiff = abs(pix[x,y][0] - nextYPixel[0]) + abs(pix[x,y][1] - nextYPixel[1]) + abs(pix[x,y][2] - nextYPixel[2])



    #         if pix[x,y] == (255,255,255):
    #             imageStatus[x][y] = 'outline'

    #         if imageStatus[x][y] == 'outline':
    #             pix2[x,y] = pix[x,y]

    #         if imageStatus[x][y] != 'bigBorder' and imageStatus[x][y] != 'outline':
    #             if nextXDiff > 0 and x < xSize - 1 and imageStatus[x + 1][y] != 'outline':
    #                 borderGrey = 255 - (int(nextXDiff/15) - 1) * 10
    #                 # if nextXDiff >= 75:
    #                 #     borderGrey = 195
    #                 # elif nextXDiff >= 45:
    #                 #     borderGrey = 225
    #                 # elif nextXDiff >= 30:
    #                 #     borderGrey = 255
    #                 # elif nextXDiff >= 15:
    #                 #     borderGrey = 255
    #                 # else:
    #                 #     borderGrey = 255
    #                 pix2[x,y] = (borderGrey,borderGrey,borderGrey)
    #                 imageStatus[x][y] = 'border'
    #                 pix2[x + 1,y] = (borderGrey,borderGrey,borderGrey)
    #                 imageStatus[x + 1][y] = 'border'
    #             if nextYDiff > 0 and y < ySize - 1 and imageStatus[x][y + 1] != 'outline':
    #                 borderGrey = 255 - (int(nextYDiff/15) - 1) * 10

    #                 # if nextYDiff >= 75:
    #                 #     borderGrey = 195
    #                 # elif nextYDiff >= 45:
    #                 #     borderGrey = 225
    #                 # elif nextYDiff >= 30:
    #                 #     borderGrey = 255
    #                 # elif nextXDiff >= 15:
    #                 #     borderGrey = 255
    #                 # else:
    #                 #     borderGrey = 255                
    #                 pix2[x,y] = (borderGrey,borderGrey,borderGrey)
    #                 imageStatus[x][y] = 'border'
    #                 pix2[x,y + 1] = (borderGrey,borderGrey,borderGrey)
    #                 imageStatus[x][y + 1] = 'border'
                
    #         if imageStatus[x][y] != 'border' and imageStatus[x][y] != 'outline' and imageStatus[x][y] != 'bigBorder':
    #             pix2[x,y] = (255,255,255)
    #         if imageStatus[x][y] != 'outline':
    #             if pix[x,y] in rareColors:
    #                 pix2[x,y] = pix[x,y]
            

    # im2.save(altoutlinedFile)
    # print(altoutlinedFile + ': ' + str(len(colorList) + len(greyList)) + ' ' + str(len(greyList)) + ' grey,' + str(reduced))

