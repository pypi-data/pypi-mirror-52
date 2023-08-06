# easy-icm-runner :rocket:
Simplified Job Execution for IBM ICM v10 using REST APIs

https://developer.ibm.com/api/view/id-689:title-Incentive_Compensation_Management

## Installation:
```
pip install easy-icm-runner
```

## Usage:
This project can be used as a module within your custom program, or standalone from the command line.  Below we demonstrate sample usage:

### Python

The snippet below demonstrates running a job _syncronously_ in python code.  Such a method will be desirable for incorporating an ICM job step into a more complex application, or such tasks as integrating your own secret and configuration management.
```python
from icm_runner import exec_runner

username = 'username'
password = 'user password'
model_name = 'some model name'
process_name = 'some process name'
api_key = 'some api key'

#execute using api key
exec_runner(username=username,  model_name=model_name,
            process_name=process_name, api_key=api_key)
            
#execute using username and password
exec_runner(username=username, password=password, model_name=model_name,
            process_name=process_name)

```

### Command Line
For those of you who are not budding pythonistas, or just looking for a simple solution to job scheduling we also allow a command line entrypoint.   
```text
$ python -m icm_runner -u "icm username" -p "icm password" -m "model name" -j "process name"

$ python -m icm_runner -m "model name" -j "process name" -a "api key"
```
