import os
import subprocess

def check_path_exist(path):
    if not os.path.exists(path):
        raise Exception("path {} not found".format(path))

def remove_local_file(path):
    if os.path.exists(path):
        os.remove(path)

def remove_directiry(path):
    if os.path.exists(path):
        os.system("rm -rf %s"%path)

def scp (identity_file, source, target, user, host, verbose = False):
    cmd = 'scp -q -o "StrictHostKeyChecking no" -o "UserKnownHostsFile=/dev/null" -i %s -r "%s" "%s@%s:%s"' % (identity_file, source, user, host, target)
    if verbose:
        print(cmd)
    try:
        output = subprocess.check_output( cmd, shell=True )
    except subprocess.CalledProcessError as e:
        output = "Return code: " + str(e.returncode) + ", output: " + e.output.strip()
    print(output)

def SSH_exec_cmd_with_output(identity_file, user,host,cmd, supressWarning = False,verbose=False):
    if len(cmd)==0:
        return ""
    if supressWarning:
        cmd += " 2>/dev/null"
    execmd = """ssh -o "StrictHostKeyChecking no" -o "UserKnownHostsFile=/dev/null" -i %s "%s@%s" "%s" """ % (identity_file, user, host, cmd )
    if verbose:
        print(execmd)
    try:
        output = subprocess.check_output( execmd, shell=True )
    except subprocess.CalledProcessError as e:
        output = "Return code: " + str(e.returncode) + ", output: " + e.output.strip()
    # print output
    return output