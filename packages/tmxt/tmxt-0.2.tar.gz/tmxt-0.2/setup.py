import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='tmxt',
    version='0.2',
    scripts=['tmxt.py', 'tmxplore.py'],
    author="Bart Machielsen",
    author_email="bartmachielsen@gmail.com",
    description="Tool to convert TMX files to text files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bartmachielsen/tmxt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
)
