##################################################
# Modify the code below 

# Set CSR.HALT to 1 and enable the coefficients ...
# Sample a few times ...
# Intentionally sample more than a total of 255 times ...
# Try clearing the buffer ...
# Turn on bypass ...
# Check whether filter bypassing is successful ...
##################################################

import os
import subprocess

def read_csr(unit):
    output = os.popen(f"impl{unit}.exe cfg --address 0x0").read().strip()
    return int(output, 16)

def write_csr(unit, value):
    os.system(f"impl{unit}.exe cfg --address 0x0 --data {hex(value)}")

def drive_signal(unit, value, count=1, silent=True):
    for _ in range(count):
        if silent:
            subprocess.run(
                f"impl{unit} sig --data {hex(value)}",
                shell=True,
                stdout=subprocess.DEVNULL,
            )
        else:
            os.system(f"impl{unit}.exe sig --data {hex(value)}")


# ===============================
# Q1: Global enable / disable test
# ===============================
print("\n=== Q1: Global enable/disable test ===")

os.system("impl0.exe com --action reset")
os.system("impl0.exe com --action enable")

print("CSR after enable:")
print(hex(read_csr(0)))

os.system("impl0.exe com --action disable")

print("CSR read after disable (may fail or return nothing):")
try:
    print(hex(read_csr(0)))
except ValueError:
    print("CSR not readable when IP is disabled (expected behavior)")

# q2 - q3
for i in range(6):

    print(f"\n==============================")
    print(f" Running test for CHIP {i}")
    print(f"==============================")

   
    # Reset chip
    os.system(f"impl{i}.exe com --action reset")

    # Enable chip
    os.system(f"impl{i}.exe com --action enable")

    # ---- HALT AND ENABLE COEFFICIENT ----
    csr = read_csr(i)
    csr |= (1 << 5)          # HALT = 1
    csr |= (0b1111 << 1)     #enable coefficient
    write_csr(i, csr) 

    # ---- CLEAR BUFFER  ----
    csr = read_csr(i)
    csr |= (1 << 17)         # IBCLR = 1
    write_csr(i, csr)

    csr = read_csr(i)
    csr &= ~(1 << 17)        #IBCLR = 0
    write_csr(i, csr)

    csr = read_csr(i)
    ibcnt = (csr >> 8) & 0xFF
    print(f"[CLEAR] IBCNT after clear before sampling = {ibcnt}")

    # --- SAMPLE 5 INPUT SIGNALS ---
    drive_signal(i, 0xC0, count=5)

    # ---- READ INPUT BUFFER COUNT ----
    csr = read_csr(i)
    ibcnt = (csr >> 8) & 0xFF
    print(f"[HALT] IBCNT after 5 samples = {ibcnt}")
    
    # ---- OVERFLOW TEST ----
    drive_signal(i, 0xC0, count=260)
    print("After driving 260 input signals")
    csr = read_csr(i)
    ibovf = (csr >> 16) & 1
    print(f"[OVERFLOW] IBOVF = {ibovf}")

    # --- READ INPUT BUFFER COUNT AGAIN ----
    csr = read_csr(i)
    csr |= (1 << 17)         # IBCLR = 1
    write_csr(i, csr)

    csr = read_csr(i)
    csr &= ~(1 << 17)
    write_csr(i, csr)

    csr = read_csr(i)
    ibcnt = (csr >> 8) & 0xFF
    print(f"[CLEAR] IBCNT after clear after 260 input signals = {ibcnt}")

    # ---- BYPASS TEST ----
    csr = read_csr(i)
    csr &= ~(1 << 5)         # HALT = 0
    csr &= ~(1 << 0)         # FEN = 0 (bypass)
    write_csr(i, csr)

    input_val = 0xC0
    output = os.popen(f"impl{i}.exe sig --data {hex(input_val)}").read().strip()

    if int(output, 16) == input_val:
        print(f"[BYPASS] PASS (output = {output})")
    else:
        print(f"[BYPASS] FAIL (output = {output})")
    
    #set fen to 1
    csr = read_csr(i) 
    csr |= (1) 
    write_csr(i, csr)
