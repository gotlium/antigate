from setuptools import setup


setup(
    name='antigate',
    version="1.2.1",
    description='Easy wrapper for antigate.com',
    keywords="antigate captcha",
    long_description=open('README.rst').read(),
    author="GoTLiuM InSPiRiT",
    author_email='gotlium@gmail.com',
    url='http://github.com/gotlium/antigate',
    packages=['antigate'],
    include_package_data=True,
    install_requires=[
        'pycurl',
        'lxml',
        'grab',
        'xmltodict',
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
