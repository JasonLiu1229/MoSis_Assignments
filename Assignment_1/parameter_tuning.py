from simulate import singleSimExpOne
import os

def runExperimintOne():
    # Ensure the 'traces' directory exists and create the 'exp1' subdirectory
    os.makedirs('traces', exist_ok=True)
    os.makedirs('traces/exp1', exist_ok=True)
    
    i = 0.00
    while i < 5.00:
        i += 5.00 / 5001.00
        output = singleSimExpOne(d_c=i)
        i_name = str(i).replace(".", "_")
        
        # Create and write header to the CSV file
        with open(f"traces/exp1/experiminent_one_traces_{i_name}.csv", "w", encoding="utf-8") as f:
            f.write("d_c, x\n")
        
        # Append data to the CSV file
        with open(f"traces/exp1/experiminent_one_traces_{i_name}.csv", "a", encoding="utf-8") as f:
            for j, x in enumerate(output[0][output[1].index("x")]):
                f.write(f"{j}, {x}\n")

            
def runExperimintTwo():
    pass

if __name__ == "__main__":
    runExperimintOne()
    # runExperimintTwo()
