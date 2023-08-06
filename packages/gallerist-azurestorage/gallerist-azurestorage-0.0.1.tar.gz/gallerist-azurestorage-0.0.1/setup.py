from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='gallerist-azurestorage',
      version='0.0.1',
      description='Azure Storage file store for Gallerist',
      long_description=readme(),
      long_description_content_type='text/markdown',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Operating System :: OS Independent'
      ],
      url='https://github.com/RobertoPrevato/Gallerist-AzureStorage',
      author='RobertoPrevato',
      author_email='roberto.prevato@gmail.com',
      keywords='pictures images web azure storage',
      license='MIT',
      packages=['galleristazurestorage'],
      install_requires=['gallerist',
                        'azure-storage-blob'],
      include_package_data=True,
      zip_safe=False)
