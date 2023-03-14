from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import numpy as np
import json
from PIL import Image

from . import pbnUtils

from paintByNumberMeApp.models import ColorPixel

def index(request):
     return render(request, "paintByNumberMeApp/index.html")

def upload(request):
    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        pbnUtils.convert(file_url)
        return render(request, "paintByNumberMeApp/paint.html", 
        {
            # 'file_url1': file_url.replace('media/','media/result').replace('.jpg','1.png'),
            # 'file_url2': file_url.replace('media/','media/result').replace('.jpg','2.png'),
            'file_url3': file_url.replace('media/','media/result').replace('.jpg','3.png'),
            # 'file_url4': file_url.replace('media/','media/result').replace('.jpg','4.png'),
            # 'file_url5': file_url.replace('media/','media/result').replace('.jpg','5.png'),        
        })
    return render(request, "paintByNumberMeApp/upload.html")

def test(request):
    pbnUtils.testDivide('C:/Users/IansAcerLaptop/Documents/testColorAreaPict.png')
    return HttpResponse("this is a test")

def paintTest(request):
    fileName = 'resultElvisIan'
    # colorDict = pbnUtils.testDivide('./media/' + fileName + '2.png')
    # # colorDict = pbnUtils.testDivide('pbnMe/media/' + fileName)
    # print("Finished test divide")
    # paletteCount = 0
    # colorPalette = {}

    # for color in colorDict:
    #     paletteCount += 1
    #     for area in colorDict[color]:
    #         cp = ColorPixel(fileName=fileName, color=color, 
    #             colorNumber=paletteCount, paintArea=area,
    #             coorNum = len(colorDict[color][area]),
    #             coordinates = json.dumps(colorDict[color][area]))
    #         cp.save()
    # print("Finished colorpixel database")

    # samplePixels = ColorPixel.objects.filter(id=9302)
    samplePixels = ColorPixel.objects.all()
    for sample in samplePixels:
        # if sample.paintArea == 31649:
        # if sample.id == 1:
        if sample:
            # print(sample.id)
            goToNextSample = False
            sampleData = json.loads(sample.coordinates)
            sampleArray = np.array(sampleData)
            xArray = sampleArray[:,0]
            exitEntireOperation = False            

            center = int(sample.coorNum / 2)
            for squareSize in range(27, 0, -6):
                if sample.coorNum < 9:
                    break
                if squareSize ** 2 > sample.coorNum:
                    continue

                # find label coordinate in center
                exitXandY = False
                for x in range(sampleData[center][0] - int(squareSize / 2),sampleData[center][0] + int(squareSize / 2) + 1):
                    if x not in xArray:
                        continue
                    for y in range(sampleData[center][1] - int(squareSize / 2),sampleData[center][1] + int(squareSize / 2) + 1):
                        if [x,y] not in sampleData:
                            exitXandY = True
                            break
                    if exitXandY == True:
                        break
                if exitXandY == False:
                    sample.xCenter = sampleData[center][0]
                    sample.yCenter = sampleData[center][1]
                    sample.areaSize = squareSize
                    sample.save()
                    goToNextSample = True
                    break

            for squareSize in range(27, 0, -6):
                if sample.coorNum < 9:
                    break
                if goToNextSample == True:
                    break
                # find label coordinate going left to right
                for distanceFactor in range (1,sample.coorNum - center - int(squareSize ** 2 / 2)):

                    newCenter = int(sample.coorNum / 2) - distanceFactor
                    exitXandY = False
                    for x in range(sampleData[newCenter][0] - int(squareSize / 2),sampleData[newCenter][0] + int(squareSize / 2) + 1):
                        if x not in xArray:
                            continue
                        for y in range(sampleData[newCenter][1] - int(squareSize / 2),sampleData[newCenter][1] + int(squareSize / 2) + 1):
                            if [x,y] not in sampleData:
                                exitXandY = True
                                break
                        if exitXandY == True:
                            break
                    if exitXandY == False:
                        sample.xCenter = sampleData[newCenter][0]
                        sample.yCenter = sampleData[newCenter][1]
                        sample.areaSize = squareSize
                        sample.save()
                        goToNextSample = True
                        exitEntireOperation = True
                        break    

                    newCenter = int(sample.coorNum / 2) + distanceFactor
                    exitXandY = False
                    for x in range(sampleData[newCenter][0] - int(squareSize / 2),sampleData[newCenter][0] + int(squareSize / 2) + 1):
                        if x not in xArray:
                            continue
                        for y in range(sampleData[newCenter][1] - int(squareSize / 2),sampleData[newCenter][1] + int(squareSize / 2) + 1):
                            if [x,y] not in sampleData:
                                exitXandY = True
                                break
                        if exitXandY == True:
                            break
                    if exitXandY == False:
                        sample.xCenter = sampleData[newCenter][0]
                        sample.yCenter = sampleData[newCenter][1]
                        sample.areaSize = squareSize
                        sample.save()
                        exitEntireOperation = True
                        break   

                if exitEntireOperation == True:
                    break

            if goToNextSample == False:
                # print("label is at " + str(xCenter) + "," + str(yCenter) + " just at center.")
                sample.xCenter = sampleData[center][0]
                sample.yCenter = sampleData[center][1]
                sample.areaSize = 0
                sample.save()

            # RECORD CENTER COORDINATES WITH AREASIZE AT 0                           

            # maxX = int(np.max(sampleArray[:,0]))
            # minX = int(np.min(sampleArray[:,0]))
            # maxY = int(np.max(sampleArray[:,1]))
            # minY = int(np.min(sampleArray[:,1]))
            # xSize = maxX - minX + 1
            # ySize = maxY - minY + 1
            # xCenter = minX + int(xSize / 2)
            # yCenter = minY + int(ySize / 2)
            # print("XSize = " + str(xSize))
            # print("YSize = " + str(ySize))
            # print("Center = " + str(xCenter) + "," + str(yCenter))
            # exitEntireOperation = False
            # for squareSize in range(27, 0, -6):
            #     # print(sample.id)
            #     if squareSize > xSize and squareSize > ySize:
            #         # print("square size is bigger than area size")
            #         continue
            #     else:
            #         exitXandYloop = False
            #         # print("checking out the local area")
            #         for x in range(xCenter - int(squareSize/2),xCenter + int(squareSize/2) + 1):
            #             for y in range(yCenter - int(squareSize/2),yCenter + int(squareSize/2) + 1):
            #                 if [x,y] not in sampleData:
            #                     exitXandYloop = True
            #                     break
            #             if exitXandYloop == True:
            #                 break

            #         if exitXandYloop == False:
            #             # print("label is at " + str(xCenter) + "," + str(yCenter) + " at square size " + str(squareSize))
            #             sample.xCenter = xCenter
            #             sample.yCenter = yCenter
            #             sample.areaSize = squareSize
            #             sample.save()
            #             goToNextSample = True
            #             break
            #         else:
            #             rangeFactor = 0
            #             exitRangedScan = False
            #             exitXandYloop = False
            #             while(True):
            #                 # IF RANGE GOES BEYOND A CERTAIN POINT, START MAKING "newXCenter" and "newYCenter" random coordinates from the actual array
            #                 rangeFactor += 1
            #                 # print("going into range " + str(rangeFactor))
            #                 if (squareSize + squareSize * (rangeFactor) * 2) > xSize and (squareSize + squareSize * (rangeFactor) * 2) > ySize:
            #                     break
            #                 for newXCenter in range(xCenter - squareSize * rangeFactor, xCenter + squareSize * rangeFactor + 1):
            #                     # print("New X Center is " + str(newXCenter))
            #                     if newXCenter not in xArray:
            #                         continue
            #                     for newYCenter in range(yCenter - squareSize * rangeFactor, yCenter + squareSize * rangeFactor + 1):
            #                         if newYCenter not in yArray:
            #                             continue
            #                         if [newXCenter,newYCenter] not in sampleData:
            #                             continue
            #                         # print("center is at " + str(newXCenter) + "," + str(newYCenter))
            #                         if xCenter - squareSize * (rangeFactor - 1) <= newXCenter <= xCenter + squareSize * (rangeFactor - 1) and yCenter - squareSize * (rangeFactor - 1) <= newYCenter <= yCenter + squareSize * (rangeFactor - 1):
            #                             continue
            #                         else:
            #                             exitXandYloop = False
            #                             for x in range(newXCenter - int(squareSize/2),newXCenter + int(squareSize/2) + 1):
            #                                 exitXandYloop = False
            #                                 for y in range(newYCenter - int(squareSize/2),newYCenter + int(squareSize/2) + 1):
            #                                     if [x,y] not in sampleData:
            #                                         # print(str(x) + ',' + str(y) + ' not in coordinates')
            #                                         exitXandYloop = True
            #                                         break
            #                                 if exitXandYloop == True:
            #                                     break
            #                             if exitXandYloop == False:
            #                                 sample.xCenter = xCenter
            #                                 sample.yCenter = yCenter
            #                                 sample.areaSize = squareSize
            #                                 sample.save()
            #                                 # print("label is at " + str(newXCenter) + "," + str(newYCenter) + " at square size " + str(squareSize))
            #                                 goToNextSample = True
            #                                 exitXandYloop = True
            #                                 exitRangedScan = True
            #                                 exitEntireOperation = True
            #                                 break
            #                     #     if exitXandYloop == True:
            #                     #         break
            #                     # if exitXandYloop == True:
            #                     #     break
            #                     if exitEntireOperation == True:
            #                         break
            #                 if exitRangedScan == True:
            #                     break
            #             if exitEntireOperation == True:
            #                 break 
            #         if exitEntireOperation == True:
            #             break 
            #     if exitEntireOperation == True:
            #         break                        

            # if goToNextSample == False:
            #     # print("label is at " + str(xCenter) + "," + str(yCenter) + " just at center.")
            #     sample.xCenter = xCenter
            #     sample.yCenter = yCenter
            #     sample.areaSize = 0
            #     sample.save()                    
            #     # CONTINUE CODE HERE FOR SURROUNDING SQUARES



    print("Finished finding area centers")
    

    #     paletteColor = '#'
    #     paletteColor += (format(color[0], '02x'))
    #     paletteColor += (format(color[1], '02x'))        
    #     paletteColor += (format(color[2], '02x'))
    #     colorPalette[paletteCount] = {}
    #     colorPalette[paletteCount]['colorHue'] = paletteColor
    #     if color[0] < 128 and color[1] < 128 and color[2] < 128:
    #         colorPalette[paletteCount]['shade'] = 'dark'

    areaData = ColorPixel.objects.all()
    return render(request, "paintByNumberMeApp/paintTest.html",
        {
            'test_pict': '../media/' + fileName + '3.png',
            # 'colorPalette': colorPalette
            'pixels': areaData,
        }
    )