import bpy




def arbregeon_node_group(n):
    arbregeon= bpy.data.node_groups.new(type = "GeometryNodeTree", name = "ArbreGeon")

    #initialize arbregeon nodes
    #arbregeon outputs
    arbregeon.outputs.new("NodeSocketGeometry", "Geometry")
    arbregeon.outputs[0].attribute_domain = 'POINT'

    #node Group Output
    group_output = arbregeon.nodes.new("NodeGroupOutput")

    #initialize nodegroup node group
    def nodegroup_node_group(i):
        nodegroup= bpy.data.node_groups.new(type = "GeometryNodeTree", name = "NodeGroup")

        #initialize nodegroup nodes
        #nodegroup outputs
        nodegroup.outputs.new("NodeSocketGeometry", "Geometry")
        nodegroup.outputs[0].attribute_domain = 'POINT'

        #node Group Output
        group_output_1 = nodegroup.nodes.new("NodeGroupOutput")

        #nodegroup inputs

        #node Group Input
        group_input = nodegroup.nodes.new("NodeGroupInput")

        #node Join Geometry
        join_geometry = nodegroup.nodes.new("GeometryNodeJoinGeometry")

        #node String to Curves
        string_to_curves = nodegroup.nodes.new("GeometryNodeStringToCurves")
        data_font = bpy.data.fonts.load('STIX2Math.otf')
        string_to_curves.font = data_font
        string_to_curves.overflow = 'OVERFLOW'
        string_to_curves.align_x = 'CENTER'
        string_to_curves.align_y = 'TOP_BASELINE'
        string_to_curves.pivot_mode = 'BOTTOM_LEFT'
        #String
        string_to_curves.inputs[0].default_value = str(i)
        #Size
        string_to_curves.inputs[1].default_value = 1.0
        #Character Spacing
        string_to_curves.inputs[2].default_value = 1.0
        #Word Spacing
        string_to_curves.inputs[3].default_value = 1.0
        #Line Spacing
        string_to_curves.inputs[4].default_value = 1.0
        #Text Box Width
        string_to_curves.inputs[5].default_value = 0.0
        #Text Box Height
        string_to_curves.inputs[6].default_value = 0.0

        #node Resample Curve
        resample_curve = nodegroup.nodes.new("GeometryNodeResampleCurve")
        resample_curve.mode = 'EVALUATED'
        #Selection
        resample_curve.inputs[1].default_value = True
        #Count
        resample_curve.inputs[2].default_value = 10
        #Length
        resample_curve.inputs[3].default_value = 0.10000000149011612

        #node Fill Curve
        fill_curve = nodegroup.nodes.new("GeometryNodeFillCurve")
        fill_curve.mode = 'TRIANGLES'

        #node Extrude Mesh
        extrude_mesh = nodegroup.nodes.new("GeometryNodeExtrudeMesh")
        extrude_mesh.mode = 'FACES'
        #Selection
        extrude_mesh.inputs[1].default_value = True
        #Offset
        extrude_mesh.inputs[2].default_value = (0.0, 0.0, 0.0)
        #Offset Scale
        extrude_mesh.inputs[3].default_value = 0.03
        #Individual
        extrude_mesh.inputs[4].default_value = True

        #node Flip Faces
        flip_faces = nodegroup.nodes.new("GeometryNodeFlipFaces")
        #Selection
        flip_faces.inputs[1].default_value = True

        #node Join Geometry.001
        join_geometry_001 = nodegroup.nodes.new("GeometryNodeJoinGeometry")

        #node Realize Instances
        realize_instances = nodegroup.nodes.new("GeometryNodeRealizeInstances")

        #node Merge by Distance
        merge_by_distance = nodegroup.nodes.new("GeometryNodeMergeByDistance")
        merge_by_distance.mode = 'ALL'
        #Selection
        merge_by_distance.inputs[1].default_value = True
        #Distance
        merge_by_distance.inputs[2].default_value = 0.0010000000474974513

        #node Transform Geometry
        transform_geometry = nodegroup.nodes.new("GeometryNodeTransform")
        #Translation
        transform_geometry.inputs[1].default_value = (i, 0.0, 0.4)
        
        

        if n < 0 :
            transform_geometry.inputs[1].default_value[0] = n
            transform_geometry.inputs[1].keyframe_insert('default_value', frame=0)
            transform_geometry.inputs[1].default_value[0] = (n + 1) * 2
            transform_geometry.inputs[1].keyframe_insert('default_value', frame=250)
            transform_geometry.inputs[1].default_value[0] = n
        elif n > 0 :
            transform_geometry.inputs[1].default_value[0] = n
            transform_geometry.inputs[1].keyframe_insert('default_value', frame=0)
            transform_geometry.inputs[1].default_value[0] = (n + 1) * 2
            transform_geometry.inputs[1].keyframe_insert('default_value', frame=250)
            transform_geometry.inputs[1].default_value[0] = n
        else :
            transform_geometry.inputs[1].default_value[0] = 0
            transform_geometry.inputs[1].keyframe_insert('default_value', frame=0)
            transform_geometry.inputs[1].default_value[0] = 0
            transform_geometry.inputs[1].keyframe_insert('default_value', frame=250)
            transform_geometry.inputs[1].default_value[0] = 0
            
            
        
        
        
        #Rotation
        transform_geometry.inputs[2].default_value = (1.5707963705062866, 0.0, 0.0)
        #Scale
        transform_geometry.inputs[3].default_value = (1.0, 1.0, 1.0)

        #Set parents

        #Set locations
        group_output_1.location = (1175.0, 0.0)
        group_input.location = (-1185.0, 0.0)
        join_geometry.location = (985.0, 128.5)
        string_to_curves.location = (-985.0, 128.5)
        resample_curve.location = (-695.0, 128.5)
        fill_curve.location = (-455.0, 128.5)
        extrude_mesh.location = (-215.0, 128.5)
        flip_faces.location = (-215.0, -128.5)
        join_geometry_001.location = (25.0, 128.5)
        realize_instances.location = (265.0, 128.5)
        merge_by_distance.location = (505.0, 128.5)
        transform_geometry.location = (745.0, 128.5)

        #sSet dimensions
        group_output_1.width, group_output_1.height = 140.0, 100.0
        group_input.width, group_input.height = 140.0, 100.0
        join_geometry.width, join_geometry.height = 140.0, 100.0
        string_to_curves.width, string_to_curves.height = 190.0, 100.0
        resample_curve.width, resample_curve.height = 140.0, 100.0
        fill_curve.width, fill_curve.height = 140.0, 100.0
        extrude_mesh.width, extrude_mesh.height = 140.0, 100.0
        flip_faces.width, flip_faces.height = 140.0, 100.0
        join_geometry_001.width, join_geometry_001.height = 140.0, 100.0
        realize_instances.width, realize_instances.height = 140.0, 100.0
        merge_by_distance.width, merge_by_distance.height = 140.0, 100.0
        transform_geometry.width, transform_geometry.height = 140.0, 100.0

        #initialize nodegroup links
        #string_to_curves.Curve Instances -> resample_curve.Curve
        nodegroup.links.new(string_to_curves.outputs[0], resample_curve.inputs[0])
        #join_geometry_001.Geometry -> realize_instances.Geometry
        nodegroup.links.new(join_geometry_001.outputs[0], realize_instances.inputs[0])
        #flip_faces.Mesh -> join_geometry_001.Geometry
        nodegroup.links.new(flip_faces.outputs[0], join_geometry_001.inputs[0])
        #merge_by_distance.Geometry -> transform_geometry.Geometry
        nodegroup.links.new(merge_by_distance.outputs[0], transform_geometry.inputs[0])
        #extrude_mesh.Mesh -> join_geometry_001.Geometry
        nodegroup.links.new(extrude_mesh.outputs[0], join_geometry_001.inputs[0])
        #realize_instances.Geometry -> merge_by_distance.Geometry
        nodegroup.links.new(realize_instances.outputs[0], merge_by_distance.inputs[0])
        #fill_curve.Mesh -> flip_faces.Mesh
        nodegroup.links.new(fill_curve.outputs[0], flip_faces.inputs[0])
        #transform_geometry.Geometry -> join_geometry.Geometry
        nodegroup.links.new(transform_geometry.outputs[0], join_geometry.inputs[0])
        #resample_curve.Curve -> fill_curve.Curve
        nodegroup.links.new(resample_curve.outputs[0], fill_curve.inputs[0])
        #fill_curve.Mesh -> extrude_mesh.Mesh
        nodegroup.links.new(fill_curve.outputs[0], extrude_mesh.inputs[0])
        #join_geometry.Geometry -> group_output_1.Geometry
        nodegroup.links.new(join_geometry.outputs[0], group_output_1.inputs[0])
        
        fcurves = nodegroup.animation_data.action.fcurves
        for fcurve in fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'LINEAR'
                kf.easing = 'AUTO'
        
        return nodegroup

    #node Join Geometry
    join_geometry_1 = arbregeon.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_1.location = (718.0169677734375, 146.34579467773438)
    join_geometry_1.width, join_geometry_1.height = 140.0, 100.0
    arbregeon.links.new(join_geometry_1.outputs[0], group_output.inputs[0])
    #group.Geometry -> join_geometry_1.Geometry
    
    
    nodegroup = []
    group = []
    
    for i in range(-n, n + 1):
        nodegroup.append(nodegroup_node_group(i)) 
        group.append(arbregeon.nodes.new("GeometryNodeGroup"))
        group[i+n].node_tree = nodegroup[i+n]
        arbregeon.links.new(group[i+n].outputs[0], join_geometry_1.inputs[0])
        


    
    
    return arbregeon


arbregeon = arbregeon_node_group(10)
name = bpy.context.object.name
obj = bpy.data.objects[name]
mod = obj.modifiers.new(name = "ArbreGeon", type = 'NODES')
mod.node_group = arbregeon
