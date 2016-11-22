from setuptools import setup, find_packages

setup(
    name='srunctl',
    version='1.0.0',
    packages=find_packages(),
    install_requires=['argparse >= 1.1'],
    url='https://github.com/stkevintan/srunctl',
    license='MIT',
    author='Kevin Tan',
    author_email='stkevintan@zju.edu.cn',
    description='srun3000 network controller',
    entry_points={
        'console_scripts': [
            'srunctl=srunctl:main'
        ]
    }
)
