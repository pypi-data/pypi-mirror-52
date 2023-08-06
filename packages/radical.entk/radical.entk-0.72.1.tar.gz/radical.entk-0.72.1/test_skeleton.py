#!/usr/bin/env python

import os
from radical.entk import Pipeline, Stage, Task, AppManager

# ------------------------------------------------------------------------------
# Set default verbosity

# Assumptions:
# - # of MD steps: 2
# - Each MD step runtime: 15 minutes
# - Summit's scheduling policy [1]
#
# Resource rquest:
# - 4 <= nodes with 2h walltime.
#
# Workflow [2]
#
# [1] https://www.olcf.ornl.gov/for-users/system-user-guides/summit/summit-user-guide/scheduling-policy
# [2] https://docs.google.com/document/d/1XFgg4rlh7Y2nckH0fkiZTxfauadZn_zSn3sh51kNyKE/


def generate_training_pipeline():

    p = Pipeline()
    p.name = 'training'

    # --------------------------
    # MD stage
    s1 = Stage()
    s1.name = 'simulating'

    # MD tasks
    for i in range(2):
        t1 = Task()
        t1.executable = ['sleep']  # run_openmm.py
        t1.arguments  = ['6']

        # Add the MD task to the simulating stage
        s1.add_tasks(t1)

    # Add simulating stage to the training pipeline
    p.add_stages(s1)

    # --------------------------
    # Aggregate stage
    s2 = Stage()
    s2.name = 'aggregating'

    # Aggregation task
    t2 = Task()
    t2.executable = ['sleep']  # MD_to_CVAE.py
    t2.arguments  = ['3']

    # Add the aggregation task to the aggreagating stage
    s2.add_tasks(t2)

    # Add the aggregating stage to the training pipeline
    p.add_stages(s2)

    # --------------------------
    # Learning stage
    s3 = Stage()
    s3.name = 'learning'

    # learn task
    t3 = Task()
    t3.executable = ['sleep']  # train_cvae.py
    t3.arguments  = ['3']

    # Add the learn task to the learning stage
    s3.add_tasks(t3)

    # Add the learning stage to the pipeline
    p.add_stages(s3)

    return p


def generate_MDML_pipeline():

    p = Pipeline()
    p.name = 'MDML'

    # --------------------------
    # MD stage
    s1 = Stage()
    s1.name = 'simulating'

    # MD tasks
    for i in range(4):
        t1 = Task()
        t1.executable = ['sleep']  # MD executable
        t1.arguments  = ['6']

        # Add the MD task to the Docking Stage
        s1.add_tasks(t1)

    # Add Docking stage to the pipeline
    p.add_stages(s1)

    # --------------------------
    # Aggregate stage
    s2 = Stage()
    s2.name = 'aggregating'

    # Aggregation task
    t2 = Task()
    t2.executable = ['sleep']
    t2.arguments  = ['3']

    s2.add_tasks(t2)

    # Add MD stage to the MD Pipeline
    p.add_stages(s2)

    # --------------------------
    # Learning stage
    s3 = Stage()
    s3.name = 'inferring'

    # Aggregation task
    t3 = Task()
    t3.executable = ['sleep']  # CVAE executable
    t3.arguments  = ['3']

    s3.add_tasks(t3)

    # Add MD stage to the MD Pipeline
    p.add_stages(s3)

    return p


if __name__ == '__main__':

    # Create a dictionary to describe four mandatory keys:
    # resource, walltime, cores and project
    # resource is 'local.localhost' to execute locally
    res_dict = {
            'resource': 'local.localhost',
          # 'queue'   : 'batch',
            'schema'  : 'local',
            'walltime': 15,
            'cpus'    : 48,
            'gpus'    : 4
    }

    # Create Application Manager
    appman = AppManager(hostname='two.radical-project.org', port=5672)
  # appman = AppManager()
    appman.resource_desc = res_dict

    p1 = generate_training_pipeline()
    p2 = generate_MDML_pipeline()

    pipelines = []
    pipelines.append(p1)
    pipelines.append(p2)

    # Assign the workflow as a list of Pipelines to the Application Manager. In
    # this way, all the pipelines in the list will execute concurrently.
    appman.workflow = pipelines

    # Run the Application Manager
    appman.run()

