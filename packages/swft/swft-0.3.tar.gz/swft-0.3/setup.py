import setuptools

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setuptools.setup(name='swft',
                version='0.3',
                description='Process swft files',
                long_description=long_description,
                long_description_content_type='text/markdown',
                url='',
                author='Marc Endesfelder',
                author_email='marc@endesfelder.de',
                license='MIT',
                packages=setuptools.find_packages(),
                classifiers=[
                    'Development Status :: 4 - Beta',
                    'Programming Language :: Python :: 2',
                    'Programming Language :: Python :: 3',
                    'License :: OSI Approved :: MIT License',
                    'Operating System :: OS Independent',
                    'Intended Audience :: Science/Research',
                    'Topic :: Scientific/Engineering :: Bio-Informatics'
                ],
                install_requires=['numpy', 'pandas'],)
