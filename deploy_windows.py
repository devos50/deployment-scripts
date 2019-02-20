"""
This script fetches the latest build executable for Win64 from Jenkins
and installs it. Note that it expects the following environment
variable:
- JENKINS_JOB_URL : Jenkins job which builds the Debian package
- BUILD_TYPE : Build type [Win64, Win32, Linux, MacOS]
- WORKSPACE : Jenkins workspace (set by jenkins itself)
"""
from __future__ import print_function
import os
import time

from deployment_utils import fetch_latest_build_artifact, print_and_exit, tribler_is_installed, check_sha256_hash

if __name__ == '__main__':
    start_time = time.time()

    # Step 1: fetch the latest Tribler installer from Jenkins
    build_type = os.environ.get('BUILD_TYPE', 'Win64')
    job_url = os.environ.get('JENKINS_JOB_URL', None)
    if not job_url:
        print_and_exit('JENKINS_JOB_URL is not set')

    INSTALLER_FILE, HASH = fetch_latest_build_artifact(job_url, build_type)

    # Step 2: check SHA256 hash
    if not check_sha256_hash(INSTALLER_FILE, HASH):
        print_and_exit("SHA256 of file does not match with target hash %s" % HASH)

    # Step 3: run the installer
    os.system("%s /S" % INSTALLER_FILE)

    diff_time = time.time() - start_time
    print('Installed Tribler in %s in %s seconds' % (build_type, diff_time))
    time.sleep(1)

    # Step 4: check whether Tribler has been correctly installed
    if not tribler_is_installed():
        print_and_exit('Tribler has not been correctly installed')
