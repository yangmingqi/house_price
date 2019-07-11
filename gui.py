from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtGui import QRegExpValidator, QIntValidator, QDoubleValidator
from house_price import *
import numpy as np
 
class MyWindow(QWidget):  

	def __init__(self):  
	    super().__init__()
	    self.setWindowTitle('PyQt5布局示例')
	    
	    # 开始：
	    wlayout = QVBoxLayout() # 竖直
	    
	    hlayout = QHBoxLayout() # 水平
	    resout = QHBoxLayout()
	    glayout = QGridLayout() # 网格
	    
	    floorLabels = []
	    self.floorAreas = []
	    for i in range(6):
	        floorLabels.append(QLabel(f"{i+1}楼:{a[i]}元/平米"))
	        self.floorAreas.append(QLineEdit(""))

	    for i,(label, edit) in enumerate(zip(floorLabels, self.floorAreas)):
	        glayout.addWidget(label,i,0)
	        glayout.addWidget(edit,i,1)

	    couponLabel = QLabel(f"购房券")
	    self.couponEdit = QLineEdit()
	    glayout.addWidget(couponLabel,3,2)
	    glayout.addWidget(self.couponEdit,3,3)

	    hlayout.addStretch(1)
	    self.calBtn = QPushButton('计算')
	    self.calBtn.clicked.connect(self.calculate)
	    hlayout.addWidget(self.calBtn)
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
		cheap_price, cheap_areas = getcheapPrice(areas, coupon, sorted_h_price)
		mid_p_areas = getNormalPrice(areas-cheap_areas, sorted_middle_price)
		h_p_areas = areas-cheap_areas-mid_p_areas

		all_price = cheap_price + sum(mid_p_areas * b) + sum(h_p_areas * c)

		self.resTxt.clear()
		self.resTxt.append(f'购房券 {coupon}')
		self.resTxt.append(f'购房面积（1-6楼）{areas}')

		self.resTxt.append(f"购房总价: {all_price}")

		self.resTxt.append(f'拆迁价（1-6楼）: {a}')
		self.resTxt.append(f'拆迁面积（1-6楼）: {cheap_areas}')
		self.resTxt.append(f'优惠价（1-6楼）: {b}')
		self.resTxt.append(f'优惠面积（1-6楼）: {mid_p_areas}')
		self.resTxt.append(f'市场价（1-6楼）： {c}')
		self.resTxt.append(f'市场价面积（1-6楼）：{h_p_areas}')

		self.resTxt.append(f'购房总价 - 购房券 = {all_price - coupon}')
        

if __name__=="__main__":    
    import sys    
    
    app = QApplication(sys.argv)    
    win = MyWindow()  
    win.show()  
    sys.exit(app.exec_())