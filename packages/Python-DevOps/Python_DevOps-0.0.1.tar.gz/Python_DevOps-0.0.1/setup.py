from setuptools import setup, find_packages

with open("README.md","r") as fh:
    long_description= fh.read()

setup(
    name='Python_DevOps',
    version='0.0.1',
    author='Mostafa Ramezani',
    author_email='crystalsoft2010@gmail.com',
    description='Sample of How Implement CI for python project and Build Docker image for Shippable product.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://fanoosrahnama.ir',
    py_modules=["calculator","helloworld"],
   # package_dir={'':'Python_CI_CD_Test'},
    install_requires=['Flask>=1.1.1',],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

    
