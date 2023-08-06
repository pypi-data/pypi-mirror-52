from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='bali',
    version='0.0.1',
    description='lombok for python',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='mtngt',
    author_email='mtngtio@gmail.com',
    keywords=['Python 3'],
    url='https://github.com/mtngt/bali',
)

install_requires = []

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
