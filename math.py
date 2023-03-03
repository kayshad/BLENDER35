import mathutils
from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty)
import numpy
from sympy import *
import bpy
import utils

bl_info = {
    "name": "MathAddon",
    "author": "Kays",
    "blender": (3, 5, 0),
    "category": "Object",
}


x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer=True)
f, g, h = symbols('f g h', cls=Function)



def update_foncc(self, context):
    x, y, z = symbols("x y z")
    Eqc = self.Eqc
    if Eqc:
        try:
            for obj in bpy.data.objects:      
                if 'fonction' in obj.name:
                    bpy.data.objects.remove(obj)
            for coll in bpy.data.collections:      
                if 'Fonction' in coll.name:
                    bpy.data.collections.remove(coll) 
            coll = bpy.data.collections.new('Fonction')
            bpy.context.scene.collection.children.link(coll)                   
            bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)       
            name = 'fonction'
            curveData = bpy.data.curves.new(name, type='CURVE')
            curveData.dimensions = '3D'
            curveData.resolution_u = 2
            curveData.bevel_depth = 0.01
            curveOB = bpy.data.objects.new(name, curveData)
            #bpy.context.collection.objects.link(curveOB)
            coll.objects.link(curveOB)
            n = 100
            yVals = []
            xVals = numpy.linspace(-5,5,n)
            zoom = 1
            exp = parse_expr(Eqc)
            for xv in xVals:
                yVals.append((zoom*xv,0.0,zoom*exp.subs(x,xv),1))
            bpy.data.curves[name].splines.new('POLY')
            p = bpy.data.curves[name].splines[0].points
            p.add(len(yVals)-1)
            for i, coord in enumerate(yVals):
                p[i].co = coord
        except:
            import traceback
            print("", traceback.format_exc(limit=1))
    else:
        print("Aucune expression donnée")
        
        
def surf(expr, name, div, t):
    verts = []
    faces  = []
    scale = 1
    for obj in bpy.data.objects:      
        if 'surface' in obj.name:
            bpy.data.objects.remove(obj)
    for coll in bpy.data.collections:      
        if 'Surface' in coll.name:
            bpy.data.collections.remove(coll) 
    coll = bpy.data.collections.new('Surface')
    bpy.context.scene.collection.children.link(coll)
    expr = expr
    name = name
    lin = numpy.linspace(-1*t, t, num=div)
    verts = [(scale * i, scale * j, scale*(expr.subs({x:i, y:j}))) for i in lin for j in lin] 
    count = 0
    for i in range (0, lin.size *(lin.size-1)):
        if count < lin.size-1:
            A = i
            B = i+1
            C = (i+lin.size)+1
            D = (i+lin.size)
            face = (A,B,C,D)
            faces.append(face)
            count = count + 1
        else:
            count = 0    
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update(calc_edges=True)
    for f in mesh.polygons:
        f.use_smooth = True
    obj = bpy.data.objects.new(name, mesh)
    coll.objects.link(obj)
        
def update_foncs(self,context):
    surf(parse_expr(context.scene.mes_props.Eqs), 'surface', 50, 10)

class MesProps(bpy.types.PropertyGroup):
    Eqc: bpy.props.StringProperty(name="Equation courbe 3D", description="Equation  y=f(x)", default="x", update=update_foncc)
    Eqs: bpy.props.StringProperty(name ="Equation Surface 3D", description="Equation  z=f(x,y)", default='sin(x)+cos(y)' , update=update_foncs)
    #extmax: bpy.props.IntProperty(name ="MaX", default= 5 , update=update_fonc)
    #extmin: bpy.props.IntProperty(name ="MiN", default=-5 , update=update_fonc)


class OBJECT_OT_simple_operator(bpy.types.Operator):
    """Tooltip"""
    bl_label = "STOCKAGEFONCTION"
    bl_idname = "object.simple_operator"
    def execute(self, context):
        for obj in bpy.data.objects:      
            if 'fonction' in obj.name:
                obj.name = 'stockf'
        for coll in bpy.data.collections:      
            if 'Fonction' in coll.name:
                coll.name = 'Stockf'
        
        return {'FINISHED'}


class OBJECT_PT_property_example(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Mon Pano Mathematique"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "MATH"

    def draw(self, context):
        donne = context.scene.mes_props
        layout = self.layout
        row = layout.row()
        row.label(text="Courbe3D", icon='WORLD_DATA')
        row = layout.row()
        moneqc = row.prop(context.scene.mes_props, "Eqc")
        moneqs = row.prop(context.scene.mes_props, "Eqs")
        row = layout.row()
        
        #m0prop = self.layout.prop(donne, "extmin")
        #m1prop = self.layout.prop(donne, "extmax")
        monop = row.operator("object.simple_operator")



classes = [MesProps, OBJECT_OT_simple_operator, OBJECT_PT_property_example]
invclasses = [OBJECT_PT_property_example, OBJECT_OT_simple_operator, MesProps]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.mes_props = bpy.props.PointerProperty(type=MesProps)


def unregister():
    for cls in invclasses:
        bpy.utils.unregister_class(cls)
        #del bpy.types.Scene.mes_props


if __name__ == "__main__":
    register()