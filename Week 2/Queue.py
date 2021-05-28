from Environment import *

leaderPipet = MyMutex("leaderPipet")
followerPipet = MyMutex("followerPipet")
leaderRendezvous = MySemaphore(0, "leaderRendezvous")
followerRendezvous = MySemaphore(0, "followerRendezvous")


def LeaderThread():
    while True:
        leaderPipet.wait()  # Make sure that only one leader thread can enter

        # Rendezvous pattern
        followerRendezvous.signal()
        leaderRendezvous.wait()

        leaderPipet.signal()


def FollowerThread():
    while True:
        followerPipet.wait()  # Make sure that only one follower thread can enter

        # Rendezvous pattern
        leaderRendezvous.signal()
        followerRendezvous.wait()

        followerPipet.signal()


def setup():
    for i in range(4):
        subscribe_thread(LeaderThread)

    for i in range(8):
        subscribe_thread(FollowerThread)
