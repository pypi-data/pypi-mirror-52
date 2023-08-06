from distutils.core import setup
setup(
  name = 'pyimgflip',      
  packages = ['pyimgflip'],   
  version = '1.0.0',      
  license='MIT',        
  description = 'pyimgflip for simple code',   
  author = 'Yoshino',                   
  author_email = 'yoshino@oupbots.com',      
  url = 'https://github.com/KingAizen/pyimgflip',   
  download_url = 'https://github.com/KingAizen/pyimgflip.git',    
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   
  install_requires=[            
          'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Topic :: Software Development :: Build Tools',    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)