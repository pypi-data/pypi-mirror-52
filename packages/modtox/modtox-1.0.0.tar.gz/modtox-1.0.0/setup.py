from distutils.core import setup


setup(name='modtox',
      version='1.0.0',
      description='Asses toxic effect of drugs based on MD simualtions of HROT dataset',
      author='Daniel Soler',
      author_email='daniel.soler@e-campus.uab.cat',
      url='https://www.python.org/sigs/distutils-sig/',
      install_requires=['pytraj', 'mdtraj', 'matplotlib', 'xgboost', 'sklearn', 'prody', 'biopython', 'pandas', 'mordred', 'nltk', 'seaborn', 'umap-learn', 'tqdm', 'requests', 'chembl_webresource_client', 'pytest'],
     )
