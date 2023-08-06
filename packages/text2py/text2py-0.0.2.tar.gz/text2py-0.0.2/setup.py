from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()



setup(
    name='text2py',
    version='0.0.2',
    packages=find_packages(),
    url='https://gitlab.com/omaxx/text2py',
    license='MIT License',
    author='maxim orlov',
    author_email='maxx.orlov@gmail.com',
    description='Library for processing structured text into python object (dict or list) using templates',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
                'Development Status :: 3 - Alpha',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.5',
                'Programming Language :: Python :: 3.6',
                'Programming Language :: Python :: 3.7',
                'License :: OSI Approved :: MIT License',
                'Operating System :: OS Independent',
                ],
    python_requires='>=3.5',
    install_requires=['PyYAML'],
    entry_points={
        'console_scripts': [
            'text2py=text2py:run',
        ],
    },
)
