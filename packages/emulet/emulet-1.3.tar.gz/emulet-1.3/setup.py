from setuptools import setup

def readme_file_contents():
	with open('README.rst') as readme_file:
		data = readme_file.read()
	return data


setup(
	name='emulet',
	version='1.3',
	description='TCP HoneyPot',
	long_description=readme_file_contents(),
	long_description_content_type='text/markdown',
	author='vikas',
	author_email='vikas4sharma4@gmail.com',
	licence='MIT',
	packages=['emulet'],
	zip_safe=False,
	install_requires=[]
)	 

