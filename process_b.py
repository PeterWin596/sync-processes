from multiprocessing import Process, Value, Array
import time

def process_b(int_shared, str_shared):
    # Polling until Process A writes "10" to shared memory
    while int_shared.value != 10:
        time.sleep(0.1)
    
    # Step 2: Write "20" to shared integer memory and string for Process B
    int_shared.value = 20
    str_shared[:] = b"I am Process B"
    print(f"Process B: {str_shared.value.decode()}")
    # Quit after writing

if __name__ == "__main__":
    # Attach to shared memory locations
    int_shared = Value('i', 0)
    str_shared = Array('c', 20)

    # Create and start process B
    p_b = Process(target=process_b, args=(int_shared, str_shared))
    p_b.start()
    p_b.join()  # Wait for process B to finish
