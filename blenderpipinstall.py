import subprocess
import ensurepip
import sys
ensurepip.bootstrap()
pybin = sys.executable
subprocess.check_call([pybin, '-m', 'pip', 'install', 'pip','--upgrade'])
subprocess.check_call([pybin, '-m', 'pip', 'install', 'sympy'])
subprocess.check_call([pybin, '-m', 'pip', 'install', 'pandas'])
subprocess.check_call([pybin, '-m', 'pip', 'install', 'openpyxl'])