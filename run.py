"""Bioconductor run git transition code.

This module assembles the classes for the SVN --> Git transition
can be run in a sequential manner.

It runs the following aspects fo the Bioconductor transition.

1. Run Bioconductor Software package transition
2. Run Bioconductor Experiment Data package transition
3. Run Workflow package transition
4. Run Manifest file transition
5. Run Rapid update of master (trunk) and RELEASE_3_5 branches on
   software packages

Manual tasks which need to be done:
1. Copy over bare repos to repositories/packages
2. Copy manifest bare git repo to repositories/admin
"""

import run_transition as rt


def run():
    config_file = "./settings.ini"
    rt.run_manifest_transition(config_file, new_svn_dump=False)
    rt.run_software_transition(config_file, new_svn_dump=False)
    rt.run_experiment_data_transition(config_file, new_svn_dump=False)
    rt.run_workflow_transition(config_file, new_svn_dump=False)
    rt.run_updates(config_file)
    return


if __name__ == '__main__':
    run()
