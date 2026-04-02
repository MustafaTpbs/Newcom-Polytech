
def decToBin(dec,n_bits):
  binary = f'{dec:0{n_bits}b}'
  return binary

def binToHexa(n):
    # convert binary to int
    num = int(n, 2)
    # convert int to hexadecimal
    hex_num = hex(num)
    return(hex_num)

def to_mirror_inverted(binary):
  n_bits = len(binary)
  result = n_bits*[None]
  for idx,b in enumerate(binary):
    result[n_bits-idx-1] = '0' if b=='1' else '1'
  binary_mirror_inverted = ''.join(result)
  result_hex = binToHexa(binary_mirror_inverted)
  result_dec = int(result_hex,16)

  return binary_mirror_inverted,result_hex,result_dec