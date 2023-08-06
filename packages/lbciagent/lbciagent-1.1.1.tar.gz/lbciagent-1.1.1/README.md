General description
-------------------

This package is used to convert build ready end env ready messages to installations commands on CVMFS.
It is used on lbmessagingbroker. 

The nightlies installation deployment policy (priorities) can be found in DeploymentPolicy.py inside lbciagent package.
The order of slots used by the deployment policy is stored in `lbciagent/slotsOnCVMFS` 


Deployment policy update
------------------

* If you need to update the priorities order, please edit `lbciagent/slotsOnCVMFS`
* If you need to update the way the priorities are computed, please edit `lbciagent/DeploymentPolicy.py`.
This file also contains the list of the principal platform per slot.

After finishing your updates, please perform a manual visual test to confirm that the priorities are computed as you wanted:

* `python lbciagent/scripts/checkDeploymentPolicy.py <path to local clone of LHCbNightlyConf>` if you want to check against all the slots/platforms that should be produced for today. 
This requires LbNightlyTools to be included in the PYTHONPATH
* `python lbciagent/scripts/checkDeploymentPolicy.py` if you want to check against the slots/platforms already produced for today.


Release of new Deployment policy
------------------

* If you are satisfied with your updates, please create a merge request on gitlab.
* An extra run for `python lbciagent/scripts/checkDeploymentPolicy.py` is run in gitlabci staging phase. Please verify the result!
* After the merge was approved please deploy the new version (if you have root privileges on lbmessagingbroker):
    * `ssh lbmessagingbroker` 
    * `sudo -s -u lblocal` #change the user to lblocal
    * `cd /build/lbciagent/`
    * `source virtualenv/bin/activate` #activate the demon environment
    * `pip install --extra-index-url https://lhcb-pypi.web.cern.ch/lhcb-pypi/simple/ --trusted-host lhcb-pypi.web.cern.ch lbciagent --upgrade` #update the lbciagent
    * `exit`
    * `sudo -s`
    * `systemctl restart ciagent` #Restart the lbciagent

