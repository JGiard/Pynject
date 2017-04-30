from setuptools import setup, find_packages

setup(name='Pynject',
      version='0.2',
      description='A minimalist python injector',
      url='https://github.com/JGiard/Pynject',
      author='Jean Giard',
      author_email='opensource@antidot.net',
      license='LGPL',
      classifier=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
          'Programming Language :: Python :: 3'
      ],
      keywords='pynject json',
      packages=find_packages(exclude=['pynject.test']),
      install_requires=[],
      test_suite='pynject.test')
