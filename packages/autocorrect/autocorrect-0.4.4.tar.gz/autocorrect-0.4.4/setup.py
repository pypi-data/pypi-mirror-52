from distutils.core import setup

setup(name='autocorrect',
      version='0.4.4',
      packages=['autocorrect'],
      package_data={'autocorrect': ['data/*.tar.gz']},
      description='Python 3 Spelling Corrector',
      author='Jonas McCallum',
      author_email='jonasmccallum@gmail.com',
      url='https://github.com/phatpiglet/autocorrect/',
      license='http://www.opensource.org/licenses/mit-license.php',
      classifiers=('Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Natural Language :: Polish',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',),
      keywords='autocorrect spelling corrector')
