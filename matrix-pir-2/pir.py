import random


class Server:

    # data is a list of integers
    def __init__(self, data, name):
        self.data = data[:]
        self.size = len(data)
        self.name = name

    # req is a dictionary mapping indexes to booleans of to include or not
    def make_req(self, req):
        print("server", self.name, "received req:", req)
        output = 0
        for i in req:
            if req[i]:
                output = output ^ self.data[i]
        return output


class User:
    def __init__(self, server1, server2):
        self.server1 = server1
        self.server2 = server2
        self.size = server1.size

    def send_req(self, x_i):
        print("user requesting data at index:", x_i)
        req = {}
        for i in range(self.size):
            req[i] = random.randint(0, 1) == 1

        req2 = req.copy()
        req2[x_i] = not req[x_i]

        res = self.server1.make_req(req)
        res2 = self.server2.make_req(req2)

        return res ^ res2


def main():
    size = 10
    index = 5

    test_data = []

    for i in range(size):
        test_data.append(random.randint(0, 10))

    s1 = Server(test_data, "S1")
    s2 = Server(test_data, "S2")

    print("Initializing servers on data:", test_data)

    user = User(s1, s2)
    print("OUTPUT:", user.send_req(index))


if __name__ == "__main__":
    main()
