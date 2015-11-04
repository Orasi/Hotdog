import datetime
from time import sleep, time
import requests
import os
from hotdog.FilePath import get_full_path
from hotdog.Config import GetConfig

MustardURL = GetConfig('MUSTARD_URL')
MustardKey = GetConfig('MUSTARD_KEY')


def UploadToMustard(test, status, error_message=None, stacktrace=None):

    if test.options['mustard'] and not test.skipMustard:
        try:
            imageName = get_full_path(test.driver.desired_capabilities['udid']+'.png')
            test.driver.save_screenshot(imageName)
            files = {'screenshot': open(imageName, 'rb')}
        except:
            files = None


        payload = {'project_id': MustardKey,
                   'device_id': test.desired_caps['udid'],
                   'test_name': test._testMethodName,
                   'status': status,
                   'comment': error_message,
                   'stacktrace': stacktrace,
                   'device_platform': test.desired_caps['platformName'],
                   'device_type': test.options['manufacturer'] + ' ' +test.options['model'],
                   'os_version': test.options['osv']
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
    imageName = get_full_path(test.driver.desired_capabilities['udid']+'.png')
    if test.options['mustard']:
        test.driver.save_screenshot(imageName)

        files = {'screenshot': open(imageName, 'rb')}
        payload = {'project_id': MustardKey,
                   'result_type': 'screenshot',
                   'device_id': test.driver.desired_capabilities['udid'],
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
        r = requests.post(MustardURL, data=payload, files=files)
    except:
        caughtException = True

    if r.status_code != 200 or caughtException:
        bl = get_full_path('MustardFailSafe.txt')

        with open(bl, 'a') as backlog:
            backlog.write(str(datetime.datetime.now()) + '\n')
            backlog.write(str(payload))
            backlog.write('\n')
            backlog.write('\n')
        print('Failed to upload results to mustard.  Saved to MustardFailSafe.txt')