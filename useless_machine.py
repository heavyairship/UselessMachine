import threading

class UselessMachine(object):
  def __init__(self):
    self.switches = ["OFF" for x in range(10)]
    self.queue = []
    self.cond = threading.Condition()
    self.finished = False

  def flipOn(self, idx):
    self.cond.acquire()
    if self.switches[idx] == "OFF":
      self.queue.append(idx)
      self.switches[idx] = "ON"
      self.cond.notify()
    self.cond.release()

  def flipOff(self):
    out = 0
    self.cond.acquire()
    while len(self.queue) == 0 and not self.finished:
      self.cond.wait()
    if self.finished:
      out = -1
    while len(self.queue) > 0:
      idx = self.queue.pop(0)
      print("OFF %s" % idx)
      self.switches[idx] = "OFF"
    self.cond.release()
    return out

  def input(self):
    while True:
      self.cond.acquire()
      idx_raw = input("ON  ")
      if idx_raw == 'q':
        self.finished = True
      self.cond.notify()
      self.cond.release()
      if self.finished:
        return
      try:
        idx = int(idx_raw)
      except ValueError:
        continue
      if idx >= len(self.switches):
        continue
      self.flipOn(idx)

  def output(self):
    while self.flipOff() == 0:
      pass

uselessMachine = UselessMachine()
inputThread = threading.Thread(target=uselessMachine.input)
outputThread = threading.Thread(target=uselessMachine.output)
inputThread.start()
outputThread.start()
inputThread.join()
