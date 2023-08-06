from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='weng-pkgtest',
    version='1.0.0',
    packages=['weng_pkgtest'],
    # packages=setuptools.find_packages(),
    zip_safe=False,
    include_package_data=True,
    url='https://github.com/MutiYouth',
    license='GPL',
    author='Cheetah',
    author_email='murphe@qq.com',
    keywords='weng,test',
    description='a python package test project',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
