from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(name='sphinxcontrib-coffee',
          version='0.1.1',
          license='BSD',
          author="Stephen Sugden",
          author_email="glurgle@gmail.com",
          description='Sphinx extension to add CoffeeScript support',
          platforms='any',
          packages=find_packages(),
          namespace_packages=['sphinxcontrib'])
