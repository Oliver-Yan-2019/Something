broker_url = 'redis://localhost:6379//'
result_backend = 'redis://localhost:6380'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Asia/Shanghai'
enable_utc = True
result_expires = 3600

# task_routes = {
#     'tasks.add': 'low-priority',
# }
#
# task_annotations = {
#     'tasks.add': {'rate_limit': '10/m'}
# }

beat_schedule = {
    'exec_periodic_task': {
        'task': 'tasks.exec_periodic_task',
        'schedule': 10,
        'args': (),
        'kwargs': {},
        'options': {
            'queue': 'default'
        },
        'relative': False
    },
}
