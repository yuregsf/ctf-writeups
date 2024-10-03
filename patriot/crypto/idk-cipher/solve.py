
import base64
# """
# ********************************************
# *                                          *
# *                                          *
# ********************************************
# """
# # WARNING: This is a secret key. Do not expose it.
srt_key = 'secretkey' # // TODO: change the placeholder
# rsv_input = usr_input[::-1]
output_arr = []
c = base64.b64decode('QRVWUFdWEUpdXEVGCF8DVEoYEEIBBlEAE0dQAURFD1I=')
n = len(c)

left = []
right = []

for i in range(n):
    if i%2 == 0:
        left.append(c[i])
    else:
        right.append(c[i])

left_c = []
right_c = []
for i in range(len(left)):
    enc_p1 = chr(left[i] ^ ord(srt_key[i % len(srt_key)]))
    enc_p2 = chr(right[i] ^ ord(srt_key[i % len(srt_key)]))
    left_c.append(enc_p1)
    right_c.append(enc_p2)

print(''.join(left_c) + ''.join(right_c[::-1]))
# WARNING: Encoded text should not be decoded without proper authorization.
#encoded_val = ''.join(output_arr)
#b64_enc_val = base64.b64encode(encoded_val.encode())
#print(encoded_val)
