#test subprocess check_output
import subprocess as sb 
a=sb.check_output("ls")
print(a.decode("utf-8"))