# 使用方法

​		本程序将**OVITO pro**中原本收费的代码, 通过官方提供的**API**进行封装之后再供同学们调用, 简化了许多不必要的麻烦, 本代码主要是对**OVITO pro**中的**Spatial binning**模块进行封装, 以实现LAMMPS中类似于compute chunk类似的功能, 本代码共提供了5个函数以供同学们进行调用, 具体用法和意义如下:

```python
Bin_1d(fileName, outputName, itemName, axis, counts, operation="mean", isDeriv=False, isReturn=False):
  '''
  此函数用于将导入的原子模型在一维方向上进行切割, 并计算对应的property, 然后将结果输出, 各输入参数意义如下
  fileName  : 字符串类型, 模型文件的名称
  outputName: 字符串类型, 输出的结果文件的名称, 类型为txt格式, 只有2列数据, 可以用熟练的绘图软件读取数据并绘制曲线
  itemName  : 字符串类型, 需要在某一个方向上进行平均的propertyname, 对应dump文件中ITEMS那一行的输出
  axis      : 字符串类型, 在哪个轴上面进行切割
  counts    : 整数类型, 在对应的轴上面共切割几份
  operation : 字符串类型, 默认为mean, 意思是将chunk内部的所有原子的property加起来再除以chunk中原子数量
  isDeriv   : 逻辑变量, 默认为false, 这个选项只对1维有效, 意思是是否对获得的曲线求取一阶导数
  isReturn  : 逻辑变量, 默认为false, 意思是是否返回numpy结果, 如果改成True需要用一个变量来接受计算出来的numpy矩阵
  '''
```

```python
Bin_2d(fileName, outputName, itemName, axis, counts, 
           operation="mean"):
  '''
  此函数用于将导入的原子模型在一维方向上进行切割, 并计算对应的property, 然后将结果输出, 各输入参数意义如下
  fileName  : 字符串类型, 模型文件的名称
  outputName: 字符串类型, 输出的结果文件的名称, 类型为VTK格式, 可以使用paraview进行查看和后处理
  itemName  : 字符串类型, 需要在某一个方向上进行平均的propertyname, 对应dump文件中ITEMS那一行的输出
  axis      : 字符串类型, 在哪个轴上面进行切割, 可以选择的方向有xy, xz, yz
  counts    : 元组类型, 含有2个整数在对应的轴上面共切割几份
  operation : 字符串类型, 默认为mean, 意思是将chunk内部的所有原子的property加起来再除以chunk中原子数量
  '''
```

```python
Bin_3d(fileName, outputName, itemName, counts, 
           operation="mean"):
  '''
  此函数用于将导入的原子模型在三维方向上进行切割, 并计算对应的property, 然后将结果输出, 各输入参数意义如下
  fileName  : 字符串类型, 模型文件的名称
  outputName: 字符串类型, 输出的结果文件的名称, 类型为VTK格式, 可以使用paraview进行查看和后处理
  itemName  : 字符串类型, 需要在某一个方向上进行平均的propertyname, 对应dump文件中ITEMS那一行的输出
  counts    : 元组类型, 含有3个整数在对应的xyz轴上面共切割几份
  operation : 字符串类型, 默认为mean, 意思是将chunk内部的所有原子的property加起来再除以chunk中原子数量
  '''
```

```python
density_2d(fileName, outputName, counts, axis,
           operation="sumvol"):
  '''
  此函数用于计算导出绘制原子模型的二维密度云图, 以下是各参数的具体意义:
  fileName  : 字符串类型, 模型文件的名称
  outputName: 字符串类型, 输出的结果文件的名称, 类型为VTK格式, 可以使用paraview进行查看和后处理
  axis      : 字符串类型, 在哪个轴上面进行切割, 可以选择的方向有xy, xz, yz
  counts    : 元组类型, 含有2个整数在对应的xyz轴上面共切割几份
  operation : 字符串类型, 默认为sumvol, 意思是平均数密度, 即用原子数除以chunk体积
  '''
```

```python
density_3d(fileName, outputName, counts,
           operation="sumvol"):
  '''
  此函数用于计算导出绘制原子模型的三维密度云图, 以下是各参数的具体意义:
  fileName  : 字符串类型, 模型文件的名称
  outputName: 字符串类型, 输出的结果文件的名称, 类型为VTK格式, 可以使用paraview进行查看和后处理
  counts    : 元组类型, 含有3个整数在对应的xyz轴上面共切割几份
  operation : 字符串类型, 默认为sumvol, 意思是平均数密度, 即用原子数除以chunk体积
  '''
```

​		同时在**main.py**文件中, 提供了5种函数的具体调用方法, 测试文件**Fe_tension1000.xyz**是我之前做的一个模型, **v_mises**是我在in文件里面编程计算出来的原子**mises**应力. 

​		而**final_cool.lmp**是我做的一个**CuNb**的非晶金属玻璃模型, 用于绘制2d密度云图的演示, 密度云图这一块貌似都是以二维的为主, 所以我只提供了**二维和三维**的数据导出函数.



# 计算结果展示

**Bin_1d:**

![](.\picture\bin1d.png)

**Bin_2d:**

![](.\picture\bin_2d.png)

**Bin_3d:**

![](.\picture\bin_3d.png)



**density_2d:**

![](.\picture\density2d.png)



**density_3d:**

![](.\picture\density3d.png)



最后关于**paraview**的下载安装和使用, 就请同学们自行**bing**查找资料学习了, 基础操作还是非常简单易懂的.