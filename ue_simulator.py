import time
import datetime
import sys

def log(message):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{timestamp}] [UE] {message}", flush=True)

def decode_for_duration(duration):
    start = time.time()
    # Every 2 seconds, simulate a decoded output
    while (time.time() - start) < duration:
        log("Decoded MIB: SFN=..., SCS=scs30or120, Offset=8, DMRS=pos2, PDCCH=32, CellBarred=notBarred")
        log("Decoded SIB: PLMN=00101, CellBarred=notBarred, Reserved=notReserved, OnDemandSI=disabled")
        time.sleep(2)

if __name__ == '__main__':
    duration = 10
    if "--duration" in sys.argv:
        try:
            duration = float(sys.argv[sys.argv.index("--duration") + 1])
        except Exception:
            duration = 10
    decode_for_duration(duration)
