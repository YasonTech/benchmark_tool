from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities    
from time import sleep
import Tkinter
import sys
import os
import argparse
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

base_dir = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file_path")
parser.add_argument("-u","--url")
args = parser.parse_args()

if len(sys.argv) > 1:
    if args.url:
        url = args.url
    elif args.file_path:
        abs_path = os.path.abspath(args.file_path)
        url = "file:///"+abs_path
    else: 
        sys.exit("expected either --url or --file_path arg")
else:
    url = "https://google.com"

driver = webdriver.Chrome()
driver.get(url)

execution_time = driver.execute_script("return performance.timing.loadEventEnd - performance.timing.navigationStart;")
driver.quit()
print ("load time: " + str(execution_time/1000.0))

chrome_options = Options()
caps = DesiredCapabilities.CHROME
caps['loggingPrefs'] = { 'browser':'ALL' }

chrome_options.add_extension(base_dir + "/metricExtension.crx")
chrome_options.add_argument("--enable-precise-memory-info")
driver = webdriver.Chrome(chrome_options=chrome_options,desired_capabilities=caps)

driver.get(url)
execution_time = driver.execute_script("return performance.timing.loadEventEnd - performance.timing.navigationStart;")

print ("milliseconds with injected mem usage script:" + str(execution_time))

heap_status = driver.execute_script("return window.performance.memory;")

print ("heap_status:" + str(heap_status))

usedMem = []
totalMem = []
maxMem = []

log_count = 0
log_max = 1000
sleep(4)
while log_count < log_max:
    sleep(1)
    print log_count
    for entry in driver.get_log('browser'):
        data = entry['message']
        sig = 'heap data='
        if sig in data:
            index = data.index(sig)
            offset = len(sig)
            vals = data[index + offset:-1].split(',')
            usedMem.append(int(vals[0]))
            totalMem.append(int(vals[1]))
            maxMem.append(int(vals[2]))
            log_count += 1
            if log_count >= log_max:
                break
        
t = np.asarray(xrange(len(usedMem)))

print "run time with extenion: " + str(execution_time) + "ms"

# generate consumption graph
plt.plot(t, usedMem, 'b-', t, totalMem, 'r--')
plt.locator_params(nbins=20, axis='y')
plt.suptitle('Memory Consumption', fontsize=14, fontweight='bold')
plt.xlabel('milliseconds')
plt.ylabel('bytes')
red_patch = mpatches.Patch(color='red', label='Total Heap Size')
blue_patch = mpatches.Patch(color='blue', label='Used Heap Size')
plt.legend(handles=[red_patch, blue_patch])

plt.savefig("graph.png")
plt.show()

driver.quit()
