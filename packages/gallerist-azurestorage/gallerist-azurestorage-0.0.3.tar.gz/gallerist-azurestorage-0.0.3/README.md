[![Build Status](https://dev.azure.com/robertoprevato/Nest/_apis/build/status/RobertoPrevato.Gallerist-AzureStorage?branchName=master)](https://dev.azure.com/robertoprevato/Nest/_build/latest?definitionId=27&branchName=master) [![pypi](https://img.shields.io/pypi/v/gallerist-azurestorage.svg?color=blue)](https://pypi.org/project/gallerist-azurestorage/)

# Gallerist-AzureStorage
Gallerist classes for Azure Storage: implements reading image files from Azure Blob Service, and writing of resized pictures to the same.

```bash
$ pip install gallerist-azurestorage
```

This library is used in [Gallerist-AzureFunctions](https://github.com/RobertoPrevato/Gallerist-AzureFunctions), an Azure Functions front-end that uses [`Gallerist`](https://github.com/RobertoPrevato/Gallerist) library, to resize pictures
in Azure Storage Blob Service.
