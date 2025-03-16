import time
import argparse
import logging
from simulators.base_simulator import BaseSimulator
from middleware import socket_communication

class UESimulator(BaseSimulator):
    def run(self):
        self.setup_logging(f'logs/ue_simulator_{self.simulator_id}.log')
        logging.info(f"UE {self.simulator_id} starting.")
        print(f"UE {self.simulator_id} starting.")
        self.connect_to_server()
        start_time = time.time()
        while time.time() - start_time < 10:
            mib_str = socket_communication.receive_data(self.socket)
            logging.info(f"UE {self.simulator_id} received MIB: {mib_str}")
            print(f"UE {self.simulator_id} received MIB: {mib_str}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='UE Simulator')
    parser.add_argument('--simulator_id', type=int, required=True, help='Simulator ID')
    parser.add_argument('--host', type=str, required=True, help='Host address')
    parser.add_argument('--port', type=int, required=True, help='Port number')
    args = parser.parse_args()

    simulator = UESimulator(args.simulator_id, args.host, args.port)
    simulator.start()
    simulator.join()
