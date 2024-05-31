
from dataclasses import dataclass, asdict
from datetime import datetime as dt

def to_dt(time):
  return dt(year=2000,month=1,day=1,hour=time.hour,minute=time.minute)

@dataclass
class Time:
  hour: int
  minute: int

@dataclass
class Slot:
  day: str
  start: Time
  end: Time

@dataclass
class Schedule:
  slots: list # list of slots
  class_name: str = None
  def __str__(self) -> str:
    def fmt(time):
      return dt.strftime(to_dt(time),'%I:%M')
    s=''
    for slot in self.slots:
      s+=f'{slot.day:<9} {fmt(slot.start)}-{fmt(slot.end)}   '
    return s

@dataclass
class Class:
  name: str
  options: list # list of Schedules


def conflict(s, slist): # schedule s conflict with any in slist

  def to_dt_range(slot):
    return (to_dt(slot.start), to_dt(slot.end))
    
  def overlap(s1: Schedule, s2: Schedule):
    for slot1 in s1.slots:
      for slot2 in s2.slots:
        if slot1.day == slot2.day:
          slot1_range=to_dt_range(slot1)
          slot2_range=to_dt_range(slot2)
          delta = min(slot1_range[1], slot2_range[1]) - max(slot1_range[0], slot2_range[0])
          #print(slot1_range, slot2_range, delta, delta.total_seconds())
          if delta.total_seconds()>0: # positive means overlap
            return True
    return False

  if any([s.class_name == s2.class_name for s2 in slist.values()]):
    return True
  for s2 in slist.values():
    if overlap(s,s2):
      return True
  return False


def valid_combinations(target, class_schedules):
  valid_list=[]
  def check(target,reserved={}):
    if not target: # if empty, then reserved is a valid combination
      valid_list.append(reserved)
      return
    c=target[0]
    for s in class_schedules[c]:
      if not conflict(s, reserved):
        #check(target[1:], {**reserved,**{c:s}})        
        check(target[1:], {**reserved,**{s.class_name:s}})
  check(target,{})
  return valid_list

def print_possible_options(class_list, class_schedules):
  comb = valid_combinations(class_list, class_schedules)
  if not comb:
    print('No options are possible.')
  for i,option in enumerate(comb):
    print(f'\nOption {i+1}:')
    for cls, sched in option.items():
      print(f'{sched.class_name:<20} {sched}')
      
