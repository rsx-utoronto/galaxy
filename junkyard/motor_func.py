def motor_move(motor, speed_fb,speed_lr,rotate,ser):#[-1,1] 0:STOP 10:FAST
	if motor == 1:
		if speed_fb > 0 and speed_lr == 0:#backward
			ser.write(chr(int(64-speed_fb*63)))
		elif speed_fb < 0 and speed_lr == 0:#forward
			ser.write(chr(int(64-speed_fb*63)))
		elif speed_fb == 0 and speed_lr > 0:#right
			ser.write(chr(int(64+speed_lr*63)))
		elif speed_fb == 0 and speed_lr < 0:#left
			#ser.write(chr(int(64+speed_lr*63)))
			ser.write(chr(int(63)))



		elif speed_fb < 0 and speed_lr > 0:#first quodrant
			ser.write(chr(int(64-speed_fb*63)))
		elif speed_fb < 0 and speed_lr < 0:#second quodrant
			ser.write(chr(int(64-speed_fb*63*0.5)))
		elif speed_fb > 0 and speed_lr < 0:#third quodrant
			ser.write(chr(int(64-speed_fb*63*0.5)))
		elif speed_fb > 0 and speed_lr > 0:#fourth quodrant
			ser.write(chr(int(64-speed_fb*63)))

		elif speed_fb == 0 and speed_lr == 0:
			if rotate >0 : #rotate right
				ser.write(chr(int(64+rotate*63)))
			elif rotate <0: #rotate left
				ser.write(chr(int(64+rotate*63)))
			else:
				ser.write(chr(63))

	if motor == 2:
		if speed_fb > 0 and speed_lr == 0:#backward
			ser.write(chr(int(191-speed_fb*63)))
		elif speed_fb < 0 and speed_lr == 0:#forward
			ser.write(chr(int(191-speed_fb*63)))
		elif speed_fb == 0 and speed_lr > 0:#right
			#ser.write(chr(int(191-speed_lr*63)))
			ser.write(chr(int(191)))
		elif speed_fb == 0 and speed_lr < 0:#left
			ser.write(chr(int(191-speed_lr*63)))

		elif speed_fb < 0 and speed_lr > 0:#first quodrant
			ser.write(chr(int(191-speed_fb*63*0.5)))
		elif speed_fb < 0 and speed_lr < 0:#second quodrant
			ser.write(chr(int(191-speed_fb*63)))
		elif speed_fb > 0 and speed_lr < 0:#third quodrant
			ser.write(chr(int(191-speed_fb*63)))
		elif speed_fb > 0 and speed_lr > 0:#fourth quodrant
			ser.write(chr(int(191-speed_fb*63*0.5)))

		elif speed_fb == 0 and speed_lr == 0:
			if rotate >0: #rotate right
				ser.write(chr(int(191-rotate*63)))
			elif rotate <0: #rotate left
				ser.write(chr(int(191-rotate*63)))
			else:
				ser.write(chr(192))

