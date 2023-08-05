from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='weather_forecast',
      version='0.49',
      description='Location based weather forecast package',
      long_description= long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/karthikziffer/weather_forecast',
      author='Karthik',
      author_email='karthik.cool1300@gmail.com',
      license='MIT',
      packages=['weather_forecast'],
      install_requires=[
          'geopy',
      ],
      zip_safe=False)