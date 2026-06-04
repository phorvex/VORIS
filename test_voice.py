import subprocess
result = subprocess.run(["mpg123", "--version"], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)