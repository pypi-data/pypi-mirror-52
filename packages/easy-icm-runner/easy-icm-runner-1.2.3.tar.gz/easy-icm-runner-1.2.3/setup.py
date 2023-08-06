from setuptools import setup
setup(
  name = 'easy-icm-runner',
  packages = ['easy-icm-runner',],
  version = '1.2.3',
  license='MIT',
  description = 'A wrapper for IBM ICMs Scheduler API Calls',
  author = 'Bachir El Koussa and Elliott Cordo',
  author_email = 'bgkoussa@gmail.com',
  url = 'https://github.com/equinoxfitness/easy-icm-runner',
  download_url = 'https://github.com/equinoxfitness/easy-icm-runner/archive/v_1.2.3.tar.gz',
  keywords = ['ICM', 'API', 'SCHEDULER', 'RUNNER', 'IBM'],
  install_requires=[
          'requests',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)