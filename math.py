from __future__ import division
from sympy import *
x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer=True)
f, g, h = symbols('f g h', cls=Function)
init_printing()



import bpy
import numpy

#from mathutils import Vector


def nettoi(name):
    collection = bpy.data.collections.get(name)
    if not collection is None :
        for obj in collection.objects:
            cu = obj.data  # the curve
            bpy.data.curves.remove(cu)
           # bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(collection)

def nettoim(name):
    collection = bpy.data.collections.get(name)
    if not collection is None :
        for obj in collection.objects:
            data = obj.data  # the curve
            bpy.data.meshes.remove(data)
           # bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(collection)





def surf(expr, name, div, t):
    verts = []
    edges = []
    faces  = []


    nettoim('Grid')
    coll = bpy.data.collections.new('Grid')
    bpy.context.scene.collection.children.link(coll)
    expr = expr
    name = name
    div = div
    rge = int(t*1/div) #*2
    rgf = rge*2
    rgfd = rgf+1
    verts.extend([(i*div, j*div, expr.subs({x:i, y: j})) for i in range(-rge,rge+1) for j in range(-rge,rge+1)])
    faces.extend([i+(j*rgfd),(i+(j*rgfd)+rgfd),(i+(j*rgfd)+rgfd+1),(i+(j*rgfd)+1)] for i in range(rgf) for j in range(rgf))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update(calc_edges=True)
    for f in mesh.polygons:
        f.use_smooth = True
    obj = bpy.data.objects.new(name, mesh)
    obj.modifiers.new('My SubDiv', 'SUBSURF')
    coll.objects.link(obj)
    #bpy.context.scene.collection.objects.link(obj)

def cre(expr):
    nettoi('nbr')
    expr = expr
    coll = bpy.data.collections.new('nbr')
    bpy.context.scene.collection.children.link(coll)
    extmax = bpy.context.scene.my_prop_grp.extmax
    extmin = bpy.context.scene.my_prop_grp.extmin
    resol = (extmax-extmin)*10
    coords_list = numpy.linspace(extmin,extmax,resol)
    crv = bpy.data.curves.new('crv', 'CURVE')
    crv.dimensions = '3D'
    crv.bevel_depth = 0.02
    crv.use_fill_caps = True
    crv.splines.clear()
    spline = crv.splines.new(type='POLY')
    spline.points.add(len(coords_list)-1) # theres already one point by default
    # make a new object with the curve
    obj = bpy.data.objects.new('obj', crv)
    coll.objects.link(obj)
    #print(coords_list)
    for i, new_co in enumerate(coords_list):
        spline.points[i].co = (new_co,expr.subs(x,new_co),0,1.0) # (add nurbs weight)

def update_fonc(self,context):
    cre(parse_expr(context.scene.my_prop_grp.Eq))


def foncs(self,context):
    surf(parse_expr(context.scene.my_prop_grp.Eqs), 'Grid', 1, 10)

class MyPropertyGroup(bpy.types.PropertyGroup):
    Eq: bpy.props.StringProperty(name ="Equation Courbe", default='x' , update=update_fonc)
    Eqs: bpy.props.StringProperty(name ="Equation Surface", default='sin(x)+cos(y)' , update=foncs)
    extmax: bpy.props.IntProperty(name ="MaX", default= 5 , update=update_fonc)
    extmin: bpy.props.IntProperty(name ="MiN", default=-5 , update=update_fonc)


class MonPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Mon Panel"
    bl_idname = "MON_PT_hello"
    bl_space_type ='VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "MAthPano"
    def draw(self, context):
        donne = context.scene.my_prop_grp
        m0prop = self.layout.prop(donne, "extmin")
        m1prop = self.layout.prop(donne, "extmax")
        m2prop = self.layout.prop(donne, "Eq")
        m3prop = self.layout.prop(donne, "Eqs")

def register():

    bpy.utils.register_class(MonPanel)
    bpy.utils.register_class(MyPropertyGroup)
    bpy.types.Scene.my_prop_grp = bpy.props.PointerProperty(type=MyPropertyGroup)


def unregister():
    bpy.utils.unregister_class(HelloWorldPanel)
    bpy.utils.unregister_class(MyPropertyGroup)


register()
