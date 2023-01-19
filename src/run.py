import subprocess
import time
import os
import signal

for i in range(10):
    
    cmd = "nohup python3.7 main_5_nltcs.py >out1.txt >std1.err"
   
    pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid) 
                       
    cmd = "nohup python3.7 main_3_plants.py >out2.txt >std2.err"
   
    pro1 = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid) 
                       
    cmd = "nohup python3.7 main_3_baudio.py >out3.txt >std3.err"
   
    pro2 = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid) 
                       
    cmd = "nohup python3.7 main_3_bnetflix.py >out4.txt >std4.err"
   
    pro3 = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid) 
    time.sleep(100)                   
    cmd = "nohup python3.7 main_3_nltcs.py >out5.txt >std5.err"
   
    pro4 = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid) 
    time.sleep(900)
    os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
    os.killpg(os.getpgid(pro1.pid), signal.SIGTERM)
    os.killpg(os.getpgid(pro2.pid), signal.SIGTERM)
    os.killpg(os.getpgid(pro3.pid), signal.SIGTERM)
    os.killpg(os.getpgid(pro4.pid), signal.SIGTERM)
    time.sleep(10)
        