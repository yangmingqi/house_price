import sys, os
if hasattr(sys, 'frozen'):
	os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtGui import QRegExpValidator, QIntValidator, QDoubleValidator
from house_price import *
import numpy as np
 
class MyWindow(QWidget):  

	def __init__(self):  
	    super().__init__()
	    self.setWindowTitle('拆迁房价计算器')
	    
	    # 开始：
	    wlayout = QVBoxLayout() # 竖直
	    
	    hlayout = QHBoxLayout() # 水平
	    resout = QHBoxLayout()
	    glayout = QGridLayout() # 网格
	    
	    floorLabels = []
	    self.floorAreas = []
	    for i in range(6):
	        floorLabels.append(QLabel("{flooor}楼:{price}元/平米".format(flooor = i+1,price=a[i])))
	        self.floorAreas.append(QLineEdit(""))
	    floorLabels.append(QLabel("4楼(特价):{price}元/平米".format(price=a[-1])))
	    self.floorAreas.append(QLineEdit(""))

	    for i,(label, edit) in enumerate(zip(floorLabels, self.floorAreas)):
	        glayout.addWidget(label,i,0)
	        glayout.addWidget(edit,i,1)

	    couponLabel = QLabel("购房券/元")
	    self.couponEdit = QLineEdit()
	    glayout.addWidget(couponLabel,3,2)
	    glayout.addWidget(self.couponEdit,3,3)

	    hlayout.addStretch(1)
	    self.calBtn = QPushButton('计算')
	    self.calBtn.clicked.connect(self.calculate)
	    self.clearBtn = QPushButton('清空')
	    self.clearBtn.clicked.connect(self.clearText)
	    hlayout.addWidget(self.calBtn)
	    hlayout.addWidget(self.clearBtn)
	    hlayout.addStretch(1)

	    self.resTxt = QTextEdit("")
	    resout.addWidget(self.resTxt)

	    hwg = QWidget() # 准备四个部件
	    vwg = QWidget()
	    gwg = QWidget()
	    
	    gwg.setLayout(glayout)
	    hwg.setLayout(hlayout) # 四个部件设置局部布局
	    vwg.setLayout(resout)
	    
	    wlayout.addWidget(gwg)
	    wlayout.addWidget(hwg) # 四个部件加至全局布局
	    wlayout.addWidget(vwg)
	    
	    self.setLayout(wlayout) # 窗体本尊设置全局布局

	def calculate(self):
		areas = []
		for edit in self.floorAreas:
			try:
				area = float(edit.text())
			except:
				area = 0.
			areas.append(area)
		try:
			coupon = float(self.couponEdit.text())
		except:
			coupon = 0
		areas = np.array(areas)

		all_price, cheap_areas, mid_p_areas, h_p_areas = getAllPrice(areas, coupon)

		self.resTxt.clear()
		tplt = "{0:{3}^10}\t{1:{3}^10}\t{2:^10}"
		self.resTxt.append('购房券      {coupon}'.format(coupon=format(coupon, ',')))
		self.resTxt.append('购房面积    {areas}'.format(areas='%7d,'*len(areas) %(tuple(areas))))

		self.resTxt.append("购房总价:   {all_price}".format(all_price=format(all_price, ',')))
		self.resTxt.append('')
		self.resTxt.append('楼层:       {floor}'.format(floor='%7s'*len(a) %(tuple(['1楼','2楼','3楼','4楼','5楼','6楼','特价4楼']))))
		self.resTxt.append('拆迁价:     {a}'.format(a='%7d,'*len(a) %(tuple(a))))
		self.resTxt.append('拆迁面积:   {cheap_areas}'.format(cheap_areas='%7d,'*len(cheap_areas) %(tuple(cheap_areas))))
		self.resTxt.append('')
		self.resTxt.append('优惠价:     {b}'.format(b='%7d,'*len(b) %(tuple(b))))
		self.resTxt.append('优惠面积:   {mid_p_areas}'.format(mid_p_areas='%7d,'*len(mid_p_areas) %(tuple(mid_p_areas))))
		self.resTxt.append('')
		self.resTxt.append('市场价：    {c}'.format(c='%7d,'*len(c) %(tuple(c))))
		self.resTxt.append('市场价面积：{h_p_areas}'.format(h_p_areas='%7d,'*len(h_p_areas) %(tuple(h_p_areas))))
		self.resTxt.append('')
		self.resTxt.append('总房价：    {h_p_areas}'.format(h_p_areas='%7d,'*len(h_p_areas) %(tuple(a*cheap_areas+b*mid_p_areas+c*h_p_areas))))
		self.resTxt.append('')

		self.resTxt.append('购房总价 - 购房券 = {all_price} - {coupon} = {res_price}'.format(all_price=format(all_price, ','),coupon=format(coupon, ','),res_price=format(all_price - coupon, ',')))

	def clearText(self):
		for edit in self.floorAreas:
			edit.clear()
		self.couponEdit.clear()
		self.resTxt.clear()    

if __name__=="__main__":    
    import sys    
    
    app = QApplication(sys.argv)    
    win = MyWindow()  
    win.show()  
    sys.exit(app.exec_())