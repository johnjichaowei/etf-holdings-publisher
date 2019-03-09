import os
import json
import boto3
from botocore.exceptions import ClientError
from time import sleep

CFN_SUCCESS_STATES = [
    'CREATE_COMPLETE',
    'UPDATE_COMPLETE'
]
CFN_FAILURE_STATES = [
    'CREATE_FAILED',
    'ROLLBACK_FAILED',
    'ROLLBACK_COMPLETE',
    'UPDATE_ROLLBACK_FAILED',
    'UPDATE_ROLLBACK_COMPLETE',
    'DELETE_FAILED',
    'DELETE_COMPLETE'
]
STACK_MONITOR_INTERNAL = 3 # seconds

def deploy_stack(stack_name, template_file_path, params_file_path):
    print("Start to deploy stack {} with template file {} and params file {}".format(
        stack_name, template_file_path, params_file_path
    ))
    cfn = boto3.resource('cloudformation')
    payload = stack_payload(template_file_path, params_file_path)
    stack, last_stack_event = create_or_update_stack(cfn, stack_name, payload)
    monitor_statck_deployment(stack, last_stack_event)
    return stack

def create_or_update_stack(cfn, stack_name, payload):
    stack = find_stack(cfn, stack_name)
    last_stack_event = None
    if stack == None:
        print("Creating cloudformation stack: {}".format(stack_name))
        stack = cfn.create_stack(StackName=stack_name, **payload)
    else:
        print("Stack already exists, updating cloudformation stack: {}".format(stack_name))
        last_stack_event = next(iter(stack.events.all()))
        try:
            stack.update(**payload)
        except ClientError as err:
            if err.response['Error']['Code'] == 'ValidationError':
                print("No update is required for stack {}".format(stack_name))
            else: raise
    return (stack, last_stack_event)

def find_stack(cfn, stack_name):
    try:
        return next(s for s in cfn.stacks.all() if s.stack_name == stack_name)
    except StopIteration:
        return None

def stack_payload(template_file_path, params_file_path):
    template = load_template(template_file_path)
    params = load_params(params_file_path)
    return {
        'TemplateBody': template,
        'Parameters': params,
        'Capabilities': ['CAPABILITY_IAM']
    }

def load_template(template_file_path):
    with open(template_file_path) as f:
        return f.read()

def load_params(params_file_path):
    with open(params_file_path) as f:
        return json.load(f)

def monitor_statck_deployment(stack, last_stack_event):
    last_stack_event = render_stack_events(stack, last_stack_event)
    while True:
        if stack.stack_status in CFN_SUCCESS_STATES:
            print("Deploy cloudformation stack {} completed".format(stack.stack_name))
            break
        elif stack.stack_status in CFN_FAILURE_STATES:
            raise Exception(
                'Deploy cloudformation stack {} failed - {}'.format(
                    stack.stack_name, stack.status_reason
                )
            )
            break
        else:
            sleep(STACK_MONITOR_INTERNAL)
            stack.reload()
            last_stack_event = render_stack_events(stack, last_stack_event)

def render_stack_events(stack, last_stack_event):
    events_to_render, last_stack_event = get_events_to_render(stack, last_stack_event)
    [render_stack_event(e) for e in events_to_render]
    return last_stack_event

def get_events_to_render(stack, last_stack_event):
    if last_stack_event == None:
        events_to_render = [e for e in stack.events.all()]
    else:
        events_to_render = [
            e for e in stack.events.all() if e.timestamp > last_stack_event.timestamp
        ]

    events_to_render.sort(key=lambda event: event.timestamp)
    if len(events_to_render) > 0:
        last_stack_event = events_to_render[-1]

    return (events_to_render, last_stack_event)

def render_stack_event(e):
    status_reason = e.resource_status_reason
    if status_reason == None: status_reason = ''

    print("{time} {type}[{logical_id}] {status} {status_reason}".format(
        time=e.timestamp.isoformat(),
        type=e.resource_type,
        logical_id=e.logical_resource_id,
        status=e.resource_status,
        status_reason=status_reason
    ))
