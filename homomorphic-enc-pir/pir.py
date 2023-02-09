import numpy as np
from Pyfhel import Pyfhel, PyPtxt, PyPtxt


class Server:

    def __init__(self, size):
        print("Initializing server data:")

        self.size = size
        arr = []
        for i in range(size):
            row = []
            for j in range(size):
                row.append(i + j)
            arr.append(row)

            print(row)
        self.data_arr = np.array(arr)

    def get_data(self, enc_row, enc_col):
        row = np.matmul(enc_row, self.data_arr)
        return np.matmul(row, enc_col)

    def get_data_row(self, enc_row):
        row = np.matmul(enc_row, self.data_arr)
        return row


class Client:

    def __init__(self):
        HE = Pyfhel()
        HE.contextGen(p=63)  # Generating context.
        HE.keyGen()

        enc = lambda x: HE.encryptInt(x)
        self.enc_vec = np.vectorize(enc)

        dec = lambda x: HE.decryptInt(x)
        self.dec_vec = np.vectorize(dec)

    def req_row(self, i, size):
        req = [0 if j != i else 1 for j in range(size)]
        print("generated row req to enc:", req)
        return self.enc_vec(np.array(req))

    def req_col(self, i, size):
        req = [[0] if j != i else [1] for j in range(size)]
        print("generated column req to enc:", req)
        return self.enc_vec(np.array(req))

    def make_and_dec_req(self, server, row, col):
        out = server.get_data(self.req_row(row, server.size), self.req_col(col, server.size))
        return self.dec_vec(out)

    def make_and_dec_row_req(self, server, row):
        out = server.get_data_row(self.req_row(row, server.size))
        return self.dec_vec(out)


def main():
    size = 10
    row = 0
    col = 0

    server = Server(size)
    client = Client()

    print("starting request ... ")
    print("output:", client.make_and_dec_req(server, row, col))


if __name__ == "__main__":
    main()
