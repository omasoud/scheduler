
from scheduler import Schedule, Slot, Time
import json

CLASS_SCHEDULES_TEST_PRE={

  'Anim':
      [
            Schedule(slots=[Slot(day='Monday', start=Time(hour=10, minute=45), end=Time(hour=12,minute=35)),
                            Slot(day='Wednesday', start=Time(hour=10, minute=45), end=Time(hour=12,minute=35))]),
       
      ],

  'Phys Anthro':
      [
            Schedule(slots=[Slot(day='Monday', start=Time(hour=12, minute=30), end=Time(hour=13,minute=45)),
                            Slot(day='Wednesday', start=Time(hour=12, minute=30), end=Time(hour=13,minute=45))]),
                    
      ],

  'Cult Anthro':
      [
            Schedule(slots=[Slot(day='Monday', start=Time(hour=10, minute=45), end=Time(hour=12,minute=0)),
                            Slot(day='Wednesday', start=Time(hour=10, minute=45), end=Time(hour=12,minute=0))]), 
             
      ],


  'Photo':
      [
            Schedule(slots=[Slot(day='Tuesday', start=Time(hour=14, minute=0), end=Time(hour=16,minute=0)),
                            Slot(day='Thursday', start=Time(hour=14, minute=0), end=Time(hour=16,minute=0))]),
      ],

  'Paint':
      [
            Schedule(slots=[Slot(day='Monday', start=Time(hour=12, minute=30), end=Time(hour=14,minute=30)),
                            Slot(day='Wednesday', start=Time(hour=12, minute=30), end=Time(hour=14,minute=30))]),

     ],
  'Draw':
      [
            Schedule(slots=[Slot(day='Tuesday', start=Time(hour=10, minute=15), end=Time(hour=12,minute=15)),
                            Slot(day='Thursday', start=Time(hour=10, minute=15), end=Time(hour=12,minute=15))]),
       
       Schedule(slots=[Slot(day='Tuesday', start=Time(hour=15, minute=30), end=Time(hour=17,minute=30)),
                            Slot(day='Thursday', start=Time(hour=15, minute=30), end=Time(hour=17,minute=30))]),
       
      ]
}
CLASS_SCHEDULES_TEST_PRE['Art']=CLASS_SCHEDULES_TEST_PRE['Draw']+CLASS_SCHEDULES_TEST_PRE['Photo']+CLASS_SCHEDULES_TEST_PRE['Anim']

def fix_class_schedule(class_schedules_pre):
	# populate class name from key
	class_schedules = class_schedules_pre.copy()
	for k,v in class_schedules.items():
		for sched in v:
			if sched.class_name is None:
				sched.class_name = k
			# print(k,sched)
			for slot in sched.slots:
				if slot.day not in ['Monday','Tuesday','Wednesday','Thursday','Friday']:
					print(f'Error: {k} {slot}')
			for i in range(len(sched.slots)-1):
				if sched.slots[0].start!=sched.slots[i+1].start or sched.slots[0].end!=sched.slots[i+1].end:
					print(f'Warning: class {k} has different start/end times: {sched.slots[0]} {sched.slots[i+1]}')
	return class_schedules

CLASS_SCHEDULES_TEST = fix_class_schedule(CLASS_SCHEDULES_TEST_PRE)

