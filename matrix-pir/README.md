## Basic Two Server Scheme

Very simple PIR scheme that allows user to privately obtain the bit `x_i` by receiving a single bit from each of two servers

1. Select random set
2. Send set to server 1
3. Send set XOR i to server 2
4. Servers respond with bits of index specified by set.
5. All the XORs cancel out except for the bit i
6. Server is only sent a single bit back
7. User sends [n] items though, so not better communication yet
