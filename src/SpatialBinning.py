from ovito.io import import_file, export_file
from ovito.modifiers import SpatialBinningModifier as SBM
from ovito.modifiers import ComputePropertyModifier as CPM
from ovito.data import *
import numpy as np
import os

def Bin_1d(fileName, outputName, itemName, axis, counts, operation="mean", isDeriv=False, isReturn=False):
  '''
  此函数用于将导入的原子模型在一维方向上进行切割, 并计算对应的property, 然后将结果输出, 各输入参数意义如下
  fileName  : 字符串类型, 模型文件的名称
  outputName: 字符串类型, 输出的结果文件的名称
  itemName  : 字符串类型, 需要在某一个方向上进行平均的propertyname, 对应dump文件中ITEMS那一行的输出
  axis      : 字符串类型, 在哪个轴上面进行切割
  counts    : 整数类型, 在对应的轴上面共切割几份
  operation : 字符串类型, 默认为mean, 意思是将chunk内部的所有原子的property加起来再除以chunk中原子数量
  isDeriv   : 逻辑变量, 默认为false, 这个选项只对1维有效, 意思是是否对获得的曲线求取一阶导数
  isReturn  : 逻辑变量, 默认为false, 意思是是否返回numpy结果, 如果改成True需要用一个变量来接受计算出来的numpy矩阵
  '''
  # 首先检查文件是否存在
  if not os.path.exists(fileName):
    raise FileNotFoundError("The file " + fileName + " does not exist.")
  
  # 接着检查传入的counts是否为整数
  if not isinstance(counts, int):
    raise TypeError("The type of variable 'counts' must be integer.")
  else: # 然后检查传入的counts是否大于1, 因为至少需要切割2份 
    if counts < 1:
      raise ValueError("The value of counts must be greater than 1.")
  
  # 检查传入的itemName是否为字符串
  if not isinstance(itemName, str):
    raise TypeError("The type of variable 'itemName' must be string.")
  
  # 根据用户传入的axis选择方向, python中没有提供Switch语法, 故使用字典代替
  axis_dict={
    'X': SBM.Direction.X,
    'x': SBM.Direction.X,
    'Y': SBM.Direction.Y,
    'y': SBM.Direction.Y,
    'Z': SBM.Direction.Z,
    'z': SBM.Direction.Z
  }

  # 根据传入的key值, 也就是axis变量的值返回对应结果, 如果在字典里面没有找到对应对象, 那么返回一个0
  axis1 = axis_dict.get(axis, 0)   

  # 如果发现返回值为0, 就给出报错, 并终止程序
  if axis1 == 0: 
    raise ValueError("The value of variable 'axis' is inappropriate.")
  
  # 判断是否传入了operation
  if (operation != "mean"):   # 如果发现传入的operation不是默认的mean, 进行一系列的检测

    # 按照和上述的axis一样的做法, 同样定义一个字典来检测operation的输入, 但是先检测传入的operation是否是字符串类型
    if not isinstance(operation, str):
      raise TypeError("The type of variable 'operation' must be string.")
    
    # 接着检查传入的字符串是否全部都是英文
    if not operation.isalpha():
      raise ValueError("The content of variable 'operation' must be Alphabet.")
    
    # 运行到此, operation变量应该是没错了, 然后我们利用和上述axis一样的做法, 设置一个字典实现Switch的功能
    tmp_operation = operation.lower()   # 设置一个临时变量, 将字符串全部转成小写
    operation_dict={
      "mean": SBM.Operation.Mean,
      "min": SBM.Operation.Min,
      "max": SBM.Operation.Max,
      "sum": SBM.Operation.Sum,
      "sumvol": SBM.Operation.SumVol
    }

    # 根据传入的操作选择对应的操作
    RealOperation = operation_dict.get(tmp_operation, 0)

    if (RealOperation == 0):
      raise TypeError("The value of variable 'Operation' is inappropriate.")
  else:
    RealOperation = SBM.Operation.Mean
  # 至此, 对所有传入参数的检查以及处理全部完成, 可以开始正式调用OVITO进行数据处理计算

  # 将模型导入计算空间
  pipeline = import_file(fileName)
  
  # 获取当前模型里面具体有哪些property
  itemList = list(pipeline.compute().particles.keys())

  # 检查传入的itemName是否在这个列表里面
  if not itemName in itemList:
    raise ValueError("The property " + itemName + " not seen in file " + fileName + ".")
  
  # 如果程序运行到此处还没有报错, 那么说明数据输入没有问题, 那么我们将调用OVITO进行计算
  pipeline.modifiers.append(SBM(
                          property = itemName,
                          direction = axis1, 
                          bin_count = counts,
                          reduction_operation = RealOperation,
                          first_derivative = isDeriv))
  
  # 开始计算并获取结果
  data = pipeline.compute()
  result = data.tables['binning'].xy()      # 这里返回的应该是一个Nx2的numpy的矩阵, N为原子数量

  # 将结果输出为文件
  np.savetxt(outputName, result)

  # 如果用户要求将计算获得的numpy输出
  if isReturn:
    return result
  
