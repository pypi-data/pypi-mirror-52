from distutils.core import setup
setup(
  name = 'el_piptest',
  packages = ['el_piptest'],
  version = '0.2',
  license='MIT',
  description = 'Test pip install my package',
  author = 'eleannna',
  author_email = 'your.email@domain.com',
  url = 'https://github.com/eleannna/Piptest',
  download_url = 'https://github.com/eleannna/Piptest/archive/v_02.tar.gz',
  keywords = ['install', 'pip'],
  install_requires=[
          'numpy'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',    
	'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',    
	'License :: OSI Approved :: MIT License',    
	'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
