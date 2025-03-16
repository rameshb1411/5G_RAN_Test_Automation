import time
import datetime
import sys

SFN = 0  # System Frame Number (0-1023)
MIB_PERIOD = 40    # ms: transmit MIB every 40ms
SIB1_PERIOD = 8    # ms: transmit SIB1 every 8ms

def log(message):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{timestamp}] [gNB] {message}", flush=True)

def broadcast_cycle():
    global SFN
    # Simulate a 1-second cycle with 1000 iterations (each = 1ms)
    for i in range(1000):
        # MIB broadcast: if current ms in cycle mod 40 is less than 2 (≈2ms window)
        if i % MIB_PERIOD < 2:
            log(f"SFN={SFN}: Broadcasting MIB... -> SFN={SFN} | SCS=scs30or120 | Offset=8 | DMRS=pos2 | PDCCH=32 | CellBarred=notBarred")
        # SIB1 broadcast: if current ms mod 8 is less than 2 (≈2ms window)
        if i % SIB1_PERIOD < 2:
            log(f"SFN={SFN}: Broadcasting SIB1... -> PLMN=00101, CellBarred=notBarred, Reserved=notReserved, OnDemandSI=disabled")
        SFN = (SFN + 1) % 1024
        time.sleep(0.001)  # 1ms per iteration
    log("ALL_SIBS_BROADCASTED")

def broadcast_for_duration(duration):
    # Run broadcast_cycle repeatedly for "duration" seconds
    import time
    start = time.time()
    while (time.time() - start) < duration:
        broadcast_cycle()

if __name__ == '__main__':
    duration = 10
    if "--duration" in sys.argv:
        try:
            duration = float(sys.argv[sys.argv.index("--duration") + 1])
        except Exception:
            duration = 10
    broadcast_for_duration(duration)
