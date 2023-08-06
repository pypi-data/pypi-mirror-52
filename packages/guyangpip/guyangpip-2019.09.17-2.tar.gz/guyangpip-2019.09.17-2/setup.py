import os

import setuptools

setuptools.setup(
    name='guyangpip',
    version='2019.09.17_2',
    keywords='demo',
    description='A demo for python packaging.',
    long_description=open(
        os.path.join(
            os.path.dirname(__file__),
            'README.rst'
        )
    ).read(),
    author='guyang',
    author_email='316903631@qq.com',

    url='https://github.com/DeliangFan/packagedemo',
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
