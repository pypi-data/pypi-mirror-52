from setuptools import setup

with open('README.md', 'r') as readme:
    long_des = readme.read()


setup(
    name='prettimer',
    version='0.0.2',
    packages=[
        'prettimer',
    ],
    author='Giordano Zanoli',
    author_email='giordano.zanoli84@gmail.com',
    url="https://gitlab.com/giordano.zanoli/prettimer",
    long_description=long_des,
    long_description_content_type='text/markdown',
    extras_require={
        'dev': [
            'pytest==5.0.1',
            'Sphinx==1.8.2',
            'sphinx_rtd_theme==0.4.2',
            'numpydoc==0.8.0',
            'check-manifest==0.39',
            'twine==1.13'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
