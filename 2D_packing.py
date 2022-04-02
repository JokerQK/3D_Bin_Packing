from rectpack import newPacker

rectangles = [(140,102),(122,102),(122,90),(110,75),(138,89)] * 30
bins = [(580,227)]

packer = newPacker()

# Add the rectangles to packing queue
for r in rectangles:
    packer.add_rect(*r)

# Add the bins where the rectangles will be placed
for b in bins:
    packer.add_bin(*b)

# Start packing
packer.pack()

import matplotlib.pyplot as plt
from matplotlib import patches

output = []
for index, abin in enumerate(packer):
    bw, bh  = abin.width, abin.height # Here , width = length, height = width!!
    print('bin', bw, bh, "nr of rectangles in bin", len(abin))
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')
    for rect in abin:
        x, y, wid, len = rect.x, rect.y, rect.width, rect.height
        output.append([x,y,wid,len])
        plt.axis([0,bw,0,bh])
        print('rectangle', len,wid)
        ax.add_patch(
            patches.Rectangle(
                (x, y),  # (x,y)
                wid,          # width
                len,          # height
                facecolor="#00ffff",
                edgecolor="black",
                linewidth=3
            )
        )
    fig.savefig("rect_%(index)s.png" % locals(), dpi=144, bbox_inches='tight')

# printing the rectangle coordinates to plot them in P5JS
print(output)

#------------------------------------------------------------------------
