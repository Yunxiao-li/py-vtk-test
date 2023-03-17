import vtk

import vtkmodules.vtkRenderingOpenGL2
import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingFreeType

reader = vtk.vtkMetaImageReader()
# reader.SetFileName(R"/home/jackie/works/code/repo/misc/python/py-vtk-test/test/mesh.vti")
reader.SetFileName("mesh.mhd")
reader.Update()
image = reader.GetOutput()

image_actor = vtk.vtkImageActor()
# image_actor.SetInputData(image)
image_actor.GetMapper().SetInputConnection(reader.GetOutputPort())
bounds = image_actor.GetBounds()
image_actor.SetPosition(50,50,100)

render = vtk.vtkRenderer()
render.AddActor(image_actor)

window = vtk.vtkRenderWindow()
window.AddRenderer(render)

interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(window)

style = vtk.vtkInteractorStyleImage()
interactor.SetInteractorStyle(style)

interactor.Initialize()
interactor.Start()

