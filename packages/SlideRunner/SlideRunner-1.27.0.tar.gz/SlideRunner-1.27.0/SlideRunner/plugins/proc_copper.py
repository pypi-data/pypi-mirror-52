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
import os
import numpy as np
import matplotlib.pyplot as plt 
import sklearn.cluster
import matplotlib.colors



class Plugin(SlideRunnerPlugin.SlideRunnerPlugin):
    version = 0.1
    shortName = 'Rhodanine dye copper detection'
    inQueue = Queue()
    outQueue = Queue()
    initialOpacity=1.0
    updateTimer=0.1
    outputType = SlideRunnerPlugin.PluginOutputType.RGB_IMAGE
    description = 'Image-based detection of copper particles in rhodanine dye'
    pluginType = SlideRunnerPlugin.PluginTypes.IMAGE_PLUGIN
    configurationList = list((
                            SlideRunnerPlugin.PushbuttonPluginConfigurationEntry(uid=0, name='Store'),
                            SlideRunnerPlugin.PluginConfigurationEntry(uid='hue_value', name='HUE Value', initValue=0.04, minValue=0.0, maxValue=1.0),
                            SlideRunnerPlugin.PluginConfigurationEntry(uid='hue_range', name='HUE Range', initValue=0.08, minValue=0.0, maxValue=0.5),
                            SlideRunnerPlugin.PluginConfigurationEntry(uid='sat_min', name='SAT Min', initValue=0.2, minValue=0.0, maxValue=1.0),
                            SlideRunnerPlugin.PluginConfigurationEntry(uid='sat_max', name='SAT Max', initValue=1.2, minValue=0.0, maxValue=1.0),
                            SlideRunnerPlugin.PluginConfigurationEntry(uid=4, name='Weak Signals', initValue=220, minValue=0.0, maxValue=255.0),
                            SlideRunnerPlugin.PluginConfigurationEntry(uid=5, name='Medium Signals', initValue=175, minValue=0.0, maxValue=255.0),
                            SlideRunnerPlugin.PluginConfigurationEntry(uid=6, name='Strong Signals', initValue=100, minValue=0.0, maxValue=255.0),
                            SlideRunnerPlugin.PluginConfigurationEntry(uid=7, name='Gaussian Kernel', initValue=5, minValue=1.0, maxValue=10.0)))
    
    def __init__(self, statusQueue:Queue):
        self.statusQueue = statusQueue
        self.p = Thread(target=self.queueWorker, daemon=True)
        self.p.start()
        
        pass

    def queueWorker(self):
        debugModule= False
        quitSignal = False
        oldFilename = ''
        while not quitSignal:
            job = SlideRunnerPlugin.pluginJob(self.inQueue.get())
            image = job.currentImage

            if (job.jobDescription == SlideRunnerPlugin.JobDescription.QUIT_PLUGIN_THREAD):
                # signal to exit this thread
                quitSignal=True
                continue

            if (oldFilename is not job.slideFilename):
                # try to load old thresholds, if available
                if os.path.exists(job.slideFilename+'_copper_thresholds.npz'):
                    # Load file
                    f = np.load(job.slideFilename+'_copper_thresholds.npz')
                    config = f['config'].tolist()
                    updateConfig = list()
                    for entry in config.keys():
                        updateConfig.append(SlideRunnerPlugin.PluginConfigUpdateEntry(SlideRunnerPlugin.PluginConfigurationType.SLIDER_WITH_FLOAT_VALUE, uid=entry, value=config[entry]))
                    self.updateConfiguration(SlideRunnerPlugin.PluginConfigUpdate(updateConfig))
                oldFilename=job.slideFilename
                        

            if (job.trigger is not None):
                # SAVE button has been hit
                np.savez(job.slideFilename+'_copper_thresholds.npz', config=job.configuration)
                self.showMessageBox('Thresholds have been stored.')
                continue

            rgb = np.copy(image[:,:,0:3])

            # Blur
            kernelSize = job.configuration[7]
            rgb_blur = cv2.blur(rgb,(int(kernelSize),int(kernelSize)))


            hsv_sharp = matplotlib.colors.rgb_to_hsv(rgb)
            rgb_orig = rgb
            rgb = rgb_blur
            # Convert to HSV
            hsv = matplotlib.colors.rgb_to_hsv(rgb_blur)
            hsv_sharp_flat = np.reshape(hsv_sharp, [-1,3])

            img_hsv = np.reshape(hsv, [-1,3])

            if (debugModule):
                plt.clf()
                plt.subplot(1,3,1)
                plt.hist(img_hsv[:,0],255)
                plt.title('Hue')
                plt.subplot(1,3,2)
                plt.hist(img_hsv[:,1],255)
                plt.title('Sat')
                plt.subplot(1,3,3)
                plt.hist(img_hsv[:,2],255)
                plt.title('Val')
                plt.savefig('histo.pdf')


            HUE_MIN = job.configuration['hue_value'] - job.configuration['hue_range']
            HUE_MAX = job.configuration['hue_value'] + job.configuration['hue_range']


            SAT_MIN = job.configuration['sat_min']
            SAT_MAX = job.configuration['sat_max']
            hsv = np.float32(hsv)
            hue = hsv[:,:,0]
            sat = hsv[:,:,1]
            val = hsv[:,:,2]
            print('Absolut maximum values for HUE: ',np.min(hue),np.max(hue))
            print('Min and max values for HUE: ',HUE_MIN, HUE_MAX)
            print('Total: ',hue.shape[0]*hue.shape[1])

            if (HUE_MAX<1) and (HUE_MIN<0):
                print('HUE limits: < ',HUE_MAX,' or > ',1+HUE_MIN)
                hue_masked = (hue<HUE_MAX) | (hue>1+HUE_MIN)
            elif (HUE_MAX>1) and (HUE_MIN>0):
                print('HUE limits: > ',HUE_MIN,' or < ',HUE_MAX-1)
                hue_masked = (hue>HUE_MIN) | (hue<HUE_MAX-1)
            else:
                hue_masked = (hue>HUE_MIN) & (hue<HUE_MAX)
                print('HUE limits: > ',HUE_MIN,' and < ',HUE_MAX)

            print('HUE mask: ',np.sum(hue_masked))

            sat_masked = (hsv[:,:,1]>SAT_MIN) & (hsv[:,:,1]<SAT_MAX)

            if (debugModule):
                plt.clf()
                plt.hist(hue[sat_masked & hue_masked],255)
                plt.savefig('histo_hue_limited.pdf')

            hsv_masked = hsv[sat_masked & hue_masked,:]
            hsv_masked_flat = np.reshape(hsv_masked,[-1, 3])
            mask_flat = np.reshape(sat_masked & hue_masked, [-1])
            cluster = sklearn.cluster.KMeans(n_clusters=2)

            if (hsv_masked_flat.shape[0]<2):
                #nothing was found
                self.returnImage(np.float32(rgb_orig), job.procId)
                continue 

            cluster = cluster.fit(hsv_masked_flat[:,0:1])
            y = cluster.predict(hsv_masked_flat[:,0:1])
            print('kmeans Centers: (HSV) ',cluster.cluster_centers_)

            colors = [[j,255,255] for j in cluster.cluster_centers_*255]
            # choose cluster closest to zero
            chooseCluster = np.argmin(cluster.cluster_centers_)
            completeMask=sat_masked & hue_masked
            if (False):
                maskCluster = np.zeros(mask_flat.shape, dtype=np.bool)
                maskCluster[mask_flat] = (y==chooseCluster)
                color_array = np.asarray([colors[chooseCluster] for j in range(np.sum(maskCluster))])
                completeMask = np.reshape(maskCluster, newshape=rgb.shape[0:2])

            else:
                color_array = np.asarray([colors[j] for j in y])
                hsv_sharp_flat[mask_flat,0:3] = color_array

            if (True):
                rgb = rgb_orig
                strong = (val<job.configuration[6]) & completeMask
                medium = (val>job.configuration[6]) & (val<=job.configuration[5])  & completeMask
                weak = (val>job.configuration[5]) & (val<=job.configuration[4])  & completeMask

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



            self.returnImage(np.float32(rgb), job.procId)
            self.setMessage('PPC: Total: %d    Weak: %d   Medium: %d   Strong: %d    Copper Hue: %.2f' % (np.prod(rgb.shape[0:2]),np.sum(weak),np.sum(medium),np.sum(strong),cluster.cluster_centers_[chooseCluster] ))



        