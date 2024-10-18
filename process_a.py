from multiprocessing import Process, Value, Array
import time
import os

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

if __name__ == "__main__":
    # Shared memory locations for integer and string
    int_shared = Value('i', 0)
    str_shared = Array('c', 20)

    # Create and start process A
    p_a = Process(target=process_a, args=(int_shared, str_shared))
    p_a.start()
    p_a.join()  # Wait for process A to finish
