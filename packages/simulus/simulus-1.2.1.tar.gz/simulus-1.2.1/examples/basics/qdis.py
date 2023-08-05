import simulus

# so that we get same result from random priority
from random import seed
seed(12345)

def p(idx, sem):
    # set the priority of the current process (this is only useful 
    # if we use PRIORITY qdis)
    sim.set_priority(abs(idx-3.2))

    # make sure the process wait on the semaphore in order
    sim.sleep(idx)

    # the process will block on the semaphore and then print out 
    # a message when it is unblocked
    sem.wait()
    print("p[id=%d,prio=%.1f] resumes at %f" % 
          (idx, sim.get_priority(), sim.now))

def trywaits(sem):
    # create ten processes which will all block on the semaphore
    for i in range(10):
        sim.process(p, idx=i, sem=sem)
    sim.sleep(10)
    
    # release them all and check the order they are unblocked
    print('-'*40)
    for i in range(10):
        sem.signal()

sim = simulus.simulator()
s1 = sim.semaphore()
s2 = sim.semaphore(qdis=simulus.QDIS.LIFO)
s3 = sim.semaphore(qdis=simulus.QDIS.SIRO)
s4 = sim.semaphore(qdis=simulus.QDIS.PRIORITY)
sim.process(trywaits, s1, offset=0)
sim.process(trywaits, s2, offset=100)
sim.process(trywaits, s3, offset=200)
sim.process(trywaits, s4, offset=300)
sim.run()
