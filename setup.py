from distutils.core import setup

from html_stripper import __doc__, __version__

setup(
    name="html_stripper",
    version=str(__version__),
    description=__doc__,
    py_modules=["html_stripper"],
    classifiers=[
        "Development Status :: 5 - Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
    ],
)
