#!/usr/bin/env python3

import os
import sys
import subprocess


class BadRCError(Exception):
    pass


def run_command_orig(cmd):
    """ No idea how th f to get this to work """
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode == 0:
        os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
    else:
        raise BadRCError("Bad rc (%s) for cmd '%s': %s" % (process.returncode, cmd, stdout + stderr))
    return stdout


def parameters(args):
    parameter_str = ''
    for arg in args:
        parameter_str += arg + ' '
    return parameter_str



# Method 1:  Call --------------------------------------------------------------

    # can't process stdout stream
    # CAN perform user interface operations for interaction


cmd = 'sudo sh rkinstaller.sh ' + parameters(sys.argv[1:])

subprocess.call(
        [cmd], shell=True,
        cwd=os.getcwd() + '/' + 'rkhunter'
        )

sys.exit(0)


# Method 2: subprocess.Popen  --------------------------------------------------

    # - can process output if required
    # - Need to know how to SIGINT after execution -- shell script retains control



process = subprocess.Popen(
    [cmd],
    shell=True,
    cwd='/home/blake/git/Security/gensec/rkhunter',
    universal_newlines=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT
    )

with process.stdout:
    for line in iter(process.stdout.readline, b''):
        sys.stdout.write(line)
        sys.stdout.flush()
    if process.returncode == 0:
        os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
        #process.kill()      # DOES NOT WORK
    else:
        raise BadRCError("Bad rc (%s) for cmd '%s': %s" % (p.returncode, cmd, stdout + stderr))


# Method 3: subprocess.Popen  --------------------------------------------------

    # - can process output if required?
    #

out, err = subprocess.Popen([cmd], stdout=subprocess.PIPE).communicate()


# Method 4: subprocess.Popen  --------------------------------------------------

    # - can process output if required?
    #

r = subprocess.Popen(['ls','-l'], stdout=subprocess.PIPE)
out = r.stdout.readlines()

# or, if you want to read line-by-line (maybe the other process is more intensive than ls):

for ln in ls.stdout:
    # process each line of output individually
