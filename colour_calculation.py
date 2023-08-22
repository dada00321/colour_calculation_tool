import math

def RGB_to_XYZ(rgb_colour):
	R, G, B = rgb_colour
	
	r = R / 255.0
	g = G/ 255.0
	b = B / 255.0
	
	# Inverse sRGB Companding
	r = ((r+0.055)/1.055)**2.4 if r > 0.04045 else r/12.92
	g = ((g+0.055)/1.055)**2.4 if g > 0.04045 else g/12.92
	b = ((b+0.055)/1.055)**2.4 if b > 0.04045 else b/12.92
    
	'''
	Transform Matrix from linear RGB to XYZ:
	(http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html)
	=> D65, sRGB
	 [[0.4124564  0.3575761  0.1804375]
	  [0.2126729  0.7151522  0.0721750]
	  [0.0193339  0.1191920  0.9503041]]
	'''
	x = 0.4124564 * r +  0.3575761 * g + 0.1804375 * b
	y = 0.2126729 * r +  0.7151522 * g + 0.0721750 * b
	z = 0.0193339 * r +  0.1191920 * g + 0.9503041 * b
	#print(f"xyz: {(x,y,z)}")
	return (x,y,z)
	
def XYZ_to_Lab(XYZ):
	'''
	Transform Matrix from linear XYZ to Lab:
	(http://www.brucelindbloom.com/index.html?Eqn_XYZ_to_Lab.html)
	=> D65, sRGB
	 [[0.4124564  0.3575761  0.1804375]
	  [0.2126729  0.7151522  0.0721750]
	  [0.0193339  0.1191920  0.9503041]]
	'''
	print(f"XYZ: {XYZ}\n")
	
	k = 903.3
	e = 0.008856
	
	'''
	Ref:
	(1) Convert CIEXYZ into CIELAB
		"Calculating CIELAB Coordinates", Color Appearance Models - 3rd Edition, p202
	(2) XYZ values of Reference White
		"3.18 CIEDE2000 WORKED EXAMPLE", Measuring Colour, p69
	'''
	#X_r, Y_r, Z_r = 94.811, 100.000, 107.304
	
	'''
	Ref:
		White reference illuminant, "d65"
		https://www.mathworks.com/help/images/ref/whitepoint.html
	'''
	X_r, Y_r, Z_r = 0.9504, 1.0000, 1.0888
	
	X, Y, Z = XYZ
	
	x_r = X / X_r
	y_r = Y / Y_r
	z_r = Z / Z_r
	
	f_x = x_r**(1/3) if x_r > e else (k * x_r + 16) / 116
	f_y = y_r**(1/3) if y_r > e else (k * y_r + 16) / 116
	f_z = z_r**(1/3) if z_r > e else (k * z_r + 16) / 116
	
	L = 116 * (f_y) - 16
	#print("Lightness: L")
	a = 500 * (f_x - f_y)
	b = 200 * (f_y - f_z)
	return (L, a, b)

def Lab_to_LCh(Lab):
	'''
	Ref:
		(1) Formula of Lab to LCh
			http://www.brucelindbloom.com/index.html?Eqn_Lab_to_LCH.html
		(2) Usage of `math.atan2`
			https://www.runoob.com/python/func-number-atan2.html
		(3) Online colour picker
			https://www.nixsensor.com/free-color-converter/
	'''
	L, a, b = Lab
	C = round((a**2 + b**2)**0.5, 1)
	h = math.atan2(b, a) * (180 / math.pi)
	if h < 0:  
		h+= 360
	if a == 0: 
		a = 0.0001
	h = int(round(h, 0))
	return (L, C, h)

def Lab_to_XYZ(Lab):
	'''
	Transform Matrix from linear Lab to XYZ:
	(http://www.brucelindbloom.com/index.html?Eqn_Lab_to_XYZ.html)
	'''
	L, a, b = Lab
	f_y = (L+16) / 116
	f_x = a/500 + f_y
	f_z = f_y - b/200
	e = 0.008856
	k = 903.3
	
	x_r = f_x**3 if f_x**3 > e else (116*f_x-16)/k
	y_r = ((L+16)/116)**3 if L > k*e else L/k
	z_r = f_z**3 if f_z**3 > e else (116*f_z-16)/k
	
	X_r, Y_r, Z_r = 0.9504, 1.0000, 1.0888
	X = x_r * X_r
	Y = y_r * Y_r
	Z = z_r * Z_r
	
	return (X, Y, Z)
	
