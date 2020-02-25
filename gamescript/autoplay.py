import autopy as at
import time
import math

def fight(enemyblood,attack,buttonX,buttonY):
	at.mouse.move(buttonX/1.5,buttonY/1.5)
	at.mouse.click(at.mouse.Button.LEFT,0.1)
	time.sleep(0.5)
	count = math.ceil(enemyblood/attack)
	print("敌人血量{},我方攻击力{},需要{}个回合".format(enemyblood,attack,count))
	for i in range(count):
		print("第{}回合".format(i+1))
		at.mouse.move(520/1.5,520/1.5)
		at.mouse.click(at.mouse.Button.LEFT,0.2)
		time.sleep(0.6)
		at.mouse.click(at.mouse.Button.LEFT,0.2)
		time.sleep(5)
	time.sleep(0.5)
	at.mouse.click(at.mouse.Button.LEFT,0.2)
	time.sleep(1)

def loopfight(num,blood,attack,buttonX,buttonY):
	for i in range(num):
		print("第{}/{}轮".format(i+1,num))
		fight(blood,attack,buttonX,buttonY)

# loopfight(10, 400, 75, 173, 436)
loopfight(2, 600, 125, 523, 285)