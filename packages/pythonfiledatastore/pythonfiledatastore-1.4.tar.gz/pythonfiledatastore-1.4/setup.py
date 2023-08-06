from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pythonfiledatastore',
      version='1.4',
      description='File based datastore',
      url='https://github.com/njaveed/Datastore.git',
      author='Javeed',
      author_email='meetjaveed11@gmail.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='MIT',
      packages=['pythonfiledatastore'],
      install_requires=['cachetools'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
		],
		python_requires='>=3.6',
      zip_safe=False)