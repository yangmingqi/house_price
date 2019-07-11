import numpy as np

a = [2200, 2418, 2558, 2318, 2028, 1678]
b = [2550, 2768, 2908, 2668, 2378, 2028]
c = [4360, 4690, 4890, 4590, 4210, 3420]

a = np.array(a)
b = np.array(b)
c = np.array(c)

dic = {}
for i, price in enumerate(a):
    dic[i] = price
sorted_h_price = sorted(dic.items(), key=lambda item:item[1])
sorted_h_price

dic = {}
for i, price in enumerate(b):
    dic[i] = price
sorted_middle_price = sorted(dic.items(), key=lambda item:item[1])
sorted_middle_price

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
                if sum_cheap_areas + area > 300:
                    area = 300 - sum_cheap_areas
                    cheap_price += area * price
                    cheap_areas[floor] = area
                    return cheap_price, cheap_areas
                    
                coupon -= area * price
                cheap_price += area * price
                cheap_areas[floor] = area
                continue
            else:
                area = coupon / price
                if sum_cheap_areas + area > 300:
                    area = 300 - sum_cheap_areas
                    cheap_price += area * price
                    cheap_areas[floor] = area
                    return cheap_price, cheap_areas
                else:
                    cheap_price += coupon
                    area = round(coupon / price, 2)
                    cheap_areas[floor] = area
#                     print(area,cheap_areas)
                    return cheap_price, cheap_areas
    return cheap_price, cheap_areas

def getNormalPrice(areas, sorted_middle_price):
    mid_p_areas = [0] * len(areas)
    sum_mid_p_area = 20
    
    for floor, price in sorted_middle_price:
        area = areas[floor]
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
    cheap_price, cheap_areas = getcheapPrice(areas, coupon, sorted_h_price)
    mid_p_areas = getNormalPrice(areas-cheap_areas, sorted_middle_price)
    h_p_areas = areas-cheap_areas-mid_p_areas
    all_price = cheap_price + sum(mid_p_areas * b) + sum(h_p_areas * c)
    return all_price, cheap_areas, mid_p_areas, h_p_areas

# coupon = 0
# areas = [110, 0, 0, 0, 0, 0]
# areas = np.array(areas)
# cheap_price, cheap_areas = getcheapPrice(areas, coupon, sorted_h_price)
# print(cheap_areas)
# mid_p_areas = getNormalPrice(areas-cheap_areas, sorted_middle_price)
# h_p_areas = areas-cheap_areas-mid_p_areas

# all_price = cheap_price + sum(mid_p_areas * b) + sum(h_p_areas * c)

# print('购房券', coupon)
# print('购房面积（1-6楼）', areas, '\n')

# print("购房总价:" , all_price, '\n')

# print('拆迁价（1-6楼）:', a)
# print('拆迁面积（1-6楼）:', cheap_areas, '\n')
# print('优惠价（1-6楼）:', b)
# print('优惠面积（1-6楼）:', mid_p_areas, '\n')
# print('市场价（1-6楼）：', c)
# print('市场价面积（1-6楼）：', h_p_areas, '\n')

# print('购房券 - 购房总价 = ', coupon - all_price)