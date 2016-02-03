import datetime
import requests
import os

import sys

from hotdog.FilePath import get_full_path
from hotdog.Config import GetConfig
import time
MustardURL = GetConfig('MUSTARD_URL')
MustardKey = GetConfig('MUSTARD_KEY')

PROJECTFOLDER = GetConfig('ProjectFolder')

def takeScreenshot(driver, imageName):
    worked = True
    try: driver.save_screenshot(imageName)
    except:
        try: driver.get_screenshot_as_file(imageName)
        except: worked = False
    return worked

def UploadToMustard(test, status, error_message=None, stacktrace=None):

    if test.options['mustard'] and not test.skipMustard:
        try:
            imageName = PROJECTFOLDER + str(int(round(time.time() * 1000)))+'.png'
            if takeScreenshot(test.driver, imageName):
                files = {'screenshot': open(imageName, 'rb')}
            else:
                files = None
        except:
            files = None

        platform = test.desired_caps['platformName'] if 'platformName' in test.desired_caps else test.desired_caps['platform']
        payload = {'project_id': MustardKey,
                   'device_id': getDeviceID(test),
                   'test_name': test._testMethodName,
                   'status': status,
                   'comment': error_message,
                   'stacktrace': stacktrace,
                   'device_platform': platform,
                   'device_type': test.options['manufacturer'] + ' ' +test.options['model'],
                   'os_version': test.options['osv'],
                   'link': test.resultLink
                   }
        if files:
            Upload(payload, files)
        else:
            Upload(payload)

        try:
            os.remove(imageName)
        except:
            pass

def UploadScreenshot(self, test, name=None):
    imageName = PROJECTFOLDER + str(int(round(time.time() * 1000)))+'.png'
    if test.options['mustard']:
        if takeScreenshot(test.driver, imageName):
            files = {'screenshot': open(imageName, 'rb')}

            payload = {'project_id': MustardKey,
                   'result_type': 'screenshot',
                   'device_id': getDeviceID(test),
                   'test_name': name if name else test.__class__.__name__,
                   }

            Upload(payload, files)

        try:
            os.remove(imageName)
        except:
            pass



def UploadPerformance(device, name, time):

    payload = {'project_id': MustardKey,
               'result_type': 'performance',
               'time': time,
               'device_id': device,
               'test_name': name,
               }

    Upload(payload)


def Upload(payload, files=None):
    caughtException = False
    try:
        r = requests.post(MustardURL, data=payload, files=files, verify=False)
    except:
        exceptionMessage = str(sys.exc_info()[1])
        caughtException = True

    if  caughtException or r.status_code != 200:
        bl = PROJECTFOLDER + '/MustardFailSafe.txt'

        with open(bl, 'a') as backlog:
            backlog.write(str(datetime.datetime.now()) + '\n')
            backlog.write(str(payload))
            if 'exceptionMessage' in locals():
                backlog.write(exceptionMessage)
            backlog.write('\n')
            backlog.write('\n')
        print('Failed to upload results to mustard.  Saved to MustardFailSafe.txt')

def getDeviceID(test):
    if 'udid' in test.driver.desired_capabilities:
        return test.driver.desired_capabilities['udid']
    else:
        return test.options['deviceName']