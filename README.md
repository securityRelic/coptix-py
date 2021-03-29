# coptix-py
Sophos Cloud Optix Automation with Python

## Overview

Notes and code guidance for automating the use of the Sophos Cloud Optix REST API

## Scope

- Infrastructure as Code (IaC) Integration endpoints
  - Scan: POST api/v1/iac/scan

## Vendor Documentation 

[Getting Started With Cloud Optix REST API](https://optix.sophos.com/apiDocumentation)

[Sophos Cloud Optix Documentation](https://docs.sophos.com/pcg/optix/help/en-us/index.html)

[Cloud Optix](https://www.sophos.com/en-us/products/cloud-optix.aspx)

## Endpoints

### IaC Integration - Scan

> Endpoint: api/v1/iac/scan \
> Method: POST \
> Produces: applicaiton/json

#### Notes

- Code/function example only handles manatory/default query parameters
  - [Query parameter documention](https://optix.sophos.com/apiDocumentation#iac)
- IaC templates will be procesed asynchronouly (Default)
  - Synchronous communication avaliable with optional query parameter
  - Optional query parameter: 'async'
- Authorization header requires '<type>': 'ApiKey'
  - example: 'Authorization: ApiKey xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
- As part of the mutipart file construction, key for earch file needs to be consistant: 'files'
  - example: = [('files', (<file1>, open(<file1>, 'rb')), 'files', (<file2>, open(<file2>, 'rb')))]
- Option to specify policy, otherwise 'default' is leveraged
  - Optional query parameter: 'policy_name'

#### Use of Example Function:
  
  ```py
  my_files = [('files', (<file1>, open(<file1>, 'rb')), 'files', (<file2>, open(<file2>, 'rb')))]
  my_key = <-- from a secure spot ;)
  my_scan_id = iac_scan(my_files, my_key)

  ```

#### API return examples

Success

```json
200
{"scan_id":"999999a9-9999-999a-9a9a-99999a99a9a9a9","summary":null}

```

AuthN Failure 

```py
401
Unauthorized access or ApiKey expired
```

#### Optional Params

```
    params = {'async': params_async,
            'policy_name': params_policy,
            'repo_url': params_repo,
            'branch': params_branch,
            'committer_name': params_cname,
            'committer_email': params_cemail,
            'save_results_to_account': params_save}

```
