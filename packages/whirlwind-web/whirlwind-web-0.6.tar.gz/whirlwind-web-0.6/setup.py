from whirlwind import VERSION

from setuptools import setup, find_packages

setup(
      name = "whirlwind-web"
    , version = VERSION
    , packages = ['whirlwind'] + ['whirlwind.%s' % pkg for pkg in find_packages('whirlwind')]
    , include_package_data = True

    , install_requires =
      [ "tornado >= 5.1.1"
      , "delfick_project >= 0.5"
      ]

    , extras_require =
      { "tests":
        [ "noseOfYeti>=1.7"
        , "asynctest==0.10.0"
        , "nose"
        , "mock"
        ]
      , "peer":
        [ "tornado==5.1.1"
        , "delfick_project==0.5"
        ]
      }

    # metadata for upload to PyPI
    , url = "http://github.com/delfick/whirlwind"
    , author = "Stephen Moore"
    , author_email = "delfick755@gmail.com"
    , description = "Wrapper around the tornado web server library"
    , long_description = open("README.rst").read()
    , license = "MIT"
    , keywords = "tornado web"
    )
