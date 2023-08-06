import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='qask',
     version='0.1.4',
     install_requires=[
        'Click',
     ],
     scripts=['qask'] ,
     author="Irina Bucse",
     author_email="irina.bucse@gmail.com",
     description="Create default skeleton app for new qa project",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/irinabucse/qask.git",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )