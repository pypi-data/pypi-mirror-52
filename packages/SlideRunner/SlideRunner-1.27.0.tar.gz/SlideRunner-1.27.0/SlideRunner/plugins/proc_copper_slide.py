"""

        This is SlideRunner - An Open Source Annotation Tool 
        for Digital Histology Slides.

         Marc Aubreville, Pattern Recognition Lab, 
         Friedrich-Alexander University Erlangen-Nuremberg 
         marc.aubreville@fau.de

        If you use this software in research, please citer our paper:
        M. Aubreville, C. Bertram, R. Klopfleisch and A. Maier:
        SlideRunner - A Tool for Massive Cell Annotations in Whole Slide Images. 
        In: Bildverarbeitung für die Medizin 2018. 
        Springer Vieweg, Berlin, Heidelberg, 2018. pp. 309-314.

        This file:
         Positive Pixel Count Algorithm  (Aperio)
         
         see:
         Olson, Allen H. "Image analysis using the Aperio ScanScope." Technical manual. Aperio Technologies Inc (2006).



"""

import SlideRunner.general.SlideRunnerPlugin as SlideRunnerPlugin
import queue
from threading import Thread
from queue import Queue
import cv2
import numpy as np
#import matplotlib.pyplot as plt 
import sklearn.cluster
import openslide

def resize_with_border(img, IMG_COL, IMG_ROW):
    # Resize
    border_v = 0
    border_h = 0
    if (IMG_COL/IMG_ROW) >= (img.shape[0]/img.shape[1]):
        border_v = int((((IMG_COL/IMG_ROW)*img.shape[1])-img.shape[0])/2)
    else:
        border_h = int((((IMG_ROW/IMG_COL)*img.shape[0])-img.shape[1])/2)
    img = cv2.copyMakeBorder(img, border_v, border_v, border_h, border_h, cv2.BORDER_CONSTANT, 0)
    img = cv2.resize(img, (IMG_ROW, IMG_COL))
    return img

def drawMapOnImage(image, themap, target_size=None):
    mapCol = cv2.cvtColor(themap, cv2.COLOR_GRAY2RGB)
    ovImage = image*0.8 + mapCol*0.2
    if (target_size is None):
        return ovImage
    else:
        return resize_with_border(ovImage, target_size[0], target_size[1])

