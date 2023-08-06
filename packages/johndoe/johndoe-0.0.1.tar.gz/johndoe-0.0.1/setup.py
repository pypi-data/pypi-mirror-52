import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()
	
setuptools.setup(
	name="johndoe",
	version="0.0.1",
	author="akingscote",
	author_email="ashleykingscote@hotmail.co.uk",
	description="package for testing package installation process",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://gitlab.com/Kingscote",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	install_requires=[
          'psutil'
    ],
	python_requires='>=3.4',
)