"""Tests for the pre-receive hook to check version numbers."""

import subprocess
import re
import os
import pytest
from hooks.prevent_bad_version_numbers import check_version_bump


CWD = "/Users/ni41435_ca/Documents/bioc_git_transition/hooks/repo-specific/test_proj"
DESC = "DESCRIPTION"


def change_version(new_version, cwd=CWD):
    filename = DESC
    path = os.path.join(cwd, filename)
    s = open(path).read()
    x = re.sub(r"Version: .+\n", "Version: " + new_version + "\n", s)
    f = open(path, 'w')
    f.write(x)
    f.close()
    return

def git_add(path, cwd=CWD):
    cmd = ['git', 'add', path]
    subprocess.check_call(cmd, cwd=cwd)
    return

def git_checkout(branch, cwd=CWD):
    cmd = ['git', 'checkout', branch]
    subprocess.check_call(cmd, cwd=cwd)
    return

def git_commit(message, cwd=CWD):
    cmd = ['git', 'commit', '-m', message]
    subprocess.check_call(cmd, cwd=cwd)
    return

def git_push(cwd=CWD):
    cmd = ['git', 'push']
    out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    return out

def test_master_check_version_bump():
    # Master
    refname = "master"
    # y should be odd
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        check_version_bump("0.25.1", "0.26.1", refname)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1

    # x should not change
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        check_version_bump("0.25.1", "1.25.1", refname)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1

    #  z should change by increment only
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        check_version_bump("0.25.5", "0.25.4", refname)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1

    # z can be 99
    res = check_version_bump("0.25.4", "0.99.0", refname)
    assert res == None

    return


def test_release_check_version_bump():
    refname = "RELEASE_3_6"
    # y should be even
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        check_version_bump("0.26.1", "0.27.1", refname)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1
    # x should not change
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        check_version_bump("0.26.1", "1.26.1", refname)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1
    # x should not change, even if y changes, it should
    # throw the same error.
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        check_version_bump("0.25.1", "1.25.1", refname)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1
    # z should not decrement
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        check_version_bump("0.26.4", "0.25.3", refname)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1

    # z can be 99
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        res = check_version_bump("0.26.4", "0.99.0", refname)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1
    return

def test_integration_version_bump_in_master():
    refname = "master"
    change_version("1.25.61")
    git_add(DESC)
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        change_version("2.25.61")
        git_add(DESC)
        git_commit("Fail test", cwd=CWD)
        out = git_push()
        assert "error" in out
        assert pytest_wrapped_e.value.code == 1
