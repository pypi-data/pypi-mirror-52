""" Get Ready setup """

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup  # pylint: disable=E0611,F0401


setup(
    name='pylermo',
    version=0.1,
    install_requires=[],
    packages=['pylermo'],
    author='Werner Van Geit',
    author_email='werner.vangeit@gmail.com',
    entry_points={'console_scripts': ['pylermo=pylermo.pylermo:main'], },
    license="LGPLv3",
    keywords=(),
    classifiers=[
        'Development Status :: 4 - Beta'])
