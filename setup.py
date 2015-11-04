from distutils.core import setup
setup(
  name = 'hotdog',
  packages = ['hotdog'], # this must be the same as the name above
  version = '0.1.2',
  description = 'Appium/Selenium testing framework deriving from unittest',
  author = 'Matt Watson',
  author_email = 'Watson.Mattc@gmail.com',
  url = 'https://github.com/Mattwhooo/Hotdog', # use the URL to the github repo
  download_url = 'https://github.com/Mattwhooo/Hotdog/tarball/0.1.2', # I'll explain this in a second
  keywords = ['appium', 'selenium', 'testing'], # arbitrary keywords
  classifiers=[],
  install_requires=['webium', 'testtools','beautifulsoup4','Appium-Python-Client', 'requests', 'sauceclient', 'timeout-decorator']
)