from setuptools import setup
from os import path

current_path = path.abspath(path.dirname(__file__))
with open(path.join(current_path, 'README.rst'), encoding='utf-8') as file:
      long_description = file.read()

setup(name='arxivpy',
      version='0.0.0',
      description='Soon.',
      long_description=long_description,
      url='https://github.com/monzita/arXivpy',
      author='Monika Ilieva',
      author_email='hidden@hidden.com',
      license='MIT',
      keywords='arXiv science beautifulsoup search',
      packages=['arxivpy'],
      package_dir={'arxivpy' : 'arxivpy'},
      install_requires = ['beautifulsoup4', 'requests'],
      classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Intended Audience :: Education',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3 :: Only',
            'Topic :: Utilities'
      ],
      zip_safe=True)