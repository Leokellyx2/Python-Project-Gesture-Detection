
import random

sim_ceiling = 180

sim_movements = {
    "LowPass" : (10, 10, 10, 10),
    "HighPass" : (30, 30, 30, 30),
    "LowHold" : (10, 10, 10, 10, 10, 10, 10, 10, 10, 10),
    "HighHold" : (30, 30, 30, 30, 30, 30, 30, 30, 30, 30),
    "PullUp" : (8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28),
    "PushDown" : (28, 26, 24, 22, 20, 18, 16, 14, 12, 10)
    }

sim_sequences = (
    ("LowPass"),
    ("HighPass"),
    ("LowHold"),
    ("HighHold"),
    ("PullUp"),
    ("PushDown"),
    ("LowPass", "LowPass"),
    ("HighPass", "HighPass"),
    ("LowPass", "LowHold"),
    ("HighPass", "HighHold"),
    ("PullUp", "HighPass", "LowHold"),
    ("PushDown", "LowPass", "HighHold")
)

sim_samples = []

def appendCeiling(count):
    for i in range(0,count):
        sim_samples.append(sim_ceiling)    

def appendSeq():
    sq = random.choice(sim_sequences)
    appendCeiling(25)
    sim_samples.append("*** " + str(sq) + " coming next")
    # single tuple actually comes back as a String
    if isinstance(sq, tuple):
        for s in sq:
            sim_samples.extend(sim_movements[s])
            appendCeiling(5)
    else:
        sim_samples.extend(sim_movements[sq])
        appendCeiling(5)
        
def getSonar():
    if (len(sim_samples) < 20):
        appendSeq()
    while True:
        value = sim_samples.pop(0)
        if (isinstance(value,int)):
            break
        else:
            print(value)
    value = value + random.uniform(-1.0,1.0)
    return value;

def setup():
    print("SIMULATOR Setup completed")
    # none required

def cleanup():
    print("Cleanup completed")
    # none required
