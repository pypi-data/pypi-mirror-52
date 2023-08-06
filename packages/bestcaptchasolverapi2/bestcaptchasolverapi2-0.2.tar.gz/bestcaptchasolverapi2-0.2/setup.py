import setuptools
from distutils.core import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()


setup(
  name = 'bestcaptchasolverapi2',
  packages = ['bestcaptchasolverapi2'], # this must be the same as the name above
  version = '0.2',
  description = 'Bestcaptchasolver python2 API library',
  author = 'BestCaptchaSolver',
  author_email = 'bcsolver@gmail.com',
  url = 'https://github.com/bestcaptchasolver/bestcaptchasolver-python2', # use the URL to the github repo
  download_url = 'https://github.com/bestcaptchasolver/bestcaptchasolver-python2', # I'll explain this in a second
  keywords = ['bestcaptchasolver', 'captcha', 'bypasscaptcha', 'decaptcher', 'decaptcha', '2captcha', 'deathbycaptcha', 'anticaptcha', 'bypass-recaptcha-v2', 'google-recaptcha-solver', 'recaptcha-v2-captcha-solver', 'captcha-services-for-recaptcha-v2', 'bypass-invisible-recaptcha', 'bypass-no-captcha-recaptcha', 'recaptcha-solver-python', 'recaptcha-bypass-script'],
  classifiers = [],
  long_description_content_type='text/markdown',
  long_description=long_description,
)
