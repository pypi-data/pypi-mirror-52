import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='transplan',
      version='0.0.2',
      author='Victor Sequi',
      author_email='vjsequi@gmail.com',
      description='Python parenting SATURN tools',
      url='https://github.com/vjsequi/TransportPy',
      dependency_links=['https://github.com/vjsequi/TransportPy'],
      license='GNU General Public License v3.0',
      packages=setuptools.find_packages(),
      classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        ],
      python_requires='>=3.7',
      zip_safe=False)