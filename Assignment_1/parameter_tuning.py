from simulate import singleSimExpOne

def runExperimintOne():
    i = 0.00
    while i < 5.00:
        i += 5.00/5001.00
        output = singleSimExpOne(d_c=i)
        with open(f"traces/experiminent_one_traces_{i}.csv", "w", encoding="utf-8") as f:
            f.write("d_c, x\n")
        with open(f"traces/experiminent_one_traces_{i}.csv", "a", encoding="utf-8") as f:
            for j, x in enumerate(output[0][output[1].index("x")]):
                f.write(f"{j}, {x}\n")
            
def runExperimintTwo():
    pass

if __name__ == "__main__":
    runExperimintOne()
    # runExperimintTwo()
