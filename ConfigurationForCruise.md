#This page shows how to create configuration file for Cruise builds

# How to configure #

1. File name:

```
[pipeline_name]__[stage_name]__[job_name].cfg or [pipeline_name]__[stage_name].cfg 
```
> Now only job level and stage level project are supported.

2. File content：
```
    [Basic]
    type: Cruise
    baseurl:  http://[cruise_host]:[cruise_port]/cruise
```