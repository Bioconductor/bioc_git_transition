"""Bioconductor run git transition code.

This module assembles the classes for the SVN --> Git transition
can be run in a sequential manner.

It runs the following aspects fo the Bioconductor transition.

Note: Update the SVN dump

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

import src.run_transition as rt
import src.svn_dump_update as sdu
import logging
import time
logging.basicConfig(filename='transition.log',
                    format='%(levelname)s %(asctime)s %(message)s',
                    level=logging.DEBUG)

def svn_dump_update(config_file):
    sdu.svn_root_update(config_file)
    sdu.svn_experiment_root_update(config_file)

def run(config_file):
    rt.run_software_transition(config_file, new_svn_dump=True)
    rt.run_experiment_data_transition(config_file, new_svn_dump=True)
    rt.run_workflow_transition(config_file, new_svn_dump=True)
    rt.run_manifest_transition(config_file, new_svn_dump=True)
    rt.run_updates(config_file)
    return


if __name__ == '__main__':
    start_time = time.time()
    config_file = "./settings.ini"
    svn_dump_update(config_file)
    run(config_file)
    logging.info("--- %s seconds ---" % (time.time() - start_time))

