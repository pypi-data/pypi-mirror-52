from distutils.core import setup
setup(
  name = 'xrptipbotPy',      
  packages = ['xrptipbotPy'],
  version = '0.2',   
  license='MIT',     
  description = 'Python implementation of the XrpTipBot API',
  author = 'Just A Guy',                
  author_email = 'breakthroughconsultations@gmail.com',   
  url = 'https://github.com/AJ58O/xrptipbotPy',
  download_url = 'https://github.com/AJ58O/xrptipbotPy/archive/v_02.tar.gz', 
  keywords = ['XRP', 'xrptipbot', 'cryptocurrency'],
  install_requires=[         
          'requests',
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