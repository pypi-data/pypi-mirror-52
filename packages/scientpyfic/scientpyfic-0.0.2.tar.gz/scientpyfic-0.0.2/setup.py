from setuptools import setup
from os import path, walk
from glob import glob
import sys

current_path = path.abspath(path.dirname(__file__))
with open(path.join(current_path, 'README.rst'), encoding='utf-8') as file:
      long_description = file.read()

agents_file = path.join(path.join(current_path, 'scientpyfic'), 'agents.txt')
print(agents_file)
abspath = path.join(path.join(path.abspath(path.dirname(__file__)), 'scientpyfic'), 'module')

def get_modules(module_name, submodule, abspath):
  modules = []
  for current_path in walk(abspath):
    for subpath in glob(current_path[0]):
      if path.isdir(subpath) and subpath.find('__pycache__') is -1:
        if sys.platform == 'win32':
          paths = subpath.split('\\')
        else:
          paths = subpath.split('/')
        module_index = paths.index(submodule)
        module = '.'.join([module_name, submodule, *paths[module_index+1:]])
        modules.append(module)

  return modules

modules = get_modules('scientpyfic', 'module', abspath)

setup(name='scientpyfic',
      version='0.0.2',
      description='Latest science news from ScienceDaily.',
      long_description=long_description,
      url='https://github.com/monzita/scientpyfic',
      author='Monika Ilieva',
      author_email='hidden@hidden.com',
      license='MIT',
      keywords='scientpyfic science daily python beautifulsoup',
      packages=['scientpyfic', *modules],
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