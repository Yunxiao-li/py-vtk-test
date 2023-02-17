import numpy
import vtk
from vtk.util.numpy_support import numpy_to_vtk

from vtkmodules.vtkCommonCore import vtkObject
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import vtkRenderWindow


def data_actor(source_data):
    # 新建 vtkPoints 实例
    points = vtk.vtkPoints()
    # 导入点数据
    points.SetData(numpy_to_vtk(source_data))
    # 新建 vtkPolyData 实例
    polydata = vtk.vtkPolyData()
    # 设置点坐标
    polydata.SetPoints(points)
    
    # 顶点相关的 filter
    vertex = vtk.vtkVertexGlyphFilter()
    vertex.SetInputData(polydata)

    # mapper 实例
    mapper = vtk.vtkPolyDataMapper()
    # 关联 filter 输出
    mapper.SetInputConnection(vertex.GetOutputPort())

    # actor 实例
    actor = vtk.vtkActor()
    # 关联 mapper
    actor.SetMapper(mapper)

    # 红色点显示
    # actor.GetProperty().SetColor(1,0,0)
    return actor


def show_actor(actorlist):
    # render
    render = vtk.vtkRenderer()
    render.SetBackground(0, 0, 0)

    # Renderer Window
    window = vtk.vtkRenderWindow()
    window.AddRenderer(render)
    window.SetSize(1200, 1200)

    # System Event
    win_render = vtk.vtkRenderWindowInteractor()
    win_render.SetRenderWindow(window)

    # Style
    win_render.SetInteractorStyle(vtk.vtkInteractorStyleMultiTouchCamera())

    # Insert Actor
    for actor in actorlist:
        render.AddActor(actor)
    win_render.Initialize()
    win_render.Start()


if __name__ == '__main__':
    # 读取 txt 文档
    file_path1 = R"pointcloud/pcdata/DepthPoints.txt"
    file_path2 = R"pointcloud/pcdata/bun180.txt"

    source_data1 = numpy.loadtxt(file_path1)
    source_data2 = numpy.loadtxt(file_path2)
    actor1 = data_actor(source_data1)
    actor2 = data_actor(source_data2)
    actor2.GetProperty().SetColor(1, 0, 0)
    actorlist = [actor1, actor2]
    show_actor(actorlist)
