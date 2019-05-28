#!/usr/bin/env python

import commands
import os
import ciscotelnet
import sys
import re
import yaml
import json
import ciscomapper
import logging



def save_config(hostname, ip_address, auth_token):
  """This function is called for each discovered cisco device
  and it will save device's configuration to the file named by device's hostname
  """
  with ciscotelnet.CiscoTelnet(ip_address, verbose=False) as cisco:
    if cisco.login(final_mode=auth_token["final_mode"], user=auth_token["user"], user_pass=auth_token["user_pass"], enable_pass=auth_token["enable_pass"], line_pass=auth_token["line_pass"]): 
      output = cisco.cmd("show running-config")
      if output:
        config = output
      else:
        raise(Exception("unable to get config from '%s' ('%s')"%(ip_address, hostname)))

      config = re.sub("ntp\s*clock-period\s*\d+", "", config) # otherwise config will be different periodically, this config line is not necessary to be saved

      filename = BACKUP_PATH + "/" + hostname + ".txt"
      fh = open(filename, "w")
      if fh:
        fh.write(config)
        fh.close()
    else:
      raise(Exception("unable to log in to '%s' ('%s')"%(ip_address, hostname)))



if __name__ == "__main__":
  #
  # Modify BACKUP_PATH and LOGGING_PATH variables for your requirements
  #
  BACKUP_PATH = "/var/backups/cisco-backup-git"
  LOGGING_PATH = "/var/log"

  ciscotelnet.WAIT_TIMEOUT = 60 # IMPORTANT, module requirement

  # the script will log to filename located in LOGGING_PATH and named as this script filename without extension plus .log:  
  logging.basicConfig(level=logging.DEBUG, format="%(asctime)s\t:%(message)s", filename=LOGGING_PATH+"/"+"".join(sys.argv[0].split("/")[-1].split(".")[:-1])+".log")


  if len(sys.argv)>=3:
    auth_choices_filename = sys.argv[1]
    start_ip = sys.argv[2]
  else:
    print "usage: %s auth_choices.conf START-IP"%(sys.argv[0])
    sys.exit(1)

  with open(auth_choices_filename, "r") as fh: 
    auth_choices = yaml.load(fh)


  devices_map = {} 
  try:
    ciscomapper.browse_cisco_network_breadth1st(start_ip, devices_map, [], auth_choices, verbose=True, call_for_every_device=save_config) # change to 'verbose=False' if you do not want any output
    #ciscomapper.browse_cisco_network_depth1st(start_ip, devices_map, [], auth_choices, verbose=True, call_for_every_device=save_config) # change to 'verbose=False' if you do not want any output
  except Exception as msg:
    logging.debug("ERROR, unable to browse network, msg='%s'"%(msg))
    sys.exit(1)
  
    
  cmd = "git --git-dir=%s/.git --work-tree=%s status"%(BACKUP_PATH, BACKUP_PATH)
  tup = commands.getstatusoutput(cmd)
  if tup[0]==0:
    output = tup[1]
  else:
    logging.debug("ERROR, unable to 'git status', err='%s'"%(tup[1]))
    sys.exit(1)

  if re.search("nothing\s+to\s+commit", output, re.MULTILINE|re.IGNORECASE):
    # no changes, good to exit
    sys.exit(0)

  filenames = set([])
  untracked_found = False
  untracked_start_space = False
  for line in output.split("\n"):
    m = re.search("modified:\s+(\S+)", line, re.IGNORECASE)
    if m:
      filenames.add(m.group(1))
      continue

    m = re.search("new file:\s+(\S+)", line, re.IGNORECASE)
    if m:
      filenames.add(m.group(1))
      continue
  
    if not untracked_found:
      m = re.search("Untracked\s+files:", line, re.IGNORECASE)
      if m:
        untracked_found = True
    else:
      m = re.search("^\s*$", line)
      if m:
        if untracked_start_space:
          untracked_found = False
        else:
          untracked_start_space = True
        continue

      if untracked_start_space:
        m = re.search("\s*(\S+)", line)
        if m:
          filenames.add(m.group(1))
  
  if not filenames:
    logging.debug("ERROR, changed files were not found in 'git status' output")
    sys.exit(1)

  if len(filenames)>3:
    changed_str = ", ".join(list(filenames)[0:3]) + "... changed"
  else:
    changed_str = ", ".join(list(filenames)) + " changed"

  cmd = "git --git-dir=%s/.git --work-tree=%s add *.txt"%(BACKUP_PATH, BACKUP_PATH)
  tup = commands.getstatusoutput(cmd)
  
  cmd = "git --git-dir=%s/.git --work-tree=%s commit -m '%s'"%(BACKUP_PATH, BACKUP_PATH, changed_str)
  tup = commands.getstatusoutput(cmd)

