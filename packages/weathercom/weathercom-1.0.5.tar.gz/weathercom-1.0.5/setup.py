from setuptools import setup, Extension
def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="weathercom",
    version="1.0.5",
    description="A Python package to get weather reports for any location from weather.com. API for weather.com",
    long_description=readme(),
	long_description_content_type='text/markdown',
	url="https://github.com/prashanth-p/weathercom/",
    author="Prashanth Pradeep",
    author_email="prashanth.pradeep96@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["weathercom"],
    include_package_data=True,
    keywords = ['weather','weather.com','python weather','weatherpy','yahoo weather','google weather','open weather python','weather api', 'weather api json'],
)