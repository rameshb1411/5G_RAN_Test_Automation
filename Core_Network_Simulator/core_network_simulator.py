import threading
import time

class CoreNetworkSimulator(threading.Thread):
    def __init__(self, component_id):
        threading.Thread.__init__(self)
        self.component_id = component_id

    def run(self):
        print(f"Network component {self.component_id} is starting.")
        time.sleep(2)
        print(f"Network component {self.component_id} is operational.")

def main():
    component_count = 3
    network_components = [CoreNetworkSimulator(comp_id) for comp_id in range(1, component_count + 1)]

    for network_component in network_components:
        network_component.start()

    for network_component in network_components:
        network_component.join()

if __name__ == "__main__":
    main()
