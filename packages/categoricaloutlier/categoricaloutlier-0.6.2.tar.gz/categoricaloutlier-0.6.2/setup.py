from distutils.core import setup
setup(
  name = 'categoricaloutlier',         # Name of the package
  packages = ['categoricaloutlier'],   
  version = '0.6.2',      
  license='MIT',        # MIT License
  description = 'Trains on categorical and date time features of the data and predicts an anomaly score for new data',   
  long_description='Categorical Outlier is a tool to detect anomalous observations in categorical and DateTime features. Most of the techniques that we already have are focused on numeric features. There is no library available which can detect an outlier within categorical data. This package does that by building a profile using the past observations and gives an outlier score to a new observation on the basis of this profile. An example use of this package may be predicting unusual driving behavior. A driver who drives the same route(s) to reach maybe office will show an anomalous behavior if he takes an altogether different route on a particular day. He will get a high outlier score for this behavior. On the contrary, an uber driver drives to a new location every time and hence, a new destination will not be an anomalous behavior and hence will get a low score. The package also takes a combination of categorical features as input.',
  author = 'AKASH BAJPAI',                   
  author_email = 'akash.baj03@gmail.com',      
  url = 'https://github.com/akashbaj03/categoricaloutlier',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/akashbaj03/categoricaloutlier/archive/categoricaloutlier_v0.1.tar.gz',    # Download link
  keywords = ['categorical', 'outlier', 'anomaly', 'unsupervised','datetime','frequency','probability'],   # Keywords that define your package best
  install_requires=['pandas','numpy','scipy'],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      #Supported python versions
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