def Bin_2d(fileName, outputName, itemName, axis, counts, 
           operation="mean"):
  '''
  此函数用于将导入的原子模型在一维方向上进行切割, 并计算对应的property, 然后将结果输出, 各输入参数意义如下
  fileName  : 字符串类型, 模型文件的名称
  outputName: 字符串类型, 输出的结果文件的名称
  itemName  : 字符串类型, 需要在某一个方向上进行平均的propertyname, 对应dump文件中ITEMS那一行的输出
  axis      : 字符串类型, 在哪个轴上面进行切割, 可以选择的方向有xy, xz, yz
  counts    : 元组类型, 含有2个整数在对应的轴上面共切割几份
  operation : 字符串类型, 默认为mean, 意思是将chunk内部的所有原子的property加起来再除以chunk中原子数量
  '''
  # 首先检查文件是否存在
  if not os.path.exists(fileName):
    raise FileNotFoundError("The file " + fileName + " does not exist.")
  
  # 然后检查传入的counts是否是元组, 以及这个元组里面是否有2个元素
  if not isinstance(counts, tuple) or len(counts) != 2:
    raise TypeError("The type of variable counts must be a tuple contains 2 integer.")
  else: # 如果传入的是元组, 那么我们接着判断元组里面的2个整数是否大于等于0
    if counts[0] < 1 or counts[1] < 1:
      raise ValueError("The value of counts must be greater than 1 both.")
    
  # 然后我们判断传入的切割方向是否是字符串变量
  if not isinstance(axis, str):
    raise TypeError("The type of variable counts must be string.")
  
  # 根据用户传入的axis选择方向, python中没有提供Switch语法, 故使用字典代替
  axis_dict={
    'xy': SBM.Direction.XY,
    'yx': SBM.Direction.XY,
    'xz': SBM.Direction.XZ,
    'zx': SBM.Direction.XZ,
    'yz': SBM.Direction.YZ,
    'zy': SBM.Direction.YZ
  }

  # 根据传入的key值, 也就是axis变量的值返回对应结果, 如果在字典里面没有找到对应对象, 那么返回一个0
  axis1 = axis_dict.get(axis.lower(), 0)   

  # 如果发现返回值为0, 就给出报错, 并终止程序
  if axis1 == 0: 
    raise ValueError("The value of variable 'axis' is inappropriate.")
  
  # 判断是否传入了operation
  if (operation != "mean"):   # 如果发现传入的operation不是默认的mean, 进行一系列的检测

    # 按照和上述的axis一样的做法, 同样定义一个字典来检测operation的输入, 但是先检测传入的operation是否是字符串类型
    if not isinstance(operation, str):
      raise TypeError("The type of variable 'operation' must be string.")
    
    # 接着检查传入的字符串是否全部都是英文
    if not operation.isalpha():
      raise ValueError("The content of variable 'operation' must be Alphabet.")
    
    # 运行到此, operation变量应该是没错了, 然后我们利用和上述axis一样的做法, 设置一个字典实现Switch的功能
    tmp_operation = operation.lower()   # 设置一个临时变量, 将字符串全部转成小写
    operation_dict={
      "mean": SBM.Operation.Mean,
      "min": SBM.Operation.Min,
      "max": SBM.Operation.Max,
      "sum": SBM.Operation.Sum,
      "sumvol": SBM.Operation.SumVol
    }

    # 根据传入的操作选择对应的操作
    RealOperation = operation_dict.get(tmp_operation, 0)

    if (RealOperation == 0):    # 如果在字典里面没有找到对应的键值, 给出报错并终止程序
      raise TypeError("The value of variable 'Operation' is inappropriate.")
  else:   # 如果用户没有定义operation, 那么默认使用mean手段
    RealOperation = SBM.Operation.Mean

  # 至此, 对所有传入参数的检查以及处理全部完成, 可以开始正式调用OVITO进行数据处理计算

  # 将模型导入计算空间
  pipeline = import_file(fileName)
  
  # 获取当前模型里面具体有哪些property
  itemList = list(pipeline.compute().particles.keys())

  # 检查传入的itemName是否在这个列表里面
  if not itemName in itemList:
    raise ValueError("The property " + itemName + " not seen in file " + fileName + ".")
  
  # 如果程序运行到此处还没有报错, 那么说明数据输入没有问题, 那么我们将调用OVITO进行计算
  pipeline.modifiers.append(SBM(
                          property = itemName,
                          direction = axis1, 
                          bin_count = counts,
                          reduction_operation = RealOperation))
  
  # 开始计算并获取结果, 二维及二维以上的维数返回的是一个VoxelGrid类, 不会返回一个矩阵
  pipeline.compute()

  # 将结果输出到VTK格式的文件中
  export_file(pipeline, outputName, 'vtk/grid', key='binning')

