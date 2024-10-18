from multiprocessing import Process, Value, Array
import time
import os

# Process A
def process_a(int_shared, str_shared):
    # Step 1: Write "10" to shared integer memory and string for Process A
    int_shared.value = 10
    str_shared[:] = b"I am Process A" + b" " * (20 - len(b"I am Process A"))
    print(f"Process A: {str_shared.value.decode()}")

    # Wait until Process B writes
    while int_shared.value != 20:
        time.sleep(0.1)

    # Process B has written, print its data
    print(f"Process A reads from Process B: {str_shared.value.decode()}, PID: {os.getpid()}")

    # Wait until Process C writes
    while int_shared.value != 30:
        time.sleep(0.1)

    # Process C has written, print its data
    print(f"Process A reads from Process C: {str_shared.value.decode()}, PID: {os.getpid()}")

    # Final message
    print("Good Bye World, I am Done!!")

# Process B
def process_b(int_shared, str_shared):
    # Polling until Process A writes "10" to shared memory
    while int_shared.value != 10:
        print(f"Process B waiting... (shared integer = {int_shared.value})")
        time.sleep(0.1)
    
    # Step 2: Write "20" to shared integer memory and string for Process B
    int_shared.value = 20
    str_shared[:] = b"I am Process B" + b" " * (20 - len(b"I am Process B"))
    print(f"Process B: {str_shared.value.decode()}")

# Process C
def process_c(int_shared, str_shared):
    # Polling until Process B writes "20" to shared memory
    while int_shared.value != 20:
        print(f"Process C waiting... (shared integer = {int_shared.value})")
        time.sleep(0.1)
    
    # Step 3: Write "30" to shared integer memory and string for Process C
    int_shared.value = 30
    str_shared[:] = b"I am Process C" + b" " * (20 - len(b"I am Process C"))
    print(f"Process C: {str_shared.value.decode()}")

# Main function to launch processes
if __name__ == "__main__":
    # Shared memory locations for integer and string
    int_shared = Value('i', 0)  # Shared integer
    str_shared = Array('c', 20)  # Shared string array

    # Create processes
    p_a = Process(target=process_a, args=(int_shared, str_shared))
    p_b = Process(target=process_b, args=(int_shared, str_shared))
    p_c = Process(target=process_c, args=(int_shared, str_shared))

    # Start all processes
    p_a.start()
    p_b.start()
    p_c.start()

    # Wait for all processes to finish
    p_a.join()
    p_b.join()
    p_c.join()
