from vtkmodules.vtkCommonCore import (
    vtkObject,
    vtkPoints,
    vtkUnsignedCharArray
)
from vtkmodules.vtkCommonDataModel import (
    vtkCell,
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleMultiTouchCamera
import vtkmodules.vtkRenderingOpenGL2
import numpy as np
import vtk


def actor_mesh(filename):
    if filename.lower().endswith(".stl"):
        reader = vtk.vtkSTLReader()
    elif filename.lower().endswith(".ply"):
        reader = vtk.vtkPLYReader()
    elif filename.lower().endswith(".vtk"):
        reader = vtk.vtkStructuredPointsReader()
        reader.ReadAllVectorsOn()
        reader.ReadAllScalarsOn()
    else:
        raise ValueError("Only reads STL and PLY")
    reader.SetFileName(filename)
    reader.Update()
    mapper = vtkPolyDataMapper()
    mapper.SetInputData(reader.GetOutput())
    actor = vtkActor()
    actor.SetMapper(mapper)
    return actor


def actor_ply(ply_file):
    points = vtkPoints()
    cells = vtkCellArray()

    file = open(ply_file, 'r')
    lines = file.readlines()
    start_extract = False
    for line in lines:
        if start_extract:
            arr = np.fromstring(line, dtype=float, sep=' ')
            id = points.InsertNextPoint(arr)
            cells.InsertNextCell(1)
            cells.InsertCellPoint(id)
        if line.find('end_header') == 0:
            start_extract = True
        
    polydata = vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetVerts(cells)
    mapper = vtkPolyDataMapper()
    mapper.SetInputData(polydata)
    actor = vtkActor()
    actor.SetMapper(mapper)
    return actor


def actor_plf_color(ply_file):
    points = vtkPoints()
    cells = vtkCellArray()
    colors = vtkUnsignedCharArray()
    colors.SetNumberOfComponents(3)

    file = open(ply_file, 'r')
    lines = file.readlines()
    start_extract = False
    for line in lines:
        if start_extract:
            arr = np.fromstring(line, dtype=float, sep=' ')
            id = points.InsertNextPoint(arr[0:3])
            cells.InsertNextCell(1)
            cells.InsertCellPoint(id)
            colors.InsertNextTuple(arr[3:6])
        if line.find('end_header') == 0:
            start_extract = True
        
    polydata = vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetVerts(cells)
    polydata.GetCellData().SetScalars(colors)
    mapper = vtkPolyDataMapper()
    mapper.SetInputData(polydata)
    actor = vtkActor()
    actor.SetMapper(mapper)
    return actor


def show_actor(actorlist):
    # render
    render = vtkRenderer()
    render.SetBackground(0, 0, 0)

    # Renderer Window
    window = vtkRenderWindow()
    window.AddRenderer(render)
    # window.SetSize(1200, 1200)

    # System Event
    win_render = vtkRenderWindowInteractor()
    win_render.SetRenderWindow(window)

    # Style
    win_render.SetInteractorStyle(vtkInteractorStyleMultiTouchCamera())

    # Insert Actor
    for actor in actorlist:
        render.AddActor(actor)
    win_render.Initialize()
    win_render.Start()


if __name__ == '__main__':
    # 读取 txt 文档
    file_path1 = R"pointcloud/pcdata/DepthPoints.ply"
    file_color = R"pointcloud/pcdata/RGBPoints.ply"
    file_stl = R"pointcloud/pcdata/noflyzone.stl"
    actor = actor_ply(file_path1)
    # actor_color = actor_plf_color(file_color)
    actor_color = actor_mesh(file_color)
    actor_stl = actor_mesh(file_stl)
    # actor.GetProperty().SetColor(1, 0, 0)
    show_actor([actor_stl])
    
