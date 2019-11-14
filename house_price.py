import numpy as np
from decimal import Decimal, ROUND_HALF_UP

# a = [2200, 2418, 2558, 2318, 2028, 1678]
# b = [2550, 2768, 2908, 2668, 2378, 2028]
# c = [4360, 4690, 4890, 4590, 4210, 3420]

a = [2400, 2638, 2868, 2564, 2296, 1634, 1694]
b = [2750, 2988, 3218, 2914, 2646, 1984, 2044]
c = [4560, 4890, 4990, 4790, 4410, 3720, 3800]

a = np.array(a)
b = np.array(b)
c = np.array(c)

dic = {}
for i, price in enumerate(a):
    dic[i] = price
sorted_cheap_price = sorted(dic.items(), key=lambda item:item[1])

dic = {}
for i, price in enumerate(b):
    dic[i] = price
sorted_middle_price = sorted(dic.items(), key=lambda item:item[1])

def round_up(value):
    # 替换内置round函数,实现保留2位小数的精确四舍五入
    return round(value * 100) / 100.0

def getcheapPrice(areas, coupon, sorted_price):
    cheap_price = 0
    cheap_areas = [0] * len(areas)
    for floor, price in sorted_price:
        area = areas[floor]
        sum_cheap_areas = sum(cheap_areas)
        if coupon <= 0:
            return cheap_price, cheap_areas
        if area > 0:
            if coupon >= area * price:
                # if sum_cheap_areas + area > 280:
                #     area = 280 - sum_cheap_areas
                #     cheap_price += area * price
                #     cheap_areas[floor] = area
                #     return cheap_price, cheap_areas
                    
                coupon -= area * price
                cheap_price += area * price
                cheap_areas[floor] = area
                continue
            else:
                # area = round_up(coupon / price)

                # area = decimal.Decimal(str(coupon / price)).quantize(decimal.Decimal("0.00"))
                # if sum_cheap_areas + area > 280:
                #     area = 280 - sum_cheap_areas
                #     cheap_price += area * price
                #     cheap_areas[floor] = area
                #     return cheap_price, cheap_areas
                # else:
                cheap_price += coupon
                # area = round(coupon / price, 2)
                area = Decimal(str(coupon / price)).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
                cheap_areas[floor] = float(area)
                return cheap_price, cheap_areas
    return cheap_price, cheap_areas

def getNormalPrice(areas, sorted_middle_price):
    mid_p_areas = [0] * len(areas)
    sum_mid_p_area = 20
    
    for floor, price in sorted_middle_price:
        area = areas[floor]
        area = Decimal(str(area)).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
        area = float(area)
        if sum_mid_p_area <= 0:
            return mid_p_areas
        if area <= sum_mid_p_area:
            mid_p_areas[floor] = area
            sum_mid_p_area -= area
        else:
            mid_p_areas[floor] = sum_mid_p_area
            return mid_p_areas
    return mid_p_areas

def getAllPrice(areas, coupon):
    if coupon == 0:
        return sum(areas * c), [0] * len(areas), [0] * len(areas), areas
    cheap_price, cheap_areas = getcheapPrice(areas, coupon, sorted_cheap_price)
    if sum(cheap_areas) > 280:
        sum_cheap_areas = 0
        for k, v in sorted_cheap_price:
            if cheap_areas[k] <= 280 - sum_cheap_areas:
                sum_cheap_areas += cheap_areas[k]
            else:
                cheap_areas[k] = 280 - sum_cheap_areas
                sum_cheap_areas = 280

    cheap_areas = [Decimal(str(a)).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP) for a in cheap_areas]
    cheap_areas = np.array([float(a) for a in cheap_areas])
    # cheap_price = Decimal(str(cheap_price)).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
    # cheap_price = float(cheap_price)

    mid_p_areas = getNormalPrice(areas-cheap_areas, sorted_middle_price)
    h_p_areas = areas-cheap_areas-mid_p_areas
    h_p_areas = [Decimal(str(a)).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP) for a in h_p_areas]
    h_p_areas = np.array([float(a) for a in h_p_areas])
    all_price = cheap_price + sum(mid_p_areas * b) + sum(h_p_areas * c)
    all_price = Decimal(str(all_price)).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
    all_price = float(all_price)
    return  all_price, cheap_areas, mid_p_areas, h_p_areas


if __name__ == '__main__':
	coupon = 1464189.04
	areas = [82.03, 89, 65, 0, 106, 0, 0]
	areas = np.array(areas)
	cheap_areas, mid_p_areas, h_p_areas = getAllPrice(areas, coupon)

	# cheap_price, cheap_areas = getcheapPrice(areas, coupon, sorted_cheap_price)
	# print(cheap_areas, areas-cheap_areas)
	# mid_p_areas = getNormalPrice(areas-cheap_areas, sorted_middle_price)
	# h_p_areas = areas-cheap_areas-mid_p_areas

	all_price = sum(a*cheap_areas+b*mid_p_areas+c*h_p_areas)

	print('购房券', coupon)
	print('购房面积（1-6楼）', areas, '\n')

	print("购房总价:" , round(all_price,2), '\n')

	print('拆迁价（1-6楼）:', a)
	print('拆迁面积（1-6楼）:', cheap_areas,2, '\n')
	print('优惠价（1-6楼）:', b)
	print('优惠面积（1-6楼）:', [round(area,2) for area in mid_p_areas], '\n')
	print('市场价（1-6楼）：', c)
	print('市场价面积（1-6楼）：', [round(area,2) for area in h_p_areas], '\n')

	print('购房券 - 购房总价 = ', round(coupon - all_price,2))