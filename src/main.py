from SpatialBinning import Bin_1d, Bin_2d, Bin_3d, density_2d, density_3d

Bin_1d(fileName="../model/Fe_tension1000.xyz", 
       outputName="../result/pyresult1.txt",
       itemName="v_mises", 
       axis="Z", 
       counts=10)

Bin_2d(fileName="../model/Fe_tension1000.xyz", 
       outputName="../result/pyresult2d.vtk",
       itemName="v_mises", 
       axis="xy", 
       counts=(10, 10))

Bin_3d(fileName="../model/Fe_tension1000.xyz", 
       outputName="../result/pyresult3d.vtk",
       itemName="v_mises", 
       counts=(10, 10, 10))

density_2d(fileName="../model/final_cool.lmp", 
       outputName="../result/density2d.vtk", 
       axis="xy", 
       counts=(30, 30),
       operation='sumvol'
)

density_3d(fileName="../model/final_cool.lmp", 
       outputName="../result/density3d.vtk",  
       counts=(30, 30, 30),
       operation='sumvol'
)

# 如果我们希望获取计算过程中的具体矩阵来进行绘图, 将isReturn改成True即可
# array = Bin_1d("../model/Fe_tension1000.xyz", 
#        "../result/pyresult.txt",
#        "v_mises", 
#        "Z", 
#        10, isReturn=True)

# x = array[:, 0]
# y = array[:, 1]

# plt.plot(x, y)
# plt.show()

