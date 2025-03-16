import multiprocessing
import time
import threading


# Updating MIB Transmission to Align with 3GPP TS 38.331

class gNB:
    def __init__(self, config, broadcast_queue):
        self.sfn = 0
        self.config = config
        self.mib_periodicity = config["MIB"]["Periodicity"]
        self.sib1_periodicity = config["SIB1"]["Periodicity"]
        self.broadcast_queue = broadcast_queue
        self.all_sibs_broadcasted = False

    def broadcast_mib(self):
        if self.sfn % (self.mib_periodicity // 10) == 0:
            mib_message = f"[SFN={self.sfn}] Broadcasting MIB... -> SFN={self.sfn}"
            print(mib_message)
            self.broadcast_queue.put(mib_message)

    def broadcast_sib1(self):
        if self.sfn % (self.sib1_periodicity // 10) == 0:
            sib_message = f"[SFN={self.sfn}] Broadcasting SIB1... -> PLMN={self.config['SIB1']['PLMN']}, CellBarred={self.config['SIB1']['CellBarred']}, Reserved={self.config['SIB1']['Reserved']}, OnDemandSI={self.config['SIB1']['OnDemandSI']}"
            print(sib_message)
            self.broadcast_queue.put(sib_message)

        if self.sfn >= 100 and not self.all_sibs_broadcasted:
            print("ALL_SIBS_BROADCASTED")
            self.broadcast_queue.put("ALL_SIBS_BROADCASTED")
            self.all_sibs_broadcasted = True

    def run(self):
        for _ in range(1024):
            self.broadcast_mib()
            self.broadcast_sib1()
            self.sfn = (self.sfn + 1) % 1024
            time.sleep(0.01)  # Simulating time delay in transmission


# Updating UE to Decode MIB and SIB1
class UE:
    def __init__(self, ue_id, broadcast_queue):
        self.ue_id = ue_id
        self.decoded_mib = None
        self.decoded_sib1 = None
        self.all_sibs_received = False
        self.broadcast_queue = broadcast_queue

    def listen_for_broadcasts(self):
        while not self.all_sibs_received:
            try:
                message = self.broadcast_queue.get(timeout=0.1)
                if "MIB" in message:
                    self.decoded_mib = message
                elif "SIB1" in message:
                    self.decoded_sib1 = message
                elif "ALL_SIBS_BROADCASTED" in message:
                    self.all_sibs_received = True
            except:
                continue

        if self.decoded_mib and self.decoded_sib1 and self.all_sibs_received:
            print(f"[UE-{self.ue_id}] Successfully decoded MIB and all SIBs")
        else:
            print(f"[UE-{self.ue_id}] Failed to decode all required messages")

    def run(self):
        listen_thread = threading.Thread(target=self.listen_for_broadcasts)
        listen_thread.start()
        listen_thread.join()


class Core:
    def run(self):
        print("[Core] Core: Handling signaling requests...")
        for _ in range(10):
            print("[Core] Processing...")
            time.sleep(0.5)


if __name__ == "__main__":
    config = {"MIB": {"Periodicity": 80},
              "SIB1": {"Periodicity": 160, "PLMN": "00101", "CellBarred": "notBarred", "Reserved": "notReserved",
                       "OnDemandSI": "disabled"}}
    broadcast_queue = multiprocessing.Queue()

    gnb = gNB(config, broadcast_queue)
    core = Core()
    ue1 = UE(1, broadcast_queue)
    ue2 = UE(2, broadcast_queue)

    gnb_process = multiprocessing.Process(target=gnb.run)
    core_process = multiprocessing.Process(target=core.run)
    ue1_process = multiprocessing.Process(target=ue1.run)
    ue2_process = multiprocessing.Process(target=ue2.run)

    gnb_process.start()
    core_process.start()
    ue1_process.start()
    ue2_process.start()

    gnb_process.join()
    core_process.join()
    ue1_process.join()
    ue2_process.join()
