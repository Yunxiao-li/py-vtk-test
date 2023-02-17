from vtkmodules.all import *
for c in vtkUnsignedCharArray, vtkCell, vtkPolyData, vtkPolyDataMapper:
    print(f"from {c.__module__} import {c.__name__}")