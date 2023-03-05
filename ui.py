import bpy
import numpy


class OBJECT_OT_kays_operator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.kays_operator"
    bl_label = "Kays Object Operator"
    bl_options = {'REGISTER', 'UNDO'}
    


    def execute(self, context):
        
        donne = context.scene.my_string
        
        self.report({'INFO'}, 'S: %r' %(donne))
        import sympy as sym
        x, y, z, t = sym.symbols('x y z t')
        k, m, n = sym.symbols('k m n', integer=True)
        f, g, h = sym.symbols('f g h', cls= sym.Function)
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
        coll.objects.link(curveOB)
        n = 100
        yVals = []
        xVals = numpy.linspace(-5,5,n)
        zoom = 1
        # parsing expression sympy
        exp = sym.parse_expr(donne)
        for xv in xVals:
            yVals.append((zoom*xv,0.0,zoom*exp.subs(x,xv),1))
        bpy.data.curves[name].splines.new('POLY')
        p = bpy.data.curves[name].splines[0].points
        p.add(len(yVals)-1)
        for i, coord in enumerate(yVals):
            p[i].co = coord
        return {'FINISHED'}

class OBJECT_PT_kays_panel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_kays_panel"
    bl_label = "Kays Example"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Kays Category"

    def draw(self, context):
        donne = context.scene
        
        layout = self.layout
        row = layout.row()
        row.prop(donne, "my_string")
        
        
        # props = self.layout.operator('object.kays_operator')

def update_func(self, context):
    bpy.ops.object.kays_operator()


bpy.types.Scene.testprop = bpy.props.FloatProperty(update=update_func)

# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    bpy.utils.register_class(OBJECT_OT_kays_operator)
    bpy.utils.register_class(OBJECT_PT_kays_panel)
    bpy.types.Scene.my_string =  bpy.props.StringProperty(name = "Equation Courbe", default = "x", update=update_func)



def unregister():
    bpy.utils.unregister_class(OBJECT_PT_kays_panel)
    bpy.utils.unregister_class(OBJECT_OT_kays_operator)
    del bpy.types.Scene.my_string



if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.object.simple_operator()
