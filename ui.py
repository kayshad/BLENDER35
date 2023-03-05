import bpy
import numpy



class OBJECT_OT_kays_operator_surface(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.kays_operator_surface"
    bl_label = "Kays Operator Surface"
    bl_options = {'REGISTER', 'UNDO'}
    


    def execute(self, context):
        import sympy as sym
        x, y, z, t = sym.symbols('x y z t')
        k, m, n = sym.symbols('k m n', integer=True)
        f, g, h = sym.symbols('f g h', cls= sym.Function)
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
            
        surf(sym.parse_expr(context.scene.Eq_Surface), 'surface', 50, 10)
        return {'FINISHED'}

class OBJECT_OT_kays_operator_curve(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.kays_operator_curve"
    bl_label = "Kays Operator Curve"
    bl_options = {'REGISTER', 'UNDO'}
    


    def execute(self, context):
        
        donne = context.scene.Eq_Curve
        
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
        
        layout = self.layout
        row = layout.row()
        row.prop(context.scene, "Eq_Curve")
        row.prop(context.scene, "Eq_Surface")
        
        
        # props = self.layout.operator('object.kays_operator_curve')
        # props = self.layout.operator('object.kays_operator_surface')

def update_funcc(self, context):
    bpy.ops.object.kays_operator_curve()
    
def update_funcs(self, context):
    bpy.ops.object.kays_operator_surface()


# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    bpy.utils.register_class(OBJECT_OT_kays_operator_surface)
    bpy.utils.register_class(OBJECT_OT_kays_operator_curve)
    bpy.utils.register_class(OBJECT_PT_kays_panel)
    bpy.types.Scene.Eq_Curve =  bpy.props.StringProperty(name = "Equation Courbe", default = "x", update=update_funcc)
    bpy.types.Scene.Eq_Surface =  bpy.props.StringProperty(name = "Equation Surface", default = "sin(x) + cos(y)", update=update_funcs)



def unregister():
    bpy.utils.unregister_class(OBJECT_OT_kays_operator_curve)
    bpy.utils.unregister_class(OBJECT_OT_kays_operator_surface)
    bpy.utils.unregister_class(OBJECT_OT_kays_operators)
    del bpy.types.Scene.Eq_Curve
    del bpy.types.Scene.Eq_Surface



if __name__ == "__main__":
    register()
