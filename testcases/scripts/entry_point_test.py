import sys
import subprocess
import pytest

def test_help():
    cmd = [sys.executable, '-m', 'japanese_media_manager', '-h']
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
        output, _ = process.communicate()
        assert 'usage: jmm' in output.decode('utf8')

@pytest.mark.parametrize('command', ['xxx', 'tiny-work', '2333'])
def test_wrong_command(command):
    cmd = [sys.executable, '-m', 'japanese_media_manager', command]
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
        output, _ = process.communicate()
        assert f"jmm: error: argument command: invalid choice: '{command}'" in output.decode('utf8')

def test_none_command():
    cmd = [sys.executable, '-m', 'japanese_media_manager']
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
        output, _ = process.communicate()
        assert 'usage: jmm' in output.decode('utf8')
