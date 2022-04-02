# from rectpack import newPacker
import queue
from rectpack import newPacker
import matplotlib.pyplot as plt
from matplotlib import patches
import time

def rectPack(rectangles, lenXwid):
    packer = newPacker()
    rectangles = sorted(rectangles, key=lambda x: x[2])
    rectangles.reverse()

    repeatedLW = []
    parsedLW = []
    for (length, width, height, weight, number) in rectangles:
        for i in range (number) :
            packer.add_rect(*(length, width))
        if (length, width) not in parsedLW :
            parsedLW.append((length, width))
            continue
        else : 
            repeatedLW.append((length, width))

    # Add the rectangles to packing queue
    # for r in rectangles:
    #     packer.add_rect(*r)

    # Add the bins where the rectangles will be placed
    for b in lenXwid:
        packer.add_bin(*b)

    # Start packing
    packer.pack()

    output = []

    for index, abin in enumerate(packer):
        bw, bh  = abin.width, abin.height
        # print('bin', bw, bh, "nr of rectangles in bin", len(abin))
        # fig = plt.figure()
        # ax = fig.add_subplot(111, aspect='equal')
        for rect in abin:
            x, y, w, h = rect.x, rect.y, rect.width, rect.height
            output.append([x, y, w, h])

            # plt.axis([0, bw, 0, bh])
            # # print('rectangle', w, h)
            # ax.add_patch(
            #     patches.Rectangle(
            #     (x, y),  # (x,y)
            #     w,          # width
            #     h,          # height
            #     facecolor="#00ffff",
            #     edgecolor="black",
            #     linewidth=3
            # )
        # )


        # fig.savefig("rect_"+str(x)+str(y)+str(w)+str(h)+str(time.time())+".png", dpi=144, bbox_inches='tight')

        # plt.close(fig=fig)

    ans = rectangles 
    ans_coord = output
    for coordIndex, (x_coord, y_coord, length, width) in enumerate(output): 
        for rectIndex, (rec_len, rec_wid, rec_height, weight, numbers) in enumerate(rectangles):
            if ((length == rec_len and width == rec_wid) or (length == rec_wid and width == rec_len)) and ans[rectIndex][3] > 0:
                ans[rectIndex] = [
                    ans[rectIndex][0],  
                    ans[rectIndex][1],
                    ans[rectIndex][2],
                    ans[rectIndex][3],
                    ans[rectIndex][4]-1
                ]
                ans_coord[coordIndex] = [x_coord, y_coord, length, width, rec_height, weight]
                break
        
    return (ans_coord, ans)

# ------------------------------------------------------

q = queue.Queue()
global_obj = []

class Container():
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height

class Pallet():
    def __init__(self, length, width, height, x_global, y_global, z_global, obj_index):
        self.length = length
        self.width = width
        self.height = height
        self.x_global = x_global
        self.y_global = y_global
        self.z_global = z_global
        self.obj_index = obj_index
        self.total_weight = 0
        self.layer = 0

class Box():
    def __init__(self, length, width, height, layer, x_global,  y_global, z_global, obj_index, weight, base_on):
        self.length = length
        self.width = width
        self.height = height
        self.layer = layer
        self.x_global = x_global
        self.y_global = y_global
        self.z_global = z_global
        self.obj_index = obj_index
        self.weight = weight
        self.base_on = base_on
        

obj_index = 0

# api output
prev_output_list = [[0, 0, 102, 140], [102, 0, 102, 140], [204, 0, 102, 140], [306, 0, 102, 140], [408, 0, 102, 140], [510, 0, 102, 140], [612, 0, 102, 140], [714, 0, 102, 140], [816, 0, 102, 140], [918, 0, 102, 140], [1020, 0, 140, 102], [1020, 102, 140, 102], [0, 140, 110, 75], [110, 140, 110, 75], [220, 140, 110, 75], [330, 140, 110, 75], [440, 140, 110, 75], [550, 140, 110, 75], [660, 140, 110, 75], [770, 140, 110, 75], [880, 140, 110, 75]]
# available box num

remain_record = [[55, 32, 38, 20, 1000],
                 [71, 23, 47, 25, 1000],
                 [64, 26, 36, 30, 1000],]
                #  [48, 35, 37, 35, 1000],
                #  [21, 54, 22, 40, 1000],
                #  [62, 37, 48, 45, 1000],
                #  [52, 39, 37, 50, 1000],
                #  [46, 15, 25, 55, 1000],
                #  [65, 38, 28, 60, 1000],
                #  [35, 34, 48, 65, 1000]]

# layer 0
for obj in prev_output_list:
    
    x, y, l, w = obj

    P = Pallet(l, w, 12, x, y, 0, obj_index)

    q.put(P)
    
    global_obj.append(P)
    
    obj_index += 1

while not q.empty():
    
    current_obj = q.get()

    # call api 
    (deploy_box, remain_record) = rectPack(remain_record, [(current_obj.length, current_obj.width)]);

    for obj in deploy_box:

        x, y, l, w, h, weight = obj

        low_obj = current_obj
        
        if type(low_obj) != Pallet:

            based_on_type = type(low_obj.base_on)

            while based_on_type != Pallet:
                low_obj = low_obj.base_on
                based_on_type = type(low_obj.base_on)
            
            low_obj = low_obj.base_on

        if low_obj.total_weight + weight < 450:
            
            if current_obj.z_global + current_obj.height + h < 225: 
            
                B = Box(l, w, h, current_obj.layer + 1, current_obj.x_global + x, current_obj.y_global + y, current_obj.z_global + current_obj.height, obj_index, weight, current_obj)
            
                q.put(B)
            
                global_obj.append(B)
            
                low_obj.total_weight += weight
            
                obj_index += 1
            
            else:
                print(low_obj.obj_index, "Height Fail")
                
        tmp = {}
        for item in global_obj[:21]:
            tmp[item.obj_index] = item.total_weight
        print(tmp)
        

dict = {}
dimension = 0
for item in global_obj:
    dict[item.obj_index] = {'pos':{"x":item.x_global, "y":item.y_global, "z":item.z_global}, "w":item.length, "h":item.width, "d": item.height} 
    dimension += item.length * item.width * item.height
print(dict)
print("\n", dimension)