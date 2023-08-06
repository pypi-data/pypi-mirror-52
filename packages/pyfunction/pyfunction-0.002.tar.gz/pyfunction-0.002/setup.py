from distutils.core import setup
setup(
  name = 'pyfunction',         
  packages = ['pyfunction'],   
  version = '0.002',      
  license='MIT',       
  description = 'Library to plot linear functions', 
  long_description='Recommended to integrate in order of services and other scientific applications;\nThis library needs tkinter to launch the graphical application, use: (sudo apt install python3-tk) to linux users.\nSee my Readme to see how it is used: https://github.com/AndrasHPataki/pyfunction',
  author = 'AndrásPataki',                   
  author_email = 'andras.h.pataki@gmail.com',     
  url = 'https://github.com/AndrasHPataki/pyfunction',  
  download_url = 'https://github.com/AndrasHPataki/pyfunction/archive/0.02.tar.gz',   
  keywords = ['Math', 'Plot', 'Function'],  
  install_requires=[            
          'matplotlib'
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
