import subprocess
import time
import os
import signal

for i in range(10):


    
    cmd = "nohup python3.7 main_5_tretail.py >out6.txt >std6.err"
   
    
    pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid) 
    
                      
    cmd = "nohup python3.7 main_5_plants.py >out7.txt >std7.err"
   
    pro1 = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid) 
                       
    cmd = "nohup python3.7 main_5_baudio.py >out8.txt >std8.err"
   
    pro2 = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid) 
                      
    cmd = "nohup python3.7 main_5_bnetflix.py >out9.txt >std9.err"
   
    pro3 = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid) 
    
   
                       
    cmd = "nohup python3.7 main_3_tretail.py >out10.txt >std10.err"
    time.sleep(300)
    pro4 = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid) 
    time.sleep(2200)
    os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
    os.killpg(os.getpgid(pro1.pid), signal.SIGTERM)
    os.killpg(os.getpgid(pro2.pid), signal.SIGTERM)
    os.killpg(os.getpgid(pro3.pid), signal.SIGTERM)
    os.killpg(os.getpgid(pro4.pid), signal.SIGTERM)
    
    time.sleep(10)
        