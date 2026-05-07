import subprocess
import tempfile
import time
import os

prompt = 'Return ONLY a JSON array of job title keywords for Developer Advocate roles. Example format: ["keyword one", "keyword two"]. Give 20 keywords. No explanation, just the JSON array.'

start = time.time()

# Create completely clean environment
clean_env = {
    'PATH': os.environ.get('PATH', ''),
    'HOME': os.environ.get('HOME', ''),
    'USERPROFILE': os.environ.get('USERPROFILE', ''),
    'APPDATA': os.environ.get('APPDATA', ''),
    'LOCALAPPDATA': os.environ.get('LOCALAPPDATA', ''),
    'TEMP': os.environ.get('TEMP', ''),
    'TMP': os.environ.get('TMP', ''),
    'SystemRoot': os.environ.get('SystemRoot', ''),
    'SystemDrive': os.environ.get('SystemDrive', ''),
    'COMPUTERNAME': os.environ.get('COMPUTERNAME', ''),
    'USERNAME': os.environ.get('USERNAME', ''),
}

with tempfile.TemporaryDirectory() as tmpdir:
    r = subprocess.run(
        ['C:\\nvm4w\\nodejs\\claude.cmd', '-p', prompt],
        capture_output=True,
        text=True,
        timeout=120,
        shell=True,
        cwd=tmpdir,
        env=clean_env  # Clean environment - no project vars
    )

elapsed = time.time() - start
print(f'Time: {elapsed:.1f}s')
print(f'Code: {r.returncode}')
print(f'Output: {r.stdout[:500]}')
print(f'Error: {r.stderr[:200]}')