def Bin_3d(fileName, outputName, itemName, counts, 
           operation="mean"):
  '''
  此函数用于将导入的原子模型在三维方向上进行切割, 并计算对应的property, 然后将结果输出, 各输入参数意义如下
  fileName  : 字符串类型, 模型文件的名称
  outputName: 字符串类型, 输出的结果文件的名称
  itemName  : 字符串类型, 需要在某一个方向上进行平均的propertyname, 对应dump文件中ITEMS那一行的输出
  counts    : 元组类型, 含有3个整数在对应的xyz轴上面共切割几份
  operation : 字符串类型, 默认为mean, 意思是将chunk内部的所有原子的property加起来再除以chunk中原子数量
  '''
  # 首先检查文件是否存在
  if not os.path.exists(fileName):
    raise FileNotFoundError("The file " + fileName + " does not exist.")
  
  # 然后检查传入的counts是否是元组, 以及这个元组里面是否有3个元素
  if not isinstance(counts, tuple) or len(counts) != 3:
    raise TypeError("The type of variable counts must be a tuple contains 2 integer.")
  else: # 如果传入的是元组, 那么我们接着判断元组里面的3个整数是否大于等于0
    if counts[0] < 1 or counts[1] < 1 or counts[2] < 1:
      raise ValueError("The value of counts must be greater than 1 both.")
  
  # 判断是否传入了operation
  if (operation != "mean"):   # 如果发现传入的operation不是默认的mean, 进行一系列的检测

    # 按照和上述的axis一样的做法, 同样定义一个字典来检测operation的输入, 但是先检测传入的operation是否是字符串类型
    if not isinstance(operation, str):
      raise TypeError("The type of variable 'operation' must be string.")
    
    # 接着检查传入的字符串是否全部都是英文
    if not operation.isalpha():
      raise ValueError("The content of variable 'operation' must be Alphabet.")
    
    # 运行到此, operation变量应该是没错了, 然后我们利用和上述axis一样的做法, 设置一个字典实现Switch的功能
    tmp_operation = operation.lower()   # 设置一个临时变量, 将字符串全部转成小写
    operation_dict={
      "mean": SBM.Operation.Mean,
      "min": SBM.Operation.Min,
      "max": SBM.Operation.Max,
      "sum": SBM.Operation.Sum,
      "sumvol": SBM.Operation.SumVol
    }

    # 根据传入的操作选择对应的操作
    RealOperation = operation_dict.get(tmp_operation, 0)

    if (RealOperation == 0):    # 如果在字典里面没有找到对应的键值, 给出报错并终止程序
      raise TypeError("The value of variable 'Operation' is inappropriate.")
  else:   # 如果用户没有定义operation, 那么默认使用mean手段
    RealOperation = SBM.Operation.Mean

  # 至此, 对所有传入参数的检查以及处理全部完成, 可以开始正式调用OVITO进行数据处理计算

  # 将模型导入计算空间
  pipeline = import_file(fileName)
  
  # 获取当前模型里面具体有哪些property
  itemList = list(pipeline.compute().particles.keys())

  # 检查传入的itemName是否在这个列表里面
  if not itemName in itemList:
    raise ValueError("The property " + itemName + " not seen in file " + fileName + ".")
  
  # 如果程序运行到此处还没有报错, 那么说明数据输入没有问题, 那么我们将调用OVITO进行计算
  pipeline.modifiers.append(SBM(
                          property = itemName,
                          direction = SBM.Direction.XYZ, 
                          bin_count = counts,
                          reduction_operation = RealOperation))
  
  # 开始计算并获取结果, 二维及二维以上的维数返回的是一个VoxelGrid类, 不会返回一个矩阵
  pipeline.compute()

  # 将结果输出到VTK格式的文件中
  export_file(pipeline, outputName, 'vtk/grid', key='binning')

