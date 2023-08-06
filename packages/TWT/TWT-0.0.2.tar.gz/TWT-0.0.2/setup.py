import setuptools

with open("README.md",'r')as fh:
	long_description =fh.read()

setuptools.setup(
	name="TWT",
	version="0.0.2",
	author="Hunter-Ou",
	author_email="oy199603@qq.com",
	py_modules = ['TWT'],
	description="Dedicated in the SAR",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/UCAS-BigBird/TWT",
	packages=setuptools.find_packages(),
	python_requires='>=3.6',
)