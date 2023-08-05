

DDNS For AWS
============

Tool to Sync your external IP address with an A Record in Route 53

Usage
-----

- Install AWS CLI and add your credentials
- Run "pip install -e ." in the programs parent directory
- Run commmand 'set-ddnsaws' with DNS Name and Hosted Zone ID arguments.
- Or Configure JSON and run with just the command.
- Cronjob the command to run every 15 minutes.



Examples
--------

Example to upload with CLI arguments::

  set-ddnsaws -DNSName "blog.example.com" -HostedZoneId "000aaa00"

Example to upload config.josn arguments::

  set-ddnsaws
