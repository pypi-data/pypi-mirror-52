# gdmTools 
### A dataset tool for converting all images in a folder into neural network recognition

<hr>

## This tool includes a total of three methods
### 1. Convert images to data using the image method of the PIL package
### 2. Read the file directory and return the data set
### 3. Slices of known global datasets and return them as training sets, test sets, validation sets

### example:
```
  data = read(input_Path)
  train_index, test_index, valid_index = cut(data, 0.5, 0.2, 0.3)
  # x
  data[train_index], data[test_index], data[valid_index] 
  # y
  label
```
<hr>

## GDM is a graphical data modeling product developed by the cosmosource. The main functions are graphical development of machine learning tasks with Spark as the engine, and graphical development of deep learning tasks with Tensorflow as the engine.


