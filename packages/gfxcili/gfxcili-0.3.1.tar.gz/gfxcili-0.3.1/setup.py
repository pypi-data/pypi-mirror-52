# import setuptools
# from distutils.core import setup, Extension

import os
from setuptools import setup, find_packages, Extension

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as file_handler:
        return file_handler.read()

setup(
    name="gfxcili",
    version="0.3.1",
    url="https://github.com/bkosciow/cili",
    license="MIT",
    author="Bartosz Kościów",
    author_email="kosci1@gmail.com",
    description="GfxCili = GfxLCD in C",
    long_description=(read('README.rst')),
    keywords=[
        'gfxlcd', 'raspberry pi', 'ili9328', 'ili9486', 'gfxcili'
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Home Automation'
    ],
    ext_modules=[
        Extension(
            "gfxcili.ili9325",
            ["_cili9325.c", "_cili.c", "ili.c", "cili9325.c", "interface.c", "spi.c", "gpio.c"],
            extra_link_args=['-lwiringPi', '-ljpeg', '-lpng']
        ),
        Extension(
            "gfxcili.ili9486",
            ["_cili9486.c", "_cili.c", "ili.c", "cili9486.c", "interface.c", "spi.c", "gpio.c"],
            extra_link_args=['-lwiringPi', '-ljpeg', '-lpng']
        ),
    ],
)

