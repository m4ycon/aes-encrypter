from random import randint

DEBUG = False # change it on main()

def printd(*args, **kwargs):
  if DEBUG:
    print(*args, **kwargs)

def get_hex_list_str(l: list[int | str]):
  int_l = [i if type(i) is int else ord(i) for i in l]
  hex_l = [hex(i)[2:].zfill(2) for i in int_l]
  return ' '.join([''.join(hex_l[i:i+4]) for i in range(0, len(hex_l), 4)])

def get_matrix_str(m: list[list[int]]):
  return ' '.join([get_hex_list_str(i) for i in m])

def xor_list(a: list[int], b: list[int]):
  return [i ^ j for i, j in zip(a, b)]

def key_expansion(key: str, nrounds: int = 10):
  
  RCON = [
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
    0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
    0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
    0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39
  ]

  printd(f'key: {key}')
  ext_key = [ord(c) for c in key[:16]] + [0]*(16 - len(key))
  klist: list[list[int]] = [ext_key[i:i+4] for i in range(0, 16, 4)]
  eklist: list[list[int]] = []

  def rot_word(word: list[int]):
    return word[1:] + [word[0]]
  def sub_word(word: list[int]):
    return sub_bytes([word, [0]*4, [0]*4, [0]*4])[0]
  def rcon(i: int):
    return [RCON[i], 0, 0, 0]
  def ek(offset: int):
    return eklist[offset//4]
  def k(offset: int):
    return klist[offset//4]
  for i in range(0, 16, 4):
    eklist.append(k(i))
  printd(f'r0: \n{get_matrix_str(eklist[0:4])}')
  for j in range(4, (nrounds+1)*4, 4):
    i = j
    a = sub_word(rot_word(ek((i-1)*4)))
    b = rcon(i//4)
    c = ek((i-4)*4)
    eklist.append(xor_list(xor_list(a, b), c)); i += 1
    eklist.append(xor_list(ek((i-1)*4), ek((i-4)*4))); i += 1
    eklist.append(xor_list(ek((i-1)*4), ek((i-4)*4))); i += 1
    eklist.append(xor_list(ek((i-1)*4), ek((i-4)*4))); i += 1
    printd(f'r{j//4}: \n{get_matrix_str(eklist[j:j+4])}')
  return eklist

def sub_bytes(state: list[list[int]], crypt: bool = True):

  SBOX = [
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
  ]

  INV_SBOX = [
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D
  ]
  
  new_state = state.copy()
  lookup = SBOX if crypt else INV_SBOX
  for r in range(0, 4):
    for c in range(0, 4):
      new_state[r][c] = lookup[new_state[r][c]]
  return new_state

def shift_rows(state: list[list[int]], crypt: bool = True):
  new_state = state.copy()
  for rows in range(0, 4):
    shift_left = new_state[rows][rows:] + new_state[rows][:rows]
    shift_right = new_state[rows][-rows:] + new_state[rows][:-rows]
    new_state[rows] = shift_left if crypt else shift_right
  return new_state

def mix_columns(state: list[list[int]], crypt: bool = True):
  
  MIX_MUL_ENC = [
    [2, 3, 1, 1],
    [1, 2, 3, 1],
    [1, 1, 2, 3],
    [3, 1, 1, 2]
  ]

  MIX_MUL_DEC = [
    [0x0E, 0x0B, 0x0D, 0x09],
    [0x09, 0x0E, 0x0B, 0x0D],
    [0x0D, 0x09, 0x0E, 0x0B],
    [0x0B, 0x0D, 0x09, 0x0E]
  ]
  
  lookup = MIX_MUL_ENC if crypt else MIX_MUL_DEC
  new_state = [[0 for _ in range(4)] for _ in range(4)]
  for i in range(0, 4):
    for j in range(0, 4):
      for k in range(0, 4):
        new_state[j][i] ^= gf_mul(state[k][i], lookup[j][k])
  return new_state

def add_round_key(state: list[list[int]], key: list[list[int]]):
  inv_key = inv_matrix(key)
  new_state = state.copy()
  for r in range(0, 4):
    for c in range(0, 4):
      new_state[r][c] ^= inv_key[r][c]
  return new_state

def gf_mul(n1: int, n2: int):

  if (n1 == 1 or n2 == 1):
    return n1 * n2
  
  if (n1 == 0 or n2 == 0):
    return 0
  
  E = [
    0x01, 0x03, 0x05, 0x0F, 0x11, 0x33, 0x55, 0xFF, 0x1A, 0x2E, 0x72, 0x96, 0xA1, 0xF8, 0x13, 0x35,
    0x5F, 0xE1, 0x38, 0x48, 0xD8, 0x73, 0x95, 0xA4, 0xF7, 0x02, 0x06, 0x0A, 0x1E, 0x22, 0x66, 0xAA,
    0xE5, 0x34, 0x5C, 0xE4, 0x37, 0x59, 0xEB, 0x26, 0x6A, 0xBE, 0xD9, 0x70, 0x90, 0xAB, 0xE6, 0x31,
    0x53, 0xF5, 0x04, 0x0C, 0x14, 0x3C, 0x44, 0xCC, 0x4F, 0xD1, 0x68, 0xB8, 0xD3, 0x6E, 0xB2, 0xCD,
    0x4C, 0xD4, 0x67, 0xA9, 0xE0, 0x3B, 0x4D, 0xD7, 0x62, 0xA6, 0xF1, 0x08, 0x18, 0x28, 0x78, 0x88,
    0x83, 0x9E, 0xB9, 0xD0, 0x6B, 0xBD, 0xDC, 0x7F, 0x81, 0x98, 0xB3, 0xCE, 0x49, 0xDB, 0x76, 0x9A,
    0xB5, 0xC4, 0x57, 0xF9, 0x10, 0x30, 0x50, 0xF0, 0x0B, 0x1D, 0x27, 0x69, 0xBB, 0xD6, 0x61, 0xA3,
    0xFE, 0x19, 0x2B, 0x7D, 0x87, 0x92, 0xAD, 0xEC, 0x2F, 0x71, 0x93, 0xAE, 0xE9, 0x20, 0x60, 0xA0,
    0xFB, 0x16, 0x3A, 0x4E, 0xD2, 0x6D, 0xB7, 0xC2, 0x5D, 0xE7, 0x32, 0x56, 0xFA, 0x15, 0x3F, 0x41,
    0xC3, 0x5E, 0xE2, 0x3D, 0x47, 0xC9, 0x40, 0xC0, 0x5B, 0xED, 0x2C, 0x74, 0x9C, 0xBF, 0xDA, 0x75,
    0x9F, 0xBA, 0xD5, 0x64, 0xAC, 0xEF, 0x2A, 0x7E, 0x82, 0x9D, 0xBC, 0xDF, 0x7A, 0x8E, 0x89, 0x80,
    0x9B, 0xB6, 0xC1, 0x58, 0xE8, 0x23, 0x65, 0xAF, 0xEA, 0x25, 0x6F, 0xB1, 0xC8, 0x43, 0xC5, 0x54,
    0xFC, 0x1F, 0x21, 0x63, 0xA5, 0xF4, 0x07, 0x09, 0x1B, 0x2D, 0x77, 0x99, 0xB0, 0xCB, 0x46, 0xCA,
    0x45, 0xCF, 0x4A, 0xDE, 0x79, 0x8B, 0x86, 0x91, 0xA8, 0xE3, 0x3E, 0x42, 0xC6, 0x51, 0xF3, 0x0E,
    0x12, 0x36, 0x5A, 0xEE, 0x29, 0x7B, 0x8D, 0x8C, 0x8F, 0x8A, 0x85, 0x94, 0xA7, 0xF2, 0x0D, 0x17,
    0x39, 0x4B, 0xDD, 0x7C, 0x84, 0x97, 0xA2, 0xFD, 0x1C, 0x24, 0x6C, 0xB4, 0xC7, 0x52, 0xF6, 0x01
  ]

  L = [
    None, 0x00, 0x19, 0x01, 0x32, 0x02, 0x1A, 0xC6, 0x4B, 0xC7, 0x1B, 0x68, 0x33, 0xEE, 0xDF, 0x03,
    0x64, 0x04, 0xE0, 0x0E, 0x34, 0x8D, 0x81, 0xEF, 0x4C, 0x71, 0x08, 0xC8, 0xF8, 0x69, 0x1C, 0xC1,
    0x7D, 0xC2, 0x1D, 0xB5, 0xF9, 0xB9, 0x27, 0x6A, 0x4D, 0xE4, 0xA6, 0x72, 0x9A, 0xC9, 0x09, 0x78,
    0x65, 0x2F, 0x8A, 0x05, 0x21, 0x0F, 0xE1, 0x24, 0x12, 0xF0, 0x82, 0x45, 0x35, 0x93, 0xDA, 0x8E,
    0x96, 0x8F, 0xDB, 0xBD, 0x36, 0xD0, 0xCE, 0x94, 0x13, 0x5C, 0xD2, 0xF1, 0x40, 0x46, 0x83, 0x38,
    0x66, 0xDD, 0xFD, 0x30, 0xBF, 0x06, 0x8B, 0x62, 0xB3, 0x25, 0xE2, 0x98, 0x22, 0x88, 0x91, 0x10,
    0x7E, 0x6E, 0x48, 0xC3, 0xA3, 0xB6, 0x1E, 0x42, 0x3A, 0x6B, 0x28, 0x54, 0xFA, 0x85, 0x3D, 0xBA,
    0x2B, 0x79, 0x0A, 0x15, 0x9B, 0x9F, 0x5E, 0xCA, 0x4E, 0xD4, 0xAC, 0xE5, 0xF3, 0x73, 0xA7, 0x57,
    0xAF, 0x58, 0xA8, 0x50, 0xF4, 0xEA, 0xD6, 0x74, 0x4F, 0xAE, 0xE9, 0xD5, 0xE7, 0xE6, 0xAD, 0xE8,
    0x2C, 0xD7, 0x75, 0x7A, 0xEB, 0x16, 0x0B, 0xF5, 0x59, 0xCB, 0x5F, 0xB0, 0x9C, 0xA9, 0x51, 0xA0,
    0x7F, 0x0C, 0xF6, 0x6F, 0x17, 0xC4, 0x49, 0xEC, 0xD8, 0x43, 0x1F, 0x2D, 0xA4, 0x76, 0x7B, 0xB7,
    0xCC, 0xBB, 0x3E, 0x5A, 0xFB, 0x60, 0xB1, 0x86, 0x3B, 0x52, 0xA1, 0x6C, 0xAA, 0x55, 0x29, 0x9D,
    0x97, 0xB2, 0x87, 0x90, 0x61, 0xBE, 0xDC, 0xFC, 0xBC, 0x95, 0xCF, 0xCD, 0x37, 0x3F, 0x5B, 0xD1,
    0x53, 0x39, 0x84, 0x3C, 0x41, 0xA2, 0x6D, 0x47, 0x14, 0x2A, 0x9E, 0x5D, 0x56, 0xF2, 0xD3, 0xAB,
    0x44, 0x11, 0x92, 0xD9, 0x23, 0x20, 0x2E, 0x89, 0xB4, 0x7C, 0xB8, 0x26, 0x77, 0x99, 0xE3, 0xA5,
    0x67, 0x4A, 0xED, 0xDE, 0xC5, 0x31, 0xFE, 0x18, 0x0D, 0x63, 0x8C, 0x80, 0xC0, 0xF7, 0x70, 0x07
  ]

  return E[L[n1] + L[n2]] if L[n1] + L[n2] <= 0xFF else E[L[n1] + L[n2] - 0xFF]


def inv_matrix(m: list[list[int]]):
  inverse_matrix = [[0 for _ in range(4)] for _ in range(4)]
  for i in range(4):
    for j in range(4):
        inverse_matrix[j][i] = m[i][j]
  return inverse_matrix

def str_to_matrix(s: str):
  matrix = [ord(i) for i in s] + [0]*(16 - len(s))
  printd(f'hex input: {get_hex_list_str(matrix)}')
  matrix = [matrix[i:i+4] for i in range(0, len(matrix), 4)]
  return inv_matrix(matrix)

def cipher(plain_text: str, key: str, isHex: bool = False, nround: int = 10):
  if (isHex):
    plain_text = hex_str_to_char_str(plain_text)
    key = hex_str_to_char_str(key)
  w = key_expansion(key, nround)
  res = []
  for i in range(0, len(plain_text), 16):
    res.extend(cipher16(plain_text[i:i+16], w, nround))
  printd(f"hex cipher: {' '.join(hex(value)[2:].zfill(2) for row in res for value in row)}")
  return ''.join(hex(value)[2:].zfill(2) if isHex else chr(value) for row in res for value in row)

def cipher16(plain_text: str, w: list[list[int]], nround: int):
  kinterval = 0
  printd(f'plain_text: {plain_text}')
  printd(f"hex plain_text: {get_hex_list_str([ord(x) for x in plain_text])}")
  state = str_to_matrix(plain_text)
  printd(f'state: \n{get_matrix_str(state)}')
  printd(f'key: \n{get_matrix_str(w[kinterval:kinterval+4])}')
  state = add_round_key(state, w[kinterval:kinterval+4])
  kinterval += 4
  printd(f'add_round_key: \n{get_matrix_str(state)}')
  printd(f'r0: \n{get_matrix_str(inv_matrix(state))}\n')

  for round in range(1, nround):
    state = sub_bytes(state)
    printd(f'sub_bytes: \n{get_matrix_str(state)}')
    state = shift_rows(state)
    printd(f'shift_rows: \n{get_matrix_str(state)}')
    state = mix_columns(state)
    printd(f'mix_columns: \n{get_matrix_str(state)}')
    state = add_round_key(state, w[kinterval:kinterval+4])
    printd(f'key: \n{get_matrix_str(w[kinterval:kinterval+4])}')
    kinterval += 4
    printd(f'add_round_key: \n{get_matrix_str(state)}')
    printd(f'r{round}: \n{get_matrix_str(inv_matrix(state))}\n')

  state = sub_bytes(state)
  printd(f'sub_bytes: \n{get_matrix_str(state)}')
  state = shift_rows(state)
  printd(f'shift_rows: \n{get_matrix_str(state)}')
  state = add_round_key(state, w[kinterval:kinterval+4])
  printd(f'key: \n{get_matrix_str(w[kinterval:kinterval+4])}')
  kinterval += 4
  printd(f'add_round_key: \n{get_matrix_str(state)}')
  printd(f'r{nround}: \n{get_matrix_str(inv_matrix(state))}\n')

  return inv_matrix(state)


def decipher(cript: str, key: str, isHex: bool = False, nround: int = 10):
  if (isHex):
    cript = hex_str_to_char_str(cript)
    key = hex_str_to_char_str(key)
  w = key_expansion(key, nround)
  res = []
  for i in range(0, len(cript), 16):
    res.extend(decipher16(cript[i:i+16], w, nround))
  printd(f"hex message: {' '.join(hex(value)[2:].zfill(2) for row in res for value in row)}")
  return ''.join(hex(value)[2:].zfill(2) if isHex else chr(value) for row in res for value in row)

def decipher16(cript: str, w: list[list[int]], nround: int):
  kinterval = nround*4
  printd(f'cript: {cript}')
  state = str_to_matrix(cript)
  printd(f'state: \n{get_matrix_str(state)}')
  printd(f'key: \n{get_matrix_str(w[kinterval:kinterval+4])}')
  state = add_round_key(state, w[kinterval:kinterval+4])
  kinterval -= 4
  printd(f'add_round_key: \n{get_matrix_str(state)}')
  printd(f'r0: \n{get_matrix_str(inv_matrix(state))}\n')

  for round in range(1, nround):
    state = shift_rows(state, False)
    printd(f'shift_rows: \n{get_matrix_str(state)}')
    state = sub_bytes(state, False)
    printd(f'sub_bytes: \n{get_matrix_str(state)}')
    printd(f'key: \n{get_matrix_str(w[kinterval:kinterval+4])}')
    state = add_round_key(state, w[kinterval:kinterval+4])
    kinterval -= 4
    printd(f'add_round_key: \n{get_matrix_str(state)}')
    state = mix_columns(state, False)
    printd(f'mix_columns: \n{get_matrix_str(state)}')
    printd(f'r{round}: \n{get_matrix_str(inv_matrix(state))}\n')

  state = shift_rows(state, False)
  printd(f'shift_rows: \n{get_matrix_str(state)}')
  state = sub_bytes(state, False)
  printd(f'sub_bytes: \n{get_matrix_str(state)}')
  state = add_round_key(state, w[kinterval:kinterval+4])
  printd(f'add_round_key: \n{get_matrix_str(state)}')
  printd(f'key: \n{get_matrix_str(w[kinterval:kinterval+4])}')
  kinterval -= 4
  printd(f'r{nround}: \n{get_matrix_str(inv_matrix(state))}\n')

  return inv_matrix(state)

def ctr(text: str, key: str, isHex: bool = False,  nrounds: int = 10, nonce: int = None):
  if isHex:
    text = hex_str_to_char_str(text)
    key = hex_str_to_char_str(key)
  w = key_expansion(key, nrounds)
  counter = 0
  if nonce is None:
    nonce = randint(0, (2**64)-1)
    print(f'nonce (dec): {nonce}')
    printd(f"nonce (hex): {'0'*(32-len(hex(nonce+counter)[2:])) + hex(nonce+counter)[2:]}")
  res = []
  for i in range(0, len(text), 16):
    offset = '0'*(32-len(hex(nonce+counter)[2:])) + hex(nonce+counter)[2:]
    offset = [int(offset[i:i+2], 16) for i in range(0, len(offset), 2)]
    plain_text = ''.join([chr(h) for h in offset])
    cript_matrix = cipher16(plain_text, w, nrounds)
    res.extend(xor_list([value for rows in cript_matrix for value in rows], [ord(c) for c in text[i:i+16]]))
    counter += 1
  printd(f"hex ctr: {' '.join(hex(value)[2:].zfill(2) for value in res)}")
  return ''.join(hex(value)[2:].zfill(2) if isHex else chr(value) for value in res)

def hex_str_to_char_str(s: str):
  s = s.replace(' ', '')
  res = [s[i:i+2] for i in range(0, len(s), 2)]
  res = [chr(i) for i in [int(i, 16) for i in res]]
  return ''.join(res)

def handle_user_cipher():
  print('Modo de operação:')
  print('1. ECB')
  print('2. CTR')
  mode = input()
  is_hex = input('O arquivo está em hexadecimal? (s/n): ').lower() == 's'
  key = input('Chave (hex 128 bits): ' if is_hex else 'Chave (ascii 128 bits): ')
  nround = int(input('Número de rodadas: '))
  file_addr = input('Endereço do arquivo: ')

  content = bytes()
  with open(file_addr, 'rb') as file:
    content = file.read()
  bytes_ = [chr(c) for c in content]
  plain_text = ''.join(bytes_)

  print(f'Texto original (hex): {plain_text if is_hex else get_hex_list_str(content)}')

  cipher_text = ''
  if (mode == '1'):
    cipher_text = cipher(plain_text, key, is_hex, nround)
  elif (mode == '2'):
    cipher_text = ctr(plain_text, key, is_hex, nround)

  with open(file_addr, 'wb') as file:
    bytes_ = bytes([ord(i) for i in cipher_text])
    file.write(bytes_)
  print(f'Texto cifrado (hex): {cipher_text if is_hex else get_hex_list_str(cipher_text)}')
  print('Arquivo cifrado com sucesso!')

def handle_user_decipher():
  print('Modo de operação:')
  print('1. ECB')
  print('2. CTR')
  mode = input()
  is_hex = input('O arquivo está em hexadecimal? (s/n): ').lower() == 's'
  key = input('Chave (hex 128 bits): ' if is_hex else 'Chave (ascii 128 bits): ')
  nround = int(input('Número de rodadas: '))
  file_addr = input('Endereço do arquivo cifrado: ')

  content = bytes()
  with open(file_addr, 'rb') as file:
    content = file.read()
  bytes_ = [chr(c) for c in content]
  cipher_text = ''.join(bytes_)
  print(f'Texto cifrado (hex): {cipher_text if is_hex else get_hex_list_str(content)}')

  if (mode == '1'):
    msg = decipher(cipher_text, key, is_hex, nround)
  elif (mode == '2'):
    nonce = int(input('Nonce (dec): '))
    msg = ctr(cipher_text, key, is_hex, nround, nonce)
  
  with open(file_addr, 'wb') as file:
    bytes_ = [ord(i) for i in msg]
    while bytes_[-1] == 0: # filter 0's at the end
      bytes_ = bytes_[:-1]
    bytes_ = bytes(bytes_)
    file.write(bytes_)
  print(f'Texto decifrado (hex): {msg if is_hex else get_hex_list_str(msg)}')
  print('Arquivo decifrado com sucesso!')

def main():
  global DEBUG
  DEBUG = False

  options = ['Cifrar', 'Decifrar', 'Sair']
  switcher = {
    options.index('Cifrar')+1: handle_user_cipher,
    options.index('Decifrar')+1: handle_user_decipher,
    options.index('Sair')+1: exit
  }

  usr_input = 1
  while options[usr_input-1] != 'Sair':
    print(f'{" AES ":=^20}')
    for i in range(len(options)):
      print(f'{i+1}. {options[i]}')
    
    usr_input = input('Opção: ')
    try:
      usr_input = int(usr_input)
      if not (0 < int(usr_input) <= len(options)):
        raise ValueError
    except ValueError:
      usr_input = 1
      print('Opção inválida!')
      continue

    switcher[usr_input]()

main()
