from distutils.core import setup

with open('README.txt') as f:
    readme = f.read()

setup(
    name='qtpi_short',
    version='0.1.1',
    packages=['qtpi_short'],
    description='Simple example kernel for Jupyter',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Jupyter Development Team',
    author_email='jupyter@googlegroups.com',
    url='https://github.com/miroslav14/qtpi_short.git',
    install_requires=[
        'jupyter_client', 'IPython', 'ipykernel'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
    ],
)