def density_2d(fileName, outputName, counts, axis,
           operation="sumvol"):
  '''
  此函数用于计算导出绘制原子模型的二维密度云图, 以下是各参数的具体意义:
  fileName  : 字符串类型, 模型文件的名称
  outputName: 字符串类型, 输出的结果文件的名称
  axis      : 字符串类型, 在哪个轴上面进行切割, 可以选择的方向有xy, xz, yz
  counts    : 元组类型, 含有2个整数在对应的xyz轴上面共切割几份
  operation : 字符串类型, 默认为sumvol, 意思是平均数密度, 即用原子数除以chunk体积
  '''
   # 首先检查文件是否存在
  if not os.path.exists(fileName):
    raise FileNotFoundError("The file " + fileName + " does not exist.")
  
  # 然后检查传入的counts是否是元组, 以及这个元组里面是否有2个元素
  if not isinstance(counts, tuple) or len(counts) != 2:
    raise TypeError("The type of variable counts must be a tuple contains 2 integer.")
  else: # 如果传入的是元组, 那么我们接着判断元组里面的2个整数是否大于等于0
    if counts[0] < 1 or counts[1] < 1:
      raise ValueError("The value of counts must be greater than 1 both.")
    
  # 然后我们判断传入的切割方向是否是字符串变量
  if not isinstance(axis, str):
    raise TypeError("The type of variable counts must be string.")
  
  # 根据用户传入的axis选择方向, python中没有提供Switch语法, 故使用字典代替
  axis_dict={
    'xy': SBM.Direction.XY,
    'yx': SBM.Direction.XY,
    'xz': SBM.Direction.XZ,
    'zx': SBM.Direction.XZ,
    'yz': SBM.Direction.YZ,
    'zy': SBM.Direction.YZ
  }

  # 根据传入的key值, 也就是axis变量的值返回对应结果, 如果在字典里面没有找到对应对象, 那么返回一个0
  axis1 = axis_dict.get(axis.lower(), 0)   

  # 如果发现返回值为0, 就给出报错, 并终止程序
  if axis1 == 0: 
    raise ValueError("The value of variable 'axis' is inappropriate.")
  
  # 判断是否传入了operation
  if (operation != "mean"):   # 如果发现传入的operation不是默认的mean, 进行一系列的检测

    # 按照和上述的axis一样的做法, 同样定义一个字典来检测operation的输入, 但是先检测传入的operation是否是字符串类型
    if not isinstance(operation, str):
      raise TypeError("The type of variable 'operation' must be string.")
    
    # 接着检查传入的字符串是否全部都是英文
    if not operation.isalpha():
      raise ValueError("The content of variable 'operation' must be Alphabet.")
    
    # 运行到此, operation变量应该是没错了, 然后我们利用和上述axis一样的做法, 设置一个字典实现Switch的功能
    tmp_operation = operation.lower()   # 设置一个临时变量, 将字符串全部转成小写
    operation_dict={
      "mean": SBM.Operation.Mean,
      "min": SBM.Operation.Min,
      "max": SBM.Operation.Max,
      "sum": SBM.Operation.Sum,
      "sumvol": SBM.Operation.SumVol
    }

    # 根据传入的操作选择对应的操作
    RealOperation = operation_dict.get(tmp_operation, 0)

    if (RealOperation == 0):    # 如果在字典里面没有找到对应的键值, 给出报错并终止程序
      raise TypeError("The value of variable 'Operation' is inappropriate.")
  else:   # 如果用户没有定义operation, 那么默认使用mean手段
    RealOperation = SBM.Operation.Mean
  
  # 至此, 对所有传入参数的检查以及处理全部完成, 可以开始正式调用OVITO进行数据处理计算

  # 将模型导入计算空间
  pipeline = import_file(fileName)

  # 调用compute property计算原子的密度
  pipeline.modifiers.append(CPM(expressions=['1'], output_property='Unity'))

  # 调用SpatialBinningModifier
  pipeline.modifiers.append(SBM(
    property = 'Unity',
    direction = axis1, 
    bin_count = counts,
    reduction_operation = RealOperation
  ))

  # 计算获取数据
  pipeline.compute()

  # 导出数据
  export_file(pipeline, outputName, 'vtk/grid', key='binning')

