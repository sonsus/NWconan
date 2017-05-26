#test subprocess check_output
import subprocess as sb 
a=sb.check_output("top -n 1", shell=True).decode("utf-8")
with open("out.txt","w") as f:
	f.write(a)
print("open out.txt")
sb.run("cat out.txt", shell=True)