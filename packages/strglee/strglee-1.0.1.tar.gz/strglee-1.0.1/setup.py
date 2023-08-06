
from distutils.core import setup
# dependency_links = ['http://xxx/xmltodict', 'http://xxx/pycurl']

setup(
    name="strglee",
    version="1.0.1",
    description="This is a test of the setup",
    author="strglee",
    author_email="strglee@gmail.com",
    url="http://strglee.com",
    install_requires=['pycurl', 'xmltodict'],
    package_dir={"bar": "foobar"},
    packages=['qi', 'bar']
)
