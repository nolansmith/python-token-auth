
# [a,b,c] = destructure(obj, 'fields', 'you', 'want')
# https://stackoverflow.com/questions/54785148/destructuring-dicts-and-objects-in-python
def destructure (d, *keys):
  return [ d[k] if k in d else None for k in keys ]