def XYZ_to_RGB(XYZ):
	'''
	Transform Matrix from linear XYZ to RGB:
	(http://www.brucelindbloom.com/index.html?Eqn_XYZ_to_RGB.html)
	
	=> D65, sRGB
	(http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html)
	[[3.2404542 -1.5371385 -0.4985314]
	 [-0.9692660  1.8760108  0.0415560]
	 [0.0556434 -0.2040259  1.0572252]]
	'''
	X, Y, Z = XYZ
	
	r = 3.2404542 * X -1.5371385 * Y -0.4985314 * Z
	g = -0.9692660 * X +1.8760108 * Y +0.0415560 * Z
	b = 0.0556434 * X -0.2040259 * Y +1.0572252 * Z
	
	# sRGB Companding
	r = 1.055*(r**(1/2.4)) - 0.055 if r > 0.0031308 else 12.92 * r
	g = 1.055*(g**(1/2.4)) - 0.055 if g > 0.0031308 else 12.92 * g
	b = 1.055*(b**(1/2.4)) - 0.055 if b > 0.0031308 else 12.92 * b
		
	R = int(round(255.0 * r, 0))
	G = int(round(255.0 * g, 0))
	B = int(round(255.0 * b, 0))
	
	return R,G,B
	
def CIEDE2000(rgb_1, rgb_2):
	'''
	Calculates CIEDE2000 color distance between two CIE L*a*b* colors
	Ref:
		https://github.com/lovro-i/CIEDE2000/blob/master/ciede2000.py
	'''
	
	xyz_1, xyz_2 = RGB_to_XYZ(rgb_1), RGB_to_XYZ(rgb_2)
	Lab_1, Lab_2 = XYZ_to_Lab(xyz_1), XYZ_to_Lab(xyz_2)
	
	C_25_7 = 6103515625 # 25**7
	
	L1, a1, b1 = Lab_1[0], Lab_1[1], Lab_1[2]
	L2, a2, b2 = Lab_2[0], Lab_2[1], Lab_2[2]
	C1 = math.sqrt(a1**2 + b1**2)
	C2 = math.sqrt(a2**2 + b2**2)
	C_ave = (C1 + C2) / 2
	G = 0.5 * (1 - math.sqrt(C_ave**7 / (C_ave**7 + C_25_7)))
	
	L1_, L2_ = L1, L2
	a1_, a2_ = (1 + G) * a1, (1 + G) * a2
	b1_, b2_ = b1, b2
	
	C1_ = math.sqrt(a1_**2 + b1_**2)
	C2_ = math.sqrt(a2_**2 + b2_**2)
	
	if b1_ == 0 and a1_ == 0: h1_ = 0
	elif a1_ >= 0: h1_ = math.atan2(b1_, a1_)
	else: h1_ = math.atan2(b1_, a1_) + 2 * math.pi
	
	if b2_ == 0 and a2_ == 0: h2_ = 0
	elif a2_ >= 0: h2_ = math.atan2(b2_, a2_)
	else: h2_ = math.atan2(b2_, a2_) + 2 * math.pi

	dL_ = L2_ - L1_
	dC_ = C2_ - C1_	
	dh_ = h2_ - h1_
	if C1_ * C2_ == 0: dh_ = 0
	elif dh_ > math.pi: dh_ -= 2 * math.pi
	elif dh_ < -math.pi: dh_ += 2 * math.pi		
	dH_ = 2 * math.sqrt(C1_ * C2_) * math.sin(dh_ / 2)
	
	L_ave = (L1_ + L2_) / 2
	C_ave = (C1_ + C2_) / 2
	
	_dh = abs(h1_ - h2_)
	_sh = h1_ + h2_
	C1C2 = C1_ * C2_
	
	if _dh <= math.pi and C1C2 != 0: h_ave = (h1_ + h2_) / 2
	elif _dh  > math.pi and _sh < 2 * math.pi and C1C2 != 0: h_ave = (h1_ + h2_) / 2 + math.pi
	elif _dh  > math.pi and _sh >= 2 * math.pi and C1C2 != 0: h_ave = (h1_ + h2_) / 2 - math.pi 
	else: h_ave = h1_ + h2_
	
	T = 1 - 0.17 * math.cos(h_ave - math.pi / 6) + 0.24 * math.cos(2 * h_ave) + 0.32 * math.cos(3 * h_ave + math.pi / 30) - 0.2 * math.cos(4 * h_ave - 63 * math.pi / 180)
	
	h_ave_deg = h_ave * 180 / math.pi
	if h_ave_deg < 0: h_ave_deg += 360
	elif h_ave_deg > 360: h_ave_deg -= 360
	dTheta = 30 * math.exp(-(((h_ave_deg - 275) / 25)**2))
	
	R_C = 2 * math.sqrt(C_ave**7 / (C_ave**7 + C_25_7))  
	S_C = 1 + 0.045 * C_ave
	S_H = 1 + 0.015 * C_ave * T
	
	Lm50s = (L_ave - 50)**2
	S_L = 1 + 0.015 * Lm50s / math.sqrt(20 + Lm50s)
	R_T = -math.sin(dTheta * math.pi / 90) * R_C

	k_L, k_C, k_H = 1, 1, 1
	
	f_L = dL_ / k_L / S_L
	f_C = dC_ / k_C / S_C
	f_H = dH_ / k_H / S_H
	
	dE_00 = math.sqrt(f_L**2 + f_C**2 + f_H**2 + R_T * f_C * f_H)
	return dE_00

de_00 = CIEDE2000((241,214,147), (248,236,202))
print(f"實際 icon 顏色和輸入 L*a*b* 到線上選色網站呈現顏色的色差: {de_00}")