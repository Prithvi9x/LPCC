class OverlayManager:
    def __init__(self, memory_size):
        self.memory_size = memory_size
        self.current_overlay = None

    def load_overlay(self, overlay_name, size):
        if size > self.memory_size:
            print(f"ERROR: Overlay '{overlay_name}' too large for memory")
            return

        if self.current_overlay:
            print(f"Unloading overlay: {self.current_overlay}")

        self.current_overlay = overlay_name
        print(f"Loading overlay: {overlay_name} (size={size}) into memory")

    def execute(self):
        if self.current_overlay:
            print(f"Executing overlay: {self.current_overlay}")
        else:
            print("No overlay loaded")

if __name__ == "__main__":
    memory_size = int(input("Enter total memory size: "))
    manager = OverlayManager(memory_size)

    n = int(input("Enter number of overlays: "))
    overlays = {}

    for _ in range(n):
        name = input("Overlay name: ")
        size = int(input("Overlay size: "))
        overlays[name] = size

    print("\nEnter execution sequence (space separated overlay names):")
    sequence = input().split()

    print("\nOVERLAY EXECUTION")

    for ov in sequence:
        if ov not in overlays:
            print(f"ERROR: Overlay '{ov}' not defined")
            continue

        manager.load_overlay(ov, overlays[ov])
        manager.execute()
        print("-" * 30)