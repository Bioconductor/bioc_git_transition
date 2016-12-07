from setuptools import setup

setup(name='bioc_git_structure',
      version='0.1',
      description='Set up bioconductor git structure',
      url='http://github.com/nturaga/bioc_git_structure',
      author='nturaga',
      author_email='nitesh.turaga@roswellpark.org',
      license='MIT',
      packages=['bioc_git_structure'],
      install_requires=['gitpython'],
      zip_safe=False)
