from simulate import singleSimExpOne


def runExperimintOne(interval=5.00/5001.00):
    with open("experiminent_one_traces.csv", "w", encoding="utf-8") as f:
        f.write("d_c, theta, x\n")
        i = 0.00
        while i < 5.00:
            output = singleSimExpOne(d_c=i)
            f.write(f"{i}, {output[0][output[1].index("x")]}\n")
            i += interval
            
def runExperimintTwo():
    pass

if __name__ == "__main__":
    runExperimintOne()
    # runExperimintTwo()
