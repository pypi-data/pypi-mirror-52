## anna client

### setup
```$ pip install anna-client```

### usage
#### initialization
```python
from anna_client.client import Client

client = Client(endpoint='http://localhost:5000/graphql')
```
#### get jobs
```python
# get all job ids
jobs = client.get_jobs()
# you can specify a where clause & the fields you wish to receive
jobs = client.get_jobs(where={'id_in', [...]}, fields=('driver','site','status'))
```
#### create jobs
```python
# create_jobs takes a list of dicts describing your jobs
jobs = client.create_jobs(data=[{'driver': 'firefox', 'site': 'test'}])
```
#### delete jobs
```python
# provide no parameters in order to delete all jobs
client.delete_jobs(where={})
# or delete specific jobs
client.delete_jobs(where={'id_in': my_jobs})
```
#### update jobs
```python
# provide no where parameter in order to update all jobs
client.update_jobs(data={'status': 'STOPPED'})
# or update specific jobs
client.delete_jobs(where={'id_in': my_jobs}, data={'status': 'STOPPED'})
```
#### reserve jobs
```python
# reserve_jobs takes a worker and a tuple of job ids
client.reserve_jobs(worker='worker', job_ids=my_jobs)
```
#### get tasks
```python
# get_tasks takes a namespace & returns a url and a list of tuples containing the task names & definitions
url, tasks = client.get_tasks(namespace='test')
```
