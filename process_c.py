from multiprocessing import Process, Value, Array
import time

def process_c(int_shared, str_shared):
    # Polling until Process B writes "20" to shared memory
    while int_shared.value != 20:
        time.sleep(0.1)
    
    # Step 3: Write "30" to shared integer memory and string for Process C
    int_shared.value = 30
    str_shared[:] = b"I am Process C" + b" " * (20 - len(b"I am Process C"))
    print(f"Process C: {str_shared.value.decode()}")
    # Quit after writing

if __name__ == "__main__":
    # Attach to shared memory locations
    int_shared = Value('i', 0)
    str_shared = Array('c', 20)

    # Create and start process C
    p_c = Process(target=process_c, args=(int_shared, str_shared))
    p_c.start()
    p_c.join()  # Wait for process C to finish
