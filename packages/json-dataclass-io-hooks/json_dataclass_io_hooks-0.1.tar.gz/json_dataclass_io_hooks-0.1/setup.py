from os import path
from setuptools import setup, find_packages

dirname = path.abspath(path.dirname(__file__))
with open(path.join(dirname, 'README.md')) as f:
    long_description = f.read()

setup(
    name='json_dataclass_io_hooks',
    version=0.1,
    packages=find_packages(),
    description='JSON encoder/decoder hooks for Python dataclasses',
    url='https://github.com/datalyticsbe/json_dataclass_io_hooks/',
    license='MIT',
    author='Datalytics BVBA',
    author_email='datalyticsbe@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7'
    ],
    install_requires=open('requirements.txt').readlines(),
    python_requires='>=3.7',
    keywords='JSON, dataclass, dataclasses, save, load, store, hooks, convert, dict',
    include_package_data=True,
    long_description_content_type="text/markdown",
    long_description=long_description,
)