class Plugin(SlideRunnerPlugin.SlideRunnerPlugin):
    version = 0.1
    shortName = 'Rhodanine dye copper detection (WSI)'
    inQueue = Queue()
    outQueue = Queue()
    initialOpacity=1.0
    outputType = SlideRunnerPlugin.PluginOutputType.RGB_IMAGE
    description = 'Image-based detection of copper particles in rhodanine dye'
    pluginType = SlideRunnerPlugin.PluginTypes.WHOLESLIDE_PLUGIN
    configurationList = list((SlideRunnerPlugin.PluginConfigurationEntry(uid=0, name='HUE Value', initValue=0.04, minValue=0.0, maxValue=1.0),
                            SlideRunnerPlugin.PluginConfigurationEntry(uid=1, name='HUE Range', initValue=0.08, minValue=0.0, maxValue=1.0),
                            SlideRunnerPlugin.PluginConfigurationEntry(uid=2, name='SAT Threshold', initValue=0.2, minValue=0.0, maxValue=1.0),
                            SlideRunnerPlugin.PluginConfigurationEntry(uid=3, name='Weak Signals', initValue=220, minValue=0.0, maxValue=255.0),
                            SlideRunnerPlugin.PluginConfigurationEntry(uid=4, name='Medium Signals', initValue=175, minValue=0.0, maxValue=255.0),
                            SlideRunnerPlugin.PluginConfigurationEntry(uid=5, name='Strong Signals', initValue=100, minValue=0.0, maxValue=255.0),
                            SlideRunnerPlugin.PluginConfigurationEntry(uid=6, name='Gaussian Kernel', initValue=5, minValue=1.0, maxValue=10.0)))
    
    def __init__(self, statusQueue:Queue):
        self.statusQueue = statusQueue
        self.p = Thread(target=self.queueWorker, daemon=True)
        self.p.start()
        
        pass
    
    """
        image inference (once image statistics are known)
    """

    def imageInference(self, image, job: SlideRunnerPlugin.pluginJob) -> (np.ndarray, np.ndarray, np.ndarray, np.ndarray):
        rgb = cv2.cvtColor(np.asarray(image),cv2.COLOR_RGBA2RGB)

        # Blur
        kernelSize = job.configuration[6]
        rgb_blur = cv2.blur(rgb,(int(kernelSize),int(kernelSize)))
        rgb_orig = rgb
        rgb_copy = np.copy(rgb)
        rgb = rgb_blur

        HUE_VALUE = job.configuration[0]
        HUE_RANGE = job.configuration[1]
        SAT_THRESHOLD = job.configuration[2]

        # Convert to HSV
        hsv = cv2.cvtColor(rgb_blur, cv2.COLOR_RGB2HSV)

        img_hsv = np.reshape(hsv, [-1,3])

        hsv = np.float32(hsv)/255.0
        hue = hsv[:,:,0]
        sat = hsv[:,:,1]
        val = hsv[:,:,2]*255.0
        hue_masked = (hue > (HUE_VALUE-HUE_RANGE)) & (hue < (HUE_VALUE+HUE_RANGE) ) 

        if (HUE_VALUE-HUE_RANGE) < 0.0:
            hue_masked += (hue > (HUE_VALUE-HUE_RANGE)+1.0)
        if (HUE_VALUE+HUE_RANGE) > 1.0:
            hue_masked += (hue < (HUE_VALUE-HUE_RANGE)-1.0)
        sat_masked = (hsv[:,:,1]>SAT_THRESHOLD)

        hsv_masked = hsv[sat_masked & hue_masked,:]
        hsv_masked_flat = np.reshape(hsv_masked,[-1, 3])
        mask_flat = np.reshape(sat_masked & hue_masked, [-1])

        if (hsv_masked_flat.shape[0]<2):
            # nothing was found
            return rgb, rgb_copy, np.zeros(1), np.zeros(1), np.zeros(1) 

        y = self.cluster.predict(hsv_masked_flat[:,0:1])
        chooseCluster = np.argmin(self.cluster.cluster_centers_)
        completeMask=sat_masked & hue_masked

        maskCluster = np.zeros(mask_flat.shape, dtype=np.bool)
        maskCluster[mask_flat] = (y==chooseCluster)
        completeMask = np.reshape(maskCluster, newshape=rgb.shape[0:2])


        rgb = rgb_orig
        strong = (val<job.configuration[5]) & completeMask
        medium = (val>job.configuration[5]) & (val<=job.configuration[4])  & completeMask
        weak = (val>job.configuration[4]) & (val<=job.configuration[3])  & completeMask

        # strong: Red
        rgb[strong,0] = 255.0
        rgb[strong,1] = 0.0
        rgb[strong,2] = 0.0

        # medium: Orange
        rgb[medium,0] = 255.0
        rgb[medium,1] = 84.0
        rgb[medium,2] = 33.0

        # weak: Yellow
        rgb[weak,0] = 255.0
        rgb[weak,1] = 255.0
        rgb[weak,2] = 0.0

        return (rgb, rgb_orig, strong, medium, weak)


    def queueWorker(self):
        debugModule= False
        quitSignal = False
        lastSlide = None
        IMGSIZE=1024
        stats=dict()
        stats['total'] = 0
        stats['weak'] = 0
        stats['strong'] = 0
        stats['medium'] = 0
        cluster = None
        
        while not quitSignal:
            job = SlideRunnerPlugin.pluginJob(self.inQueue.get())
            print('Got new job!')
            image = job.currentImage

            if (job.jobDescription == SlideRunnerPlugin.JobDescription.QUIT_PLUGIN_THREAD):
                # signal to exit this thread
                quitSignal=True
                continue
            
            print('Slide is : ', job.slideFilename)
            if (job.slideFilename == lastSlide):
                # perfect - calculate on current view!
                if (job.coordinates[2]<2048) and self.cluster is not None:
                    coordinates = job.coordinates
                    img = sl.read_region(location=(coordinates[0],coordinates[1]), level=0, size=(coordinates[2],coordinates[3]))

                    (rgb, rgb_copy, strong, medium, weak) = self.imageInference(img, job)
                    self.returnImage(np.float32(resize_with_border(rgb,job.currentImage.shape[0],job.currentImage.shape[1])),job.procId)

                    pass

                continue
            HUE_VALUE = job.configuration[0]
            HUE_RANGE = job.configuration[1]
            SAT_THRESHOLD = job.configuration[2]

            lastSlide = job.slideFilename
            sl = openslide.open_slide(lastSlide)

            overview = sl.read_region(location=(0,0), level=sl.level_count-1, size=sl.level_dimensions[-1])
            # Convert to grayscale
            ovImage = np.asarray(overview)[:,:,0:3]

            gray = cv2.cvtColor(ovImage,cv2.COLOR_BGR2GRAY)

            # OTSU thresholding
            ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

            # dilate
            dil = cv2.dilate(thresh, kernel = np.ones((7,7),np.uint8))

            # erode
            er = cv2.erode(dil, kernel = np.ones((7,7),np.uint8))
            mapOv = er
            mapOrig = np.copy(mapOv)
            
            IMGSIZE_overview = int(np.ceil(IMGSIZE/sl.level_downsamples[-1]))

            self.returnImage(drawMapOnImage(ovImage, mapOv, (job.currentImage.shape[0], job.currentImage.shape[1])), job.procId)
            self.statusQueue.put((1, ' Sampling %d / 10' % 0 ))

            # sample randomly
            numTries=0
            numSamples=0
            samples=np.empty(shape=(0,3))
            while (numTries<1000) and (numSamples<10):
                x,y = int(np.random.rand(1)*(ovImage.shape[1]-IMGSIZE_overview)), int(np.random.rand(1)*(ovImage.shape[0]-IMGSIZE_overview))

                if (np.sum(mapOv[y:y+IMGSIZE_overview, x:x+IMGSIZE_overview])>0.9*255*np.square(IMGSIZE_overview)):
                    # found a sample
                    print('Area covered: ',np.sqrt(np.sum(mapOv[y:y+IMGSIZE_overview, x:x+IMGSIZE_overview])))
                    print('Target: ', IMGSIZE_overview)
                    img = sl.read_region(location=(int(x*sl.level_downsamples[-1]), int(y*sl.level_downsamples[-1])), level=0, size=(IMGSIZE,IMGSIZE))
                    imgNp = (np.asarray(img)[:,:,0:3])

                    kernelSize = job.configuration[6]
                    rgb_blur = cv2.blur(imgNp,(int(kernelSize),int(kernelSize)))
                    # Convert to HSV
                    hsv = cv2.cvtColor(rgb_blur, cv2.COLOR_RGB2HSV)
                    hsv = np.float32(hsv)/255.0
                    hue = hsv[:,:,0]
                    sat = hsv[:,:,1]
                    hue_masked = (hue > (HUE_VALUE-HUE_RANGE)) & (hue < (HUE_VALUE+HUE_RANGE) ) 

                    if (HUE_VALUE-HUE_RANGE) < 0.0:
                        hue_masked += (hue > (HUE_VALUE-HUE_RANGE)+1.0)
                    if (HUE_VALUE+HUE_RANGE) > 1.0:
                        hue_masked += (hue < (HUE_VALUE-HUE_RANGE)-1.0)
                    sat_masked = (hsv[:,:,1]>SAT_THRESHOLD)

                    hsv_masked = hsv[sat_masked & hue_masked,:]
                    hsv_masked_flat = np.reshape(hsv_masked,[-1, 3])

                    # ignore, if black image
                    if (np.mean(hsv_masked_flat[:,2]<0.1)):
                        continue

                    mapOv[y:y+IMGSIZE_overview, x:x+IMGSIZE_overview]=0
                    self.returnImage(drawMapOnImage(ovImage, mapOv, (job.currentImage.shape[0], job.currentImage.shape[1])), job.procId)

                    print(samples.shape)
                    samples = np.vstack((samples,hsv_masked_flat))
                    numTries=0
                    numSamples+=1
                    self.statusQueue.put((1, ' Sampling %d / 10' % numSamples ))
                    print(samples.shape)

                else:
                    numTries+=1
            
            # calculate statistics based on random sample
            print('Sample is of size: ', samples.shape)

            
            cluster = sklearn.cluster.KMeans(n_clusters=2)
            cluster = cluster.fit(samples[:,0:1])
            self.cluster = cluster
            y = cluster.predict(samples[:,0:1])
            print('kmeans Centers: (HSV) ',cluster.cluster_centers_)

            IMGSIZE = int(IMGSIZE*2)
            IMGSIZE_overview = int(IMGSIZE_overview*2)

            doSave = False
            mapOv = mapOrig

            num_x = int(np.ceil(sl.dimensions[0] / IMGSIZE))
            num_y = int(np.ceil(sl.dimensions[1] / IMGSIZE))

            for x_idx in range(num_x):
                for y_idx in range(num_y):
                    img = sl.read_region(location=(x_idx*IMGSIZE, y_idx*IMGSIZE), level=0, size=(IMGSIZE,IMGSIZE))
                    viewidx = y_idx+x_idx*num_y

                    oaMap = mapOv[y_idx*IMGSIZE_overview:(y_idx+1)*IMGSIZE_overview,
                                             x_idx*IMGSIZE_overview:(x_idx+1)*IMGSIZE_overview]

                    overviewActivity = np.zeros((IMGSIZE_overview,IMGSIZE_overview))

                    if (np.sum(oaMap>0.5) / np.prod(oaMap.shape) < 0.01):
                        self.statusQueue.put((0, int(100*viewidx/num_y/float(num_x))))
                        # empty slide
                        continue

                    overviewActivity[0:oaMap.shape[0],0:oaMap.shape[1]] = oaMap
                    
                    overviewActivity = cv2.resize(overviewActivity, dsize=(IMGSIZE, IMGSIZE))

                    (rgb, rgb_copy, strong, medium, weak) = self.imageInference(img, job)

                    if (doSave):
                        cv2.imwrite('img_%d.jpg' % viewidx, cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
                        cv2.imwrite('img_%d_o.jpg' % viewidx, cv2.cvtColor(rgb_copy, cv2.COLOR_RGB2BGR))

                    self.statusQueue.put((0, int(100*viewidx/num_y/float(num_x))))
                    self.returnImage(np.float32(resize_with_border(rgb,job.currentImage.shape[0],job.currentImage.shape[1])), job.procId)

                    stats['total'] +=  np.sum(overviewActivity>0.5)
                    stats['weak'] += np.sum(weak)
                    stats['strong'] += np.sum(strong)
                    stats['medium'] += np.sum(medium)
                    self.statusQueue.put((1, ' Overall (T/W/M/S):  %''d / %''d / %''d / %''d - Current (%d)  %''d / %''d / %''d / %''d ' % (stats['total'], stats['weak'], stats['medium'], stats['strong'], viewidx, np.sum(overviewActivity>0.5),np.sum(weak),np.sum(medium),np.sum(strong) )))

            self.statusQueue.put((0, -1))
            self.statusQueue.put((1, ' Overall statistics:  Total: %d / W: %d / M %d / S %d ' % (stats['total'], stats['weak'], stats['medium'], stats['strong'] )))
            print(stats)
        