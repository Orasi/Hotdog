from distutils.core import setup
from pkgutil import walk_packages
import hotdog

def find_packages(path='.', prefix=""):
    yield prefix
    prefix = prefix + "."
    for _, name, ispkg in walk_packages(path, prefix):
        if ispkg:
            yield name

setup(
  name = 'hotdog',
  packages = list(find_packages(hotdog.__path__, hotdog.__name__)),
  version = '1.6.11',
  description = 'Appium/Selenium testing framework deriving from unittest',
  author = 'Matt Watson',
  author_email = 'Watson.Mattc@gmail.com',
  url = 'https://github.com/Mattwhooo/Hotdog',
  download_url = 'https://github.com/Mattwhooo/Hotdog/tarball/1.6.11',
  keywords = ['appium', 'selenium', 'testing'],
  classifiers=[],
  install_requires=['testtools','beautifulsoup4','Appium-Python-Client', 'requests', 'sauceclient', 'timeout-decorator', 'appium_selector', 'waiting']
)