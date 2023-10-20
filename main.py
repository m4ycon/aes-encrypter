
def sub_bytes(state):
  return

def shift_rows(state):
  return

def mix_columns(state):
  return

def add_round_key(state, w):
  return

def cipher(plain_text: str, w: str):
  state = plain_text
  state = add_round_key(state, w[0:4])

  for round in range(1, 10):
    state = sub_bytes(state)
    state = shift_rows(state)
    state = mix_columns(state)
    state = add_round_key(state, w[round*4:(round+1)*4])

  state = sub_bytes(state)
  state = shift_rows(state)
  state = add_round_key(state, w[40:44])

  return state