def density_3d(fileName, outputName, counts,
           operation="sumvol"):
  '''
  此函数用于计算导出绘制原子模型的三维密度云图, 以下是各参数的具体意义:
  fileName  : 字符串类型, 模型文件的名称
  outputName: 字符串类型, 输出的结果文件的名称
  counts    : 元组类型, 含有3个整数在对应的xyz轴上面共切割几份
  operation : 字符串类型, 默认为sumvol, 意思是平均数密度, 即用原子数除以chunk体积
  '''
   # 首先检查文件是否存在
  if not os.path.exists(fileName):
    raise FileNotFoundError("The file " + fileName + " does not exist.")
  
  # 然后检查传入的counts是否是元组, 以及这个元组里面是否有3个元素
  if not isinstance(counts, tuple) or len(counts) != 3:
    raise TypeError("The type of variable counts must be a tuple contains 3 integer.")
  else: # 如果传入的是元组, 那么我们接着判断元组里面的2个整数是否大于等于0
    if counts[0] < 1 or counts[1] < 1 or counts[2] < 1:
      raise ValueError("The value of counts must be greater than 1 both.")
  
  # 判断是否传入了operation
  if (operation != "mean"):   # 如果发现传入的operation不是默认的mean, 进行一系列的检测

    # 按照和上述的axis一样的做法, 同样定义一个字典来检测operation的输入, 但是先检测传入的operation是否是字符串类型
    if not isinstance(operation, str):
      raise TypeError("The type of variable 'operation' must be string.")
    
    # 接着检查传入的字符串是否全部都是英文
    if not operation.isalpha():
      raise ValueError("The content of variable 'operation' must be Alphabet.")
    
    # 运行到此, operation变量应该是没错了, 然后我们利用和上述axis一样的做法, 设置一个字典实现Switch的功能
    tmp_operation = operation.lower()   # 设置一个临时变量, 将字符串全部转成小写
    operation_dict={
      "mean": SBM.Operation.Mean,
      "min": SBM.Operation.Min,
      "max": SBM.Operation.Max,
      "sum": SBM.Operation.Sum,
      "sumvol": SBM.Operation.SumVol
    }

    # 根据传入的操作选择对应的操作
    RealOperation = operation_dict.get(tmp_operation, 0)

    if (RealOperation == 0):    # 如果在字典里面没有找到对应的键值, 给出报错并终止程序
      raise TypeError("The value of variable 'Operation' is inappropriate.")
  else:   # 如果用户没有定义operation, 那么默认使用mean手段
    RealOperation = SBM.Operation.Mean
  
  # 至此, 对所有传入参数的检查以及处理全部完成, 可以开始正式调用OVITO进行数据处理计算

  # 将模型导入计算空间
  pipeline = import_file(fileName)

  # 调用compute property计算原子的密度, 这里的意思是给每个原子赋予一个为1的值
  pipeline.modifiers.append(CPM(expressions=['1'], output_property='Unity'))

  # 调用SpatialBinningModifier
  pipeline.modifiers.append(SBM(
    property = 'Unity',
    direction = SBM.Direction.XYZ, 
    bin_count = counts,
    reduction_operation = RealOperation
  ))

  # 计算获取数据
  pipeline.compute()

  # 导出数据
  export_file(pipeline, outputName, 'vtk/grid', key='binning')


