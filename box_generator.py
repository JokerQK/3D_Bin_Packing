import numpy as np
Len_box = 12
length_1 = np.random.randint(low = 20, high = 55, size = Len_box)
width_1 = np.random.randint(low = 15, high = 35, size = Len_box)
height_1 = np.random.randint(low = 15, high = 40, size = Len_box)
weight_1 = np.random.randint(low = 5, high = 25, size = Len_box)

print(length_1)
print(width_1)
print(height_1)

box_info = []

print("\n")
for l, w, h, wei in zip(length_1, width_1, height_1, weight_1):
    box_info.append([l, w, h, wei, 500])

print(box_info)