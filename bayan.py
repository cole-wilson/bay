import os, math
try:
	from PIL import Image
except:
	os.system('pip3 install pillow')
	from PIL import Image

def rounds(x, base):
    return base * round(x/base)
def compare(a,b,aperture,showprogress=False,highlight=True):
	s1 = a.scan(aperture)
	s2 = b.scan(aperture)

	mat = []
	ccc = 0
	coordsa = []
	coordsb = []

	for z in s1['content']:
		x = z['c']
		ccc = ccc + 1
		if showprogress:
			print('{}/{}'.format(ccc,s1['amount']))
		for a in s2['content']:
			if x == a['c']:
				mat.append(1)
				coordsa.append([z['x1'],z['y1'],z['x2'],z['y2']])
				coordsb.append([a['x1'],a['y1'],a['x2'],a['y2']])
				# print('Match!!\n')
				break
		# if highlight:
		# 	a.highlight(coordsa,aperture)
		# 	a.highlight(coordsb,aperture)
	return {
		'matches':len(mat),
		'%':100*(len(mat)/ccc),
		'cycles':ccc,
		'ca':coordsa,
		'cb':coordsb
	}

class image:
	def __init__(self,filename):
		im = Image.open(filename, 'r')
		imagewidth, height = im.size
		# print(im.size)
		self.width = imagewidth
		self.height = height
		pix_val = list(im.getdata())
		self.vals = []
		c = 0
		cc = []
		for x in pix_val:
			c = c + 1
			b = str(x).replace('(','').replace(')','').replace(' ','').split(',')[0:4]
			bn = []
			for f in b:
				bn.append(int(f))
			cc.append(bn)
			if c % imagewidth == 0:
				self.vals.append(cc)
				cc = []
			self.hl = self.vals
	def pixelate(self,base, smooth=1):
		self.smooth(smooth)
		yadd = []
		for y in range(1,self.height-1,base-1):
			xadd = []
			for x in range(1,self.width-1,base-1):
				rs = 0
				gs = 0
				bs = 0
				aas = 0
				count = 0
				ycount = 0
				try:
					ran = self.ran(x,y,x+base,y+base)
				except:
					break
				for b in ran:
					# print(y+base,end='')
					# print(' , ',end='')
					# print(x+base)
					
					ycount = ycount + 1
					for c in b:
						count = count + 1
						rs = rs + (c[0]**2)
						gs = gs + (c[1]**2)
						bs = bs + (c[2]**2)
						try:
							aas = aas + (c[3]**2)
						except:
							aas = 255
				av_r = round(math.sqrt(rs/count))
				av_g = round(math.sqrt(gs/count))
				av_b = round(math.sqrt(bs/count))
				av_a = round(math.sqrt(aas/count))
				if xadd != []:
					xadd.append([av_r,av_g,av_b,av_a])

			yadd.append(xadd)
		# self.vals = yadd
		for x in yadd:
			for y in range(base):
				if x != []:
					self.vals.append([x]*base)
		return self.vals
	def draw(self,highlight = False):
		try:
			import turtle
		except:
			print('Already imported turtle...')
		size = 5
		turtle.pensize(size-2)
		turtle.speed(999)
		c = 0
		if highlight:
			li1 = self.hl
		else:
			li1 = self.vals
		turtle.penup()
		turtle.goto(-300,200)
		c = 0
		for x in li1:
			print('{}/{}'.format(c,len(li1)))
			c = c + size - 2
			turtle.pendown()
			for y in x:
				try:
					turtle.pencolor((y[0],y[1],y[2],y[3]))
				except:
					turtle.pencolor((y[0],y[1],y[2]))
				turtle.forward(size-2)
			turtle.penup()
			turtle.goto(-300,-c+9)
		
			turtle.penup()

	def exwhy(self,x,y):
		return self.vals[x-1][y-1]
	def ran(self,x1,y1,x2,y2):
		y = y1
		cc = []
		while y <= y2:
			x = x1
			c = []
			while x <= x2:
				c.append(self.exwhy(x,y))
				x = x + 1
			y = y + 1
			cc.append(c)
		return cc
	def scan(self,aperture):
		a = []
		for y in range(1,len(self.vals)-aperture+1):
			for x in range(1,len(self.vals)-aperture+1):
				# a.append(self.ran(x,y,x+aperture-1,y+aperture-1))
				a.append(
					{
						'x1':x,
						'y1':y,
						'x2':x+aperture-1,
						'y2':y+aperture-1,
						'c':self.ran(x,y,x+aperture-1,y+aperture-1)
					}	
					)
		return {
			'aperture':aperture,
			'amount':len(a),
			'content':a
			}
	def highlightxy(self,xin,yin,inp):
		a = []
		for y in range(len(inp)):
			ys = []
			for x in range(len(inp[y])):
				if xin-1 == x and yin-1 == y:
					ys.append([255,0,0,150])
				else:
					ys.append(inp[y][x])
			a.append(ys)
		return(a)
	def highlight(self,listin,aperture):
		b = self.vals
		prevx = -aperture
		prevy = -aperture
		for x in listin:
			if x[0]-aperture>prevx and x[1]-aperture>prevy:
				prevx = x[0]
				prevy = x[1]
				for u in range(0,aperture):
					b = self.highlightxy(x[0]+u,x[1],b)
				for u in range(0,aperture):
					b = self.highlightxy(x[0],x[1]+u,b)
				for u in range(0,aperture):
					b = self.highlightxy(x[0]+aperture,x[1]+u,b)
				for u in range(0,aperture):
					b = self.highlightxy(x[0]+u,x[1]+aperture,b)
		self.hl = b
		return b
	def smooth(self,base):
		al = []
		for y in self.vals:
			yadd = []
			for x in y:
				xadd = []
				for v in x:
					xadd.append(rounds(v,base))
				yadd.append(xadd)
			al.append(yadd)
		self.vals = al
		return True