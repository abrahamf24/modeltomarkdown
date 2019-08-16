from wb import *
import grt
from mforms import Utilities, FileChooser
import mforms
import re
from pprint import pprint
 
ModuleInfo = DefineModule(name="ModelToMarkdown", author="Abraham Flores Cosme", version="1.0", description="Model to data dictionary with markdown sintax")
 
@ModuleInfo.plugin("ModelToMarkdown", caption="Dictionary with markdown sintax", description="Model to data dictionary with markdown sintax", input=[wbinputs.currentCatalog()], pluginMenu="Catalog")
@ModuleInfo.export(grt.INT, grt.classes.db_Catalog)

def htmlDataDictionary(catalog):
    # Put plugin contents here
    mdOut = ""
    filechooser = FileChooser(mforms.SaveFile)
    filechooser.set_extensions("Markdown File (*.md)|*.md","md")
    if filechooser.run_modal():
       mdOut = filechooser.get_path()
    print "Markdown File: %s" % (mdOut)
    if len(mdOut) <= 1:
       return 1

    # iterate through columns from schema
    schema = catalog.schemata[0]
    mdFile = open(mdOut, "w")
    print >>mdFile, "# Diccionario de datos"
    print >>mdFile, ""
    tables = schema.tables
    tables = sorted(tables, key=orderTables)

    for table in tables:
        print >>mdFile, "- [%s](#markdown-header-%s)" % (table.name,table.name)

    print >>mdFile, ""

    for table in tables:
        print >>mdFile, "## %s" % (table.name)
        print >>mdFile, "%s" % (table.comment)
        print >>mdFile, ""
        print >>mdFile, "|Nombre|Tipo de dato|Nulo|PK|FK|Default|Comentario|"
        print >>mdFile, "|------|------------|----|--|--|-------|----------|"

        for column in table.columns:
            pk = ('No', 'Yes')[bool(table.isPrimaryKeyColumn(column))]
            fk = ('No', 'Yes')[bool(table.isForeignKeyColumn(column))]
            nn = ('No', 'Yes')[bool(column.isNotNull)]

            print >>mdFile, "|%s|%s|%s|%s|%s|%s|%s|" % (column.name,column.formattedType,nn,pk,fk,column.defaultValue,column.comment.replace('\n',''))

        print >>mdFile, ""
        print >>mdFile, "[Regresar al listado](#markdown-header-diccionario-de-datos)"
        print >>mdFile, ""
        print >>mdFile, ""

    Utilities.show_message("Diccionario de datos creado", "El archivo markdonw fue generado exitosamente", "Aceptar","","")
    return 0

def orderTables(e):
    return e.name