# Isogeo - XLSX Exporter

[![PyPI](https://img.shields.io/pypi/v/isogeo-export-xl.svg?style=flat-square) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/isogeo-export-xl?style=flat-square)](https://pypi.org/project/isogeo-export-xl/)

[![Build Status](https://dev.azure.com/isogeo/PythonTooling/_apis/build/status/isogeo.export-xlsx-py?branchName=master)](https://dev.azure.com/isogeo/PythonTooling/_build/latest?definitionId=23&branchName=master) ![Azure DevOps coverage](https://img.shields.io/azure-devops/coverage/isogeo/PythonTooling/23?style=flat-square)

[![Documentation Status](https://readthedocs.org/projects/isogeo-export-xlsx-py/badge/?version=latest)](https://isogeo-export-xlsx-py.readthedocs.io/en/latest/?badge=latest) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

Python package to export Isogeo metadata into Excel workshbook using the [Python SDK](https://pypi.org/project//isogeo-export-xl/) and [Openpyxl](https://pypi.org/project/openpyxl/).

## Usage in a nutshell

1. Install:

    ```powershell
    pip install isogeo-export-xl
    ```

2. Authenticate

    ```python
    # import
    from isogeo_pysdk import Isogeo
    # API client
    isogeo = Isogeo(
        auth_mode="group",
        client_id=ISOGEO_API_GROUP_CLIENT_ID,
        client_secret=ISOGEO_API_GROUP_CLIENT_SECRET,
        auto_refresh_url="{}/oauth/token".format(ISOGEO_ID_URL),
        platform=ISOGEO_PLATFORM,
    )

    # getting a token
    isogeo.connect()
    ```

3. Make a search:

    ```python
    search = isogeo.search(include="all",)
    # close session
    isogeo.close()
    ```

4. Export:

    ```python
    # import
    from isogeotoxlsx import Isogeo2xlsx
    # instanciate the final workbook
    out_workbook = Isogeo2xlsx(
        lang=isogeo.lang,
        url_base_edit=isogeo.app_url,
        url_base_view=isogeo.oc_url
    )
    # add needed worksheets
    out_workbook.set_worksheets(auto=search.tags.keys())

    # parse search results
    for md in map(Metadata.clean_attributes, search.results):
        out_workbook.store_metadatas(md)

    # save file
    out_workbook.save("./isogeo_export_to_xlsx.xlsx")
    ```
