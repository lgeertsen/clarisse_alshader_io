import maya.cmds as cmds
from functools import partial

import os
import json

shaderNetwork = {
    "nodes": {},
    "connections": []
}

def main():
    createWindow()

def testButton(objects, *args):
    print(objects)
    basicFilter = "*.json"
    path = cmds.fileDialog2(fileFilter=basicFilter, dialogStyle=2)
    print(path[0])
    shaders_to_json(objA=objects, file_path=path[0])


def createWindow():
    window = cmds.window( title="Export Shader Network", iconName='Short Name', widthHeight=(200, 150) )
    selected = cmds.ls(sl=True);
    cmds.columnLayout( adjustableColumn=True )
    for obj in selected:
        cmds.text( label=obj )

    cmds.button( label='Convert Shader', command=partial(testButton, selected) )

    cmds.button( label='Close', command=('cmds.deleteUI(\"' + window + '\", window=True)') )
    cmds.setParent( '..' )

    cmds.showWindow( window )

def getAllNodes(nodes):
    for node in nodes:
        history = cmds.listHistory(node)
        for n in history:
            if not n in shaderNetwork["nodes"]:
                print(cmds.objectType(n))
                shaderNetwork["nodes"][n] = {}
                shaderNetwork["nodes"][n]["type"] = cmds.objectType(n)
                shaderNetwork["nodes"][n]["data"] = {}
                nodeAttributes = cmds.listAttr(n)
                for a in nodeAttributes:
                    try:
                        shaderNetwork["nodes"][n]["data"][a] = cmds.getAttr(n + '.' + str(a))
                    except:
                        pass

            attributes = cmds.listAttr(n)

            for attr in attributes:
                try:
                    connection = cmds.connectionInfo(n + '.' + str(attr), sfd=1)
                    if connection:
                        try:
                            shaderNetwork["connections"].append({
                                "from": cmds.listHistory(connection)[0],
                                "to": n,
                                "fromAttribute": connection,
                                "toAttributeComplete": n + '.' + str(attr),
                                "toAttribute": str(attr)

                            })
                        except:
                            pass
                except:
                    pass


        # for attr in attributes:
        #     try:
        #         connections = cmds.listConnections(node + '.' + attr, d=False, s=True)
        #         # links = cmds.connectionInfo(node + '.' + atr, sfd=1)
        #     except:
        #         pass
        #     if connections:
        #         getAllNodes(connections)





def shaders_to_json(objA=None, file_path=None):
    if not objA:
            return

    if not file_path:
        return

    shaders = []

    for i in objA:
        allChildren = cmds.listRelatives(i, ad=1)

        for eachChild in allChildren:
            # Get the shader groups attached to this particular object
            shaderGroups = cmds.listConnections(cmds.listHistory(eachChild))

            if shaderGroups is not None:
                # Get the material attached to the shader group
                materials = [x for x in cmds.ls(cmds.listConnections(shaderGroups), materials=1)]

                if materials:
                    # If its an AlSurface material add it to the list
                    #if cmds.nodeType(materials[0]) == 'alSurface':
                    if materials not in shaders:
                        shaders.append(materials[0])

    getAllNodes(shaders)
    print shaderNetwork["nodes"]

    for shader_name in shaders:

        attributes = cmds.listAttr(shader_name, visible=True)

        atrA = {'name': shader_name, 'data': []}

        # for i in attributes:

        # value = cmds.getAttr(shader_name + '.' + "baseColor")
        # print value
        # remap = cmds.listConnections(shader_name + '.' + 'baseColor', d=False, s=True)
        # remapConnenction = cmds.connectionInfo(shader_name + '.' + 'baseColor', sfd=1)
        # print remap
        # print remapConnenction
        # print cmds.listHistory(remapConnenction)[0]
        # remapAttributes = cmds.listAttr(remap, visible=True)
        # print remapAttributes
        # file1 = cmds.listConnections(remap[0] + '.' + 'color', d=False, s=True)
        # file1Connection = cmds.connectionInfo(remap[0] + '.' + 'color', sfd=1)
        # print file1
        # print file1Connection
        # print cmds.listHistory(file1Connection)[0]
        # print cmds.listAttr(file1, visible=True)
        # texture = cmds.listConnections(file1[0] + '.' + 'uvCoord', d=False, s=True)
        # textureConnection = cmds.connectionInfo(file1[0] + '.' + 'uvCoord', sfd=1)
        # print texture
        # print texture[0]
        # print textureConnection


            # value = cmds.getAttr(shader_name + '.' + str(i))

    #         if value:

    #             if isinstance(value, list):
    #                 value = value[0]

    #             # Check if output plug has a file node connection
    #             output_conn_node = cmds.listConnections(shader_name + '.' + str(i), d=False, s=True)


    #             # for clar_id, arnold_id in clarisse_arnold_pairs.iteritems():
    #                 # if i == arnold_id:
    #             attr = {i: value}
    #             atrA['data'].append(attr)
    #                     # break

    #     if atrA:
    #         shaderA.append(atrA)

    # if shaderA:




    with open(file_path, 'w') as fp:
        json.dump(shaderNetwork, fp, sort_keys=False, indent=4)

    print '[Info]Finished exporting material data...'



# shaders_to_json(objA=['pSphere1', 'pSphere2', 'pSphere3'], file_path='C:/Users/etudiant/Documents/clarisse_alshader_io/test_mat.json')
main()
