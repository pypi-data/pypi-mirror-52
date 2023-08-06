from distutils.core import setup

setup(
  name = 'cocloud',
  packages = ['cocloud'],
  version = 0.2,
  license='MIT',
  description = 'of common code utility for aws services',
  author = 'Paul Singman',
  author_email = 'paul.singman@equinox.com',
  url = 'https://github.com/equinoxfitness/datacoco.cloud',
  download_url = 'https://github.com/equinoxfitness/datacoco.cloud/archive/v-0.2.tar.gz',
  keywords = ['helper', 'config', 'logging', 'common'],   # Keywords that define your package best
  install_requires=[
      'requests==2.20.0',
      'cocore==1.2.0',
      'gevent==1.3.7',
      'boto3==1.9.203'
    ]
)
