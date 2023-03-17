#! /usr/bin/env python3

#  Copyright (c) Thiago Franco de Moraes
#
#  This source code is licensed under the MIT license found in the
#  LICENSE file in the root directory of this source tree.

import math
import sys

import vtk


def read_mesh_file(filename):
    if filename.lower().endswith(".stl"):
        reader = vtk.vtkSTLReader()
    elif filename.lower().endswith(".ply"):
        reader = vtk.vtkPLYReader()
    elif filename.lower().endswith(".vtk"):
        # reader = vtk.vtkStructuredPointsReader()
        # reader.ReadAllVectorsOn()
        # reader.ReadAllScalarsOn()
        reader = vtk.vtkGenericDataObjectReader()
    else:
        raise ValueError("Only reads STL and PLY")
    reader.SetFileName(filename)
    reader.Update()
    return reader.GetOutput()


def polydata_2_imagedata(polydata, spacing, padding=1):
    bounds = polydata.GetBounds()
    print('bounds: ', bounds)

    # spacing = [10, 10, 10]
    dim = [0, 0, 0]
    for index in range(3):
        dim[index] = math.ceil((bounds[index*2 + 1] - bounds[index*2])/spacing[index])
    
    origin = [0, 0, 0]
    origin[0] = bounds[0] + spacing[0] / 2
    origin[1] = bounds[2] + spacing[1] / 2
    origin[2] = bounds[4] + spacing[2] / 2
    if padding:
        origin[0] -= spacing[0]
        origin[1] -= spacing[1]
        origin[2] -= spacing[2]

        dim[0] += 2 * padding
        dim[1] += 2 * padding
        dim[2] += 2 * padding

    print('dim: ', dim)
    print('origin: ', origin)

    image = vtk.vtkImageData()
    image.SetSpacing(spacing)
    image.SetDimensions(dim)
    image.SetExtent(0, dim[0] - 1, 0, dim[1] - 1, 0, dim[2] - 1)
    image.SetOrigin(origin)
    image.AllocateScalars(vtk.VTK_UNSIGNED_CHAR, 1)

    inval = 255
    outval = 0
    numpoints = image.GetNumberOfPoints()
    print('number points: ', numpoints)
    for i in range(numpoints):
        image.GetPointData().GetScalars().SetTuple1(i, inval)

    pol2stenc = vtk.vtkPolyDataToImageStencil()
    pol2stenc.SetInputData(polydata)
    pol2stenc.SetOutputOrigin(origin)
    pol2stenc.SetOutputSpacing(spacing)
    pol2stenc.SetOutputWholeExtent(image.GetExtent())
    pol2stenc.Update()

    imgstenc = vtk.vtkImageStencil()
    imgstenc.SetInputData(image)
    imgstenc.SetStencilConnection(pol2stenc.GetOutputPort())
    imgstenc.ReverseStencilOff()
    imgstenc.SetBackgroundValue(outval)
    imgstenc.Update()

    return imgstenc.GetOutput()



def polydata_to_imagedata(polydata, dimensions=(100, 100, 100), padding=1):
    xi, xf, yi, yf, zi, zf = polydata.GetBounds()
    dx, dy, dz = dimensions
    print('bounds: ', polydata.GetBounds())

    # Calculating spacing
    sx = (xf - xi) / dx
    sy = (yf - yi) / dy
    sz = (zf - zi) / dz
    print('spacing: %6.3f, %6.3f, %6.3f' % (sx, sy, sz))
    # Calculating Origin
    ox = xi + sx / 2.0
    oy = yi + sy / 2.0
    oz = zi + sz / 2.0    

    if padding:
        ox -= sx
        oy -= sy
        oz -= sz

        dx += 2 * padding
        dy += 2 * padding
        dz += 2 * padding

    print('origin: %6.3f, %6.3f, %6.3f'% (ox, oy, oz))
    print('dims: %d, %d, %d'% (dx, dy, dz))

    image = vtk.vtkImageData()
    image.SetSpacing((sx, sy, sz))
    image.SetDimensions((dx, dy, dz))
    image.SetExtent(0, dx - 1, 0, dy - 1, 0, dz - 1)
    image.SetOrigin((ox, oy, oz))
    image.AllocateScalars(vtk.VTK_UNSIGNED_CHAR, 1)

    inval = 255
    outval = 0

    for i in range(image.GetNumberOfPoints()):
        image.GetPointData().GetScalars().SetTuple1(i, inval)

    pol2stenc = vtk.vtkPolyDataToImageStencil()
    pol2stenc.SetInputData(polydata)
    pol2stenc.SetOutputOrigin((ox, oy, oz))
    pol2stenc.SetOutputSpacing((sx, sy, sz))
    pol2stenc.SetOutputWholeExtent(image.GetExtent())
    pol2stenc.Update()

    imgstenc = vtk.vtkImageStencil()
    imgstenc.SetInputData(image)
    imgstenc.SetStencilConnection(pol2stenc.GetOutputPort())
    imgstenc.ReverseStencilOff()
    imgstenc.SetBackgroundValue(outval)
    imgstenc.Update()

    return imgstenc.GetOutput()


def save(imagedata, filename):
    bounds = imagedata.GetBounds()
    origin = imagedata.GetOrigin()
    dims = imagedata.GetDimensions()
    print('output bounds: ', bounds)
    print('output origin: ', origin)
    print('output dims: ', dims)
    writer = vtk.vtkXMLImageDataWriter()
    writer.SetFileName(filename)
    writer.SetInputData(imagedata)
    writer.Write()


def savemetadata(imagedata, filename):
    writer = vtk.vtkMetaImageWriter()
    writer.SetFileName(filename + ".mhd")
    writer.SetRAWFileName(filename + ".raw")
    writer.SetInputData(imagedata)
    writer.Write()


def main():
    # input_filename = sys.argv[1]
    # output_filename = sys.argv[2]
    input_filename = R"data/screw.stl"
    output_filename = R"mesh.mhd"

    polydata = read_mesh_file(input_filename)
    spacing = [0.2, 0.2, 0.2]
    imagedata = polydata_2_imagedata(polydata, spacing)
    # imagedata = polydata_to_imagedata(polydata)
    # save(imagedata, output_filename)
    savemetadata(imagedata, "data/screw")


if __name__ == "__main__":
    main()