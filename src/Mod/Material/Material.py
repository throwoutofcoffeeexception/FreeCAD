#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2013-2015 - Juergen Riegel <FreeCAD@juergen-riegel.net> *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************

# here the usage description if you use this tool from the command line ("__main__")
CommandlineUsage = """Material - Tool to work with FreeCAD Material definition cards

Usage:
   Material [Options] card-file-name

Options:
 -c, --output-csv=file-name     write a comma separated grid with the material data

Exit:
 0      No Error or Warning found
 1      Argument error, wrong or less Arguments given

Tool to work with FreeCAD Material definition cards

Examples:

   Material  "StandardMaterial/Steel.FCMat"

Author:
  (c) 2013 Juergen Riegel
  mail@juergen-riegel.net
  Licence: LGPL

Version:
  0.1
"""


def importFCMat(fileName):
    "Read a FCMat file into a dictionary"
    try:
        import ConfigParser as configparser
    except ImportError:
        import configparser

    Config = configparser.RawConfigParser()
    Config.optionxform = str
    Config.read(fileName)
    dict1 = {}
    for section in Config.sections():
        options = Config.options(section)
        for option in options:
            dict1[option] = Config.get(section, option)

    return dict1


def exportFCMat(fileName, matDict):
    "Write a material dictionary to a FCMat file"
    try:
        import ConfigParser as configparser
    except ImportError:
        import configparser
    import string
    Config = configparser.RawConfigParser()

    # create groups
    for x in matDict.keys():
        grp, key = string.split(x, sep='_')
        if not Config.has_section(grp):
            Config.add_section(grp)

    # fill groups
    for x in matDict.keys():
        grp, key = string.split(x, sep='_')
        Config.set(grp, key, matDict[x])

    Preamble = "# This is a FreeCAD material-card file\n\n"
    # Writing our configuration file to 'example.cfg'
    with open(fileName, 'wb') as configfile:
        configfile.write(Preamble)
        Config.write(configfile)


def getMaterialAttributeStructure(withSpaces=None):
    # material properties
    # are there any more resources in FreeCAD source code where known material properties are defined except the material cards itself?
    # we should not have two of these list ...
    # withSpaces is used by the material editor ui, without spaces is used to save a material file
    if withSpaces:
        material_property_groups = (
            ('Meta', ('Card Name', 'Author And License', 'Source')),
            ('General', ('Name', 'Father', 'Description', 'Denisty', 'Vendor', 'ProductURL', 'SpecificPrice')),
            ('Mechanical', ('Youngs Modulus', 'Poisson Ratio', 'Ultimate Tensile Strength', 'Compressive Strength', 'Elasticity', 'Fracture Toughness')),
            ('Architectural', ('Execution Instructions', 'Fire Resistance Class', 'Standard Code', 'Thermal Conductivity', 'Sound Transmission Class', 'Color', 'Finish', 'Units Per Quantity', 'Environmental Efficiency Class')),
            ('Rendering', ('Diffuse Color', 'Ambient Color', 'Specular Color', 'Shininess', 'Emissive Color', 'Transparency', 'Vertex Shader', 'Fragment Shader', 'Texture Path', 'Texture Scaling')),
            ('Vector rendering', ('View Color', 'Father', 'View Linewidth', 'Section Color', 'Section Fill Pattern', 'Section Linewidth')),
            ('User defined', ())
        )
    else:
        material_property_groups = (
            ("Meta", ("CardName", "AuthorAndLicense", "Source")),
            ("General", ("Name", "Father", "Description", "Density", "Vendor", "ProductURL", "SpecificPrice")),
            ("Mechanical", ("YoungsModulus", "PoissonRatio", "UltimateTensileStrength", "CompressiveStrength", "Elasticity", "FractureToughness")),
            ("Architectural", ("Model", "ExecutionInstructions", "FireResistanceClass", "StandardCode", "ThermalConductivity", "SoundTransmissionClass", "Color", "Finish", "UnitsPerQuantity", "EnvironmentalEfficiencyClass")),
            ("Rendering", ("DiffuseColor", "AmbientColor", "SpecularColor", "Shininess", "EmissiveColor", "Transparency", "VertexShader", "FragmentShader", "TexturePath", "TextureScaling")),
            ("Vector rendering", ("ViewColor", "ViewFillPattern", "SectionFillPattern", "ViewLinewidth", "SectionLinewidth")),
            ("User defined", ())
        )
    return material_property_groups


if __name__ == '__main__':
    import sys
    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:", ["output-csv="])
    except getopt.GetoptError:
        # print help information and exit:
        sys.stderr.write(CommandlineUsage)
        sys.exit(1)

    # checking on the options
    for o, a in opts:
        if o in ("-c", "--output-csv"):
            print("writing file: " + a + "\n")
            OutPath = a

    # running through the files
    FileName = args[0]

    kv_map = importFCMat(FileName)
    for k in kv_map.keys():
        print(repr(k) + " : " + repr(kv_map[k]))
    sys.exit(0)  # no error
