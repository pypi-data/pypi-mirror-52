[![Build Status](https://travis-ci.org/rienafairefr/pyynab.svg?branch=master)](https://travis-ci.org/rienafairefr/pyynab)
[![Coverage Status](https://coveralls.io/repos/github/rienafairefr/pyynab/badge.svg?branch=master)](https://coveralls.io/github/rienafairefr/pyynab?branch=master)

# pyynab
Library to connnect to the You neeed a Budget Public API.


It uses the public Swagger file [here](https://api.youneedabudget.com/papi/spec-v1-swagger.json)
and [openapi-generator](https://github.com/OpenAPITools/openapi-generator/)

In the swagger file, some parameters accept `null` asvalues but are not marked as nullable,
to te Swagger spec needed some pre-processin: First it is converted to OpenApi 3, then patched with `path_openapi.py`
, then a `python` client is generated using openapi-generator v3 

See the doc of the auto-generated package in its own README.md