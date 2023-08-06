# DataStore

## Introduction

> File-based key-value data store that supports the basic CRD (create, read, and delete) operations. This data store is meant to be used as a local storage for one single process on one laptop.

## Installation

``` pip install python-file-datastore==0.1 ```

Additional Installation

``` pip install cachetools ```

Make sure you have python 3

## Usage:
    >>> from python-file-datastore import datastore_invoke 

#### General Instructions:

    >>> print(datastore_invoke(0)
    Operation Not FoundOperation_name  1 - Create (--client --key  --ttl(optional) --value) | 2 - Read (--client --key) | 3 - Delete (--client --key) | 4 - Reset (--client)

#### Create Operation

    >>> print(datastore_invoke(1, client = "hunch" , key = "employee_data", value = '{"employee":"siam"}' ))
    Create Operation Done

#### Create Operation with Time to Live feature

    >>> print(datastore_invoke(1, client = "hunch" , key = "employee_data_temp", value = '{"employee":"ragoish"}', ttl = 30 ))
    Create Operation Done

#### Read Operation

    >>> print(datastore_invoke(2, client = "hunch" , key = "employee_data"))
    For key | employee_data | value  - {'employee': 'siam'} 

#### Read Operation TTL Expired 

    >>> print(datastore_invoke(2, client = "hunch" , key = "employee_data_temp"))
    Error Status : TTL Value for the Key - employee_data_temp expired for the client - hunch

#### Delete Operation 

    >>> print(datastore_invoke(3, client = "hunch" , key = "employee_data"))
    Error Status : For key | employee_data | value - is deleted

#### Delete Operation TTL Expired

    >>> print(datastore_invoke(3, client = "hunch" , key = "employee_data_temp"))
    Error Status : TTL Value for the Key - employee_data_temp expired for the client - hunch

#### Reset Operation - Delete Entire file

    >>> print(datastore_invoke(4, client = "hunch" ))
    File removed!!!! - hunch
