import get_operation as GetOp
import autopy as at
import time

GetOp.start()
print("finished!")
record = GetOp.getRecord()

for item in record:
	if item['type'] == 'wait':
		time.sleep(item['time'])
	elif item['type'] == 'click':
		at.smooth_move.move(item['position'][0]/1.5,item['position'][1]/1.5)
		at.mouse.click(at.mouse.Button.LEFT,0.2)
	elif item['type'] == 'keydown':
		at.key.toggle(item['key'],True,[])
		at.key.toggle(item['key'],False,[])

print("finished!")