JSON_TEST = '''
{
  "Anim": [
    {
      "slots": [
        {
          "day": "Monday",
          "start": "10:45",
          "end": "12:35"
        },
        {
          "day": "Wednesday",
          "start": "10:45",
          "end": "12:35"
        }
      ]
    }
  ],
  "Phys Anthro": [
    {
      "slots": [
        {
          "day": "Monday",
          "start": "12:30",
          "end": "13:45"
        },
        {
          "day": "Wednesday",
          "start": "12:30",
          "end": "13:45"
        }
      ]
    }
  ],
  "Cult Anthro": [
    {
      "slots": [
        {
          "day": "Monday",
          "start": "10:45",
          "end": "12:00"
        },
        {
          "day": "Wednesday",
          "start": "10:45",
          "end": "12:00"
        }
      ]
    }
  ],
  "Photo": [
    {
      "slots": [
        {
          "day": "Tuesday",
          "start": "14:00",
          "end": "16:00"
        },
        {
          "day": "Thursday",
          "start": "14:00",
          "end": "16:00"
        }
      ]
    }
  ],
  "Paint": [
    {
      "slots": [
        {
          "day": "Monday",
          "start": "12:30",
          "end": "14:30"
        },
        {
          "day": "Wednesday",
          "start": "12:30",
          "end": "14:30"
        }
      ]
    }
  ],
  "Draw": [
    {
      "slots": [
        {
          "day": "Tuesday",
          "start": "10:15",
          "end": "12:15"
        },
        {
          "day": "Thursday",
          "start": "10:15",
          "end": "12:15"
        }
      ]
    },
    {
      "slots": [
        {
          "day": "Tuesday",
          "start": "15:30",
          "end": "17:30"
        },
        {
          "day": "Thursday",
          "start": "15:30",
          "end": "17:30"
        }
      ]
    }
  ],
  "Art": [
	"Draw",
	"Photo",
	"Anim"
  ]
}
'''



def from_json(json_content):
	from dataclasses import asdict
	from datetime import datetime as dt

	def to_dt(time):
		return dt(year=2000,month=1,day=1,hour=time.hour,minute=time.minute)

	def to_time(time):
		# parse hh:mm 24-hour format time string to Time object
		return Time(hour=int(time.split(':')[0]), minute=int(time.split(':')[1]))

	def to_slot(slot):
		return Slot(day=slot['day'], start=to_time(slot['start']), end=to_time(slot['end']))

	def to_schedule(k, s):
		return Schedule(slots=[to_slot(slot) for slot in s['slots']], class_name=k)

	# return {k:[to_schedule(k, s) for s in v] for k,v in json_content.items()}
	ret = {}
	for k, v in json_content.items():
		if all([isinstance(s, str) for s in v]):
			missing = {s for s in v if s not in ret}
			if missing:
				raise ValueError(f'Class group {k} references classes that are not defined prior to this group: {missing}')
			ret[k] = sum([ret[s] for s in v], [])
		elif all([isinstance(s, dict) for s in v]):
			ret[k] = [to_schedule(k, s) for s in v]
		else:
			raise ValueError(f'Invalid JSON format for class {k}. Expected list of slot objects or list of strings (representing a group of classes)')
	return ret


		



def to_json(class_schedules):
	from dataclasses import asdict
	from json import dumps
	from datetime import datetime as dt

	def to_time(time):
		return f"{time.hour:02d}:{time.minute:02d}"

	def to_slot(slot):
		return {'day':slot.day, 'start':to_time(slot.start), 'end':to_time(slot.end)}

	def to_schedule(s):
		return {'slots':[to_slot(slot) for slot in s.slots]}

	return {k:[to_schedule(s) for s in v] for k,v in class_schedules.items()}

def test_from_json():
	from json import loads
	from pprint import pprint
	json_content = loads(JSON_TEST)
	pprint(from_json(json_content))
	assert from_json(json_content) == CLASS_SCHEDULES_TEST

def test_to_json():
	from json import loads
	from pprint import pprint
	json_content = loads(JSON_TEST)
	from_json_content = from_json(json_content) # this will validate the JSON content as well
	# class groups are not reversible once they are combined as a list of Schedule objects; so we will skip comparing them
	schedules_as_json = to_json(CLASS_SCHEDULES_TEST)
	comp1 = {}
	comp2 = {}
	for k,v in json_content.items():
		if not all([isinstance(s, str) for s in v]):
			comp1[k] = v
			comp2[k] = schedules_as_json[k]
		
	#assert to_json(CLASS_SCHEDULES_TEST) == json_content
	assert comp1 == comp2


def from_json_file(file):
	with open(file) as f:
		return from_json(json.load(f))