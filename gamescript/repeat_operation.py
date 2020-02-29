import autopy as at
import time

# 重复一次
def repeat(record, times):
	print("repeat start!")
	for i in range(times):
		for item in record:
			if item['type'] == 'wait':
				time.sleep(item['time'])
			elif item['type'] == 'click':
				at.mouse.smooth_move(item['position'][0]/1.5,item['position'][1]/1.5)
				at.mouse.click(at.mouse.Button.LEFT,0.2)
			elif item['type'] == 'keydown':
				at.key.toggle(item['key'],True,[])
				at.key.toggle(item['key'],False,[])
	print("repeat finished!")
