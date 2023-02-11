import tenseal as ts
import numpy as np


class Server:

    def __init__(self, size):
        print("Initializing server data:")
        self.size = size
        self.data_arr = np.random.randint(1, 20, size=(size, size))
        print("Data : ", self.data_arr)

    def get_data(self, enc_row, enc_col):
        row = enc_row.matmul(self.data_arr)
        return enc_col.dot(row)

    def get_data_row(self, enc_row):
        row = np.matmul(enc_row, self.data_arr)
        return row


class Client:

    def __init__(self):
        # Setup TenSEAL context
        self.context = ts.context(
            ts.SCHEME_TYPE.CKKS,
            poly_modulus_degree=8192,
            coeff_mod_bit_sizes=[60, 40, 40, 60])
        self.context.generate_galois_keys()
        self.context.global_scale = 2 ** 40

    def req_row(self, i, size):
        req = np.array([0 if j != i else 1 for j in range(size)])
        print("generated row req to enc:", req)
        return ts.ckks_vector(self.context, req)

    def req_col(self, i, size):
        req = np.array([0 if j != i else 1 for j in range(size)])
        print("generated column req to enc:", req)
        return ts.ckks_vector(self.context, req)

    def make_and_dec_req(self, server, row, col):
        out = server.get_data(self.req_row(row, server.size), self.req_col(col, server.size))
        return out.decrypt()

    def make_and_dec_row_req(self, server, row):
        out = server.get_data_row(self.req_row(row, server.size))
        return out.decrypt()


def main():
    size = 10
    row = 8
    col = 9

    server = Server(size)
    client = Client()

    print("starting request ... ")
    print("output:", round(client.make_and_dec_req(server, row, col)[0]))


if __name__ == "__main__":
    main()
