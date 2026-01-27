# Day 3 - Working with an IP Core
Dawnstar is preparing a new [IP core](https://en.wikipedia.org/wiki/Semiconductor_intellectual_property_core), the Dawnstar FIR Filter, which can be used to filter signals. It has various features and configuration options described in its Highest-level Architecture Specification (HAS) file, which has also been added to this repository.

One of its main features is its Debugger CLI, which meant you can access this IP using the command line.

For example, as described by the UART Debugger CLI document, you can reset the IP, assert enable, and then read its Control and Status Register (CSR) by using the following commands:

```console
you@dawnstar.local:~$ ./impl0 com --action reset
you@dawnstar.local:~$ ./impl0 com --action enable
you@dawnstar.local:~$ ./impl0 cfg --address 0x0
0x00000000
```

Fortunately, Python has the `os` library, which provides a way of executing such operations. The following Python code is equivalent to the 3 commands above.

```python
import os

os.system(f"./impl0 com --action reset")
os.system(f"./impl0 com --action enable")
os.system(f"./impl0 cfg --address --address 0x0")
```

```console
you@dawnstar.local:~$ python example.py
0x00000000
```

Try out the IP core's CLI Debugger feature by going into the same directory as the IP instances (`impl0` to `impl5`) and running the commands.

Read the two documents to figure out what commands need to be run, try it, and then use Python to automate it. 

***NOTE:*** **If running `./impl0` doesn't work, try `impl0` without the `./`. If it still doesn't work for you on your laptop, you can try doing the assignment on the remote server. Check `/home/emmanuella.pv@oppstar.local/PYTHON_TRAINING/insts` (read the README!).**

## Assignment instructions
The FIR filter IP can be reset, enabled, disabled, halted, set to bypass mode, overflown, and cleared by writing to its register.

Once it has been halted, it will start storing sampled input signals in its buffer, as shown by its increasing buffer count. It can store up to 255 samples before it starts to overflow and needs to be cleared. 

You have been given `main.py` with some code to work with.

Modify it so that for each instance in `["impl0", "impl1", "impl2", "impl3", "impl4", "impl5"]`, it gives the necessary commands that need to be run to check:
1. Whether global enable/disable works
    - Example: The Python program resets and enables the IP, then tries to read its registers, then disables the IP, then tries to read again
2. Whether filter bypass works
    - Example: The program activates the bypass feature and prints the input and output of the IP
3. Whether the filter buffer works as expected
   * Set the filter to a halted state and start storing to its input buffer. Is the input buffer count correct?
       - Example: Program sets state to halted, inputs a value, then prints the buffer count
   * When it starts overflowing after more than 255 samples, is the correct register field set?
   * Can the input buffer count be cleared successfully?

## Submitting the assignment
- Click "Fork" (upper right, above "Add file" and "Code") 
- Create fork without changing any of the settings
- Go to hello-world.py and modify it according to the instructions.

Note: You can refer to using-github-and-autograder.pdf in /home/emmanuella.pv@oppstar.local/PYTHON_TRAINING/ after you connect to Remote Server `10.80.10.25`. Although the "Using Autograder" part is no longer applicable since we are no longer using GitHub Classroom, the "Using GitHub" part is still applicable. 

You can refer to `using-github-and-autograder.pdf` in `/home/emmanuella.pv@oppstar.local/PYTHON_TRAINING/` after you connect to Remote Server `10.80.10.25`.
