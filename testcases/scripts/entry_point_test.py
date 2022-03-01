import sys
import subprocess
import pytest

import japanese_media_manager.scripts.command as COMMAND

def test_help():
    cmd = [sys.executable, '-m', 'japanese_media_manager', '-h']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output, _ = process.communicate()
    assert 'usage: jmm' in output.decode('utf8')

@pytest.mark.parametrize('command', ['xxx', 'tiny-work', '2333'])
def test_wrong_command(command):
    cmd = [sys.executable, '-m', 'japanese_media_manager', command]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output, _ = process.communicate()

def test_none_command():
    cmd = [sys.executable, '-m', 'japanese_media_manager']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output, _ = process.communicate()
    assert 'usage: jmm' in output.decode('utf8')
