from vtkmodules.all import *
for c in vtkFillHolesFilter, vtkCell, vtkPolyData, vtkPolyDataMapper:
    print(f"from {c.__module__} import {c.__name__}")