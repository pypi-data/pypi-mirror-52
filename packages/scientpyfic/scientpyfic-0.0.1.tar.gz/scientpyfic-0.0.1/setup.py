from setuptools import setup
from os import path

current_path = path.abspath(path.dirname(__file__))
with open(path.join(current_path, 'README.rst'), encoding='utf-8') as file:
      long_description = file.read()

agents_file = path.join(current_path + '/scientpyfic', 'agents.txt')

setup(name='scientpyfic',
      version='0.0.1',
      description='Latest science news from ScienceDaily.',
      long_description=long_description,
      url='https://github.com/monzita/scientpyfic',
      author='Monika Ilieva',
      author_email='hidden@hidden.com',
      license='MIT',
      keywords='scientpyfic science daily python beautifulsoup',
      packages=['scientpyfic'],
      package_dir={'scientpyfic' : 'scientpyfic'},
      package_data={'scientpyfic': [ agents_file ] },
      install_requires = ['beautifulsoup4', 'requests', 'lxml'],
      classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Science/Research',
            'Intended Audience :: Developers',
            'Intended Audience :: Education',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3 :: Only',
            'Topic :: Utilities'
      ],
      zip_safe=True)