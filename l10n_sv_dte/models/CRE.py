# -*- coding: utf-8 -*-

from .MixedClass import GeneratedsSuper
from .MixedClass import showIndent
from .MixedClass import quote_xml
import re as re_
import sys

try:
    from lxml import etree as etree_
except ImportError:
    from xml.etree import ElementTree as etree_

Validate_simpletypes_ = True
if sys.version_info.major == 2:
    BaseStrType_ = basestring
else:
    BaseStrType_ = str

try:
    from generatedsnamespaces import GenerateDSNamespaceDefs as GenerateDSNamespaceDefs_
except ImportError:
    GenerateDSNamespaceDefs_ = {}

#
# Globals
#

ExternalEncoding = 'utf-8'
Tag_pattern_ = re_.compile(r'({.*})?(.*)')
String_cleanup_pat_ = re_.compile(r"[\n\r\s]+")
Namespace_extract_pat_ = re_.compile(r'{(.*)}(.*)')
CDATA_pattern_ = re_.compile(r"<!\[CDATA\[.*?\]\]>", re_.DOTALL)

# Change this to redirect the generated superclass module to use a
# specific subclass module.
CurrentSubclassModule_ = None

#
# Data representation classes.
#


class ComprobanteretencionElectronico(GeneratedsSuper):
    """Elemento Raiz de Comprobante de Retencion Electronico"""
    subclass = None
    superclass = None

    def __init__(self, identificacion=None, emisor=None, receptor=None,
                 cuerpoDocumento=None, resumen=None, extension=None, apendice=None):
        self.original_tagname_ = None
        self.identificacion = identificacion
        self.emisor = emisor
        self.receptor = receptor
        self.cuerpoDocumento = cuerpoDocumento
        self.resumen = resumen
        self.extension = extension
        self.apendice = apendice

    def get_identificacion(self):
        return self.identificacion

    def set_identificacion(self, identificacion):
        self.identificacion = identificacion

    def get_emisor(self):
        return self.emisor

    def set_emisor(self, emisor):
        self.emisor = emisor

    def get_receptor(self):
        return self.receptor

    def set_receptor(self, receptor):
        self.receptor = receptor

    def get_cuerpoDocumento(self):
        return self.cuerpoDocumento

    def set_cuerpoDocumento(self, cuerpoDocumento):
        self.cuerpoDocumento = cuerpoDocumento

    def get_resumen(self):
        return self.resumen

    def set_resumen(self, resumen):
        self.resumen = resumen

    def hasContent_(self):
        if (
                self.identificacion is not None or
                self.emisor is not None or
                self.receptor is not None or
                self.cuerpoDocumento is not None or
                self.resumen is not None or
                self.extension is not None or
                self.apendice is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='ECF', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ECF')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        # outfile.write(bytes(('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        if self.hasContent_():
            # outfile.write(bytes(('>%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='ECF', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('%s}%s' % (namespace_, eol_)).encode()))
            # outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportChildren(self, outfile, level, namespace_='', name_='ECF', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''

        if self.identificacion is not None:
            self.identificacion.export(outfile, level, namespace_, name_='identificacion', pretty_print=pretty_print)
        if self.emisor is not None:
            self.emisor.export(outfile, level, namespace_, name_='emisor', pretty_print=pretty_print)
        if self.receptor is not None:
            self.receptor.export(outfile, level, namespace_, name_='receptor', pretty_print=pretty_print)
        if self.cuerpoDocumento is not None:
            self.cuerpoDocumento.export(outfile, level, namespace_, name_='cuerpoDocumento', pretty_print=pretty_print)
        if self.resumen is not None:
            self.resumen.export(outfile, level, namespace_, name_='resumen', pretty_print=pretty_print)

        if self.extension is not None:
            self.extension.export(outfile, level, namespace_, name_='extension', pretty_print=pretty_print)
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"extension":null,%s' % eol_).encode()))
        if self.apendice is not None:
            self.apendice.export(outfile, level, namespace_, name_='apendice', pretty_print=pretty_print)
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"apendice":null%s' % eol_).encode()))


class Identificacion(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, version, ambiente=None, tipoDTE=None, numeroControl=None, codigoGeneracion=None, tipoModelo=None,
                 tipoOperacion=None, fecEmi=None, horEmi=None, tipoMoneda=None, tipoContingencia=None, motivoContin=None):
        self.original_tagname_ = None
        self.version = version
        self.ambiente = ambiente
        self.tipoDTE = tipoDTE
        self.numeroControl = numeroControl
        self.codigoGeneracion = codigoGeneracion
        self.tipoModelo = tipoModelo
        self.tipoOperacion = tipoOperacion
        self.fecEmi = fecEmi
        self.horEmi = horEmi
        self.tipoMoneda = tipoMoneda
        self.tipoContingencia = tipoContingencia
        self.motivoContin = motivoContin

    def get_version(self):
        return self.version

    def set_version(self, version):
        self.version = version

    def get_ambiente(self):
        return self.ambiente

    def set_ambiente(self, ambiente):
        self.ambiente = ambiente

    def get_tipoDTE(self):
        return self.tipoDTE

    def set_tipoDTE(self, tipoDTE):
        self.tipoDTE = tipoDTE

    def get_numeroControl(self):
        return self.numeroControl

    def set_numeroControl(self, numeroControl):
        self.numeroControl = numeroControl

    def get_codigoGeneracion(self):
        return self.codigoGeneracion

    def set_codigoGeneracion(self, codigoGeneracion):
        self.codigoGeneracion = codigoGeneracion

    def hasContent_(self):
        if (
                self.version is not None or
                self.ambiente is not None or
                self.tipoDTE is not None or
                self.numeroControl is not None or
                self.codigoGeneracion is not None or
                self.tipoModelo is not None or
                self.tipoOperacion is not None or
                self.fecEmi is not None or
                self.horEmi is not None or
                self.tipoMoneda is not None or
                self.tipoContingencia is not None or
                self.motivoContin is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='identificacion', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('identificacion')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(
            bytes(('%s"%s":%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        if self.hasContent_():
            outfile.write(bytes(('{%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='Identificacion', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            # outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
            outfile.write(bytes(('%s},%s' % (namespace_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportChildren(self, outfile, level, namespace_='', name_='EmisorType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.version is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"version":%s,%s' % (
                self.gds_encode(self.gds_format_integer(self.version, input_name='Version')),
                eol_)).encode()))
        if self.ambiente is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"ambiente":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.ambiente), input_name='Ambiente')),
                eol_)).encode()))
        if self.tipoDTE is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"tipoDte":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.tipoDTE), input_name='TipoDTE')),
                eol_)).encode()))
        if self.numeroControl is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"numeroControl":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.numeroControl), input_name='NumeroControl')),
                eol_)).encode()))
        if self.tipoModelo is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"tipoModelo":%s,%s' % (
                self.gds_format_integer(self.tipoModelo, input_name='Modelo de Facturación'),
                eol_)).encode()))
        if self.tipoOperacion is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"tipoOperacion":%s,%s' % (
                self.gds_format_integer(self.tipoOperacion, input_name='Tipo de Transmisión'),
                eol_)).encode()))
        if self.tipoContingencia is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"tipoContingencia":%s,%s' % (
                self.gds_format_integer(self.tipoContingencia, input_name='Tipo de Contingencia'),
                eol_)).encode()))
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"tipoContingencia":null,%s' % eol_).encode()))
        if self.motivoContin is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"motivoContin":"%s",%s' % (
                self.gds_encode(
                    self.gds_format_string(quote_xml(self.motivoContin), input_name='Código de Generación')),
                eol_)).encode()))
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"motivoContin":null,%s' % eol_).encode()))
        if self.codigoGeneracion is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"codigoGeneracion":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.codigoGeneracion), input_name='Código de Generación')),
                eol_)).encode()))
        if self.fecEmi is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"fecEmi":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.fecEmi), input_name='Fecha de Generación')),
                eol_)).encode()))
        if self.horEmi is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"horEmi":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.horEmi), input_name='Hora de Generación')),
                eol_)).encode()))
        if self.tipoMoneda is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"tipoMoneda":"%s"%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.tipoMoneda), input_name='Tipo de Moneda')),
                eol_)).encode()))


class Emisor(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, nit=None, nrc=None, nombre=None, codActividad=None, descActividad=None, telefono=None,
                 correo=None, nombreComercial=None, tipoEstablecimiento=None, direccion=None, puntoVentaMH=None,
                 puntoVenta=None, codigo=None, codigoMH=None):
        self.original_tagname_ = None
        self.nit = nit
        self.nrc = nrc
        self.nombre = nombre
        self.codActividad = codActividad
        self.descActividad = descActividad
        self.telefono = telefono
        self.correo = correo
        self.nombreComercial = nombreComercial
        self.tipoEstablecimiento = tipoEstablecimiento
        self.direccion = direccion
        self.puntoVentaMH = puntoVentaMH
        self.puntoVenta = puntoVenta
        self.codigo = codigo
        self.codigoMH = codigoMH

    def get_nit(self):
        return self.nit

    def set_nit(self, nit):
        self.nit = nit

    def get_telefono(self):
        return self.telefono

    def set_telefono(self, telefono):
        self.telefono = telefono

    def get_correo(self):
        return self.correo

    def set_correo(self, correo):
        self.correo = correo

    def get_nombreComercial(self):
        return self.nombreComercial

    def set_nombreComercial(self, nombreComercial):
        self.nombreComercial = nombreComercial

    def get_tipoEstablecimiento(self):
        return self.tipoEstablecimiento

    def set_tipoEstablecimiento(self, tipoEstablecimiento):
        self.tipoEstablecimiento = tipoEstablecimiento

    def hasContent_(self):
        if (
                self.nit is not None or
                self.nombre is not None or
                self.codActividad is not None or
                self.telefono is not None or
                self.correo is not None or
                self.puntoVentaMH is not None or
                self.puntoVenta is not None or
                self.codigoMH is not None or
                self.codigo is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='Emisor', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('identificacion')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(
            bytes(('%s"%s":%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        if self.hasContent_():
            outfile.write(bytes(('{%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='Identificacion', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            # outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
            outfile.write(bytes(('%s},%s' % (namespace_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportChildren(self, outfile, level, namespace_='', name_='EmisorType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.nit is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"nit":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.nit), input_name='NIT (Emisor)')),
                eol_)).encode()))
        if self.nrc is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"nrc":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.nrc), input_name='NRC (Emisor)')),
                eol_)).encode()))
        if self.nombre is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"nombre":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.nombre), input_name='Nombre')),
                eol_)).encode()))
        if self.codActividad is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"codActividad":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.codActividad), input_name='CodActividad')),
                eol_)).encode()))
        if self.descActividad is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"descActividad":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.descActividad), input_name='Actividad Económica (Emisor)')),
                eol_)).encode()))
        if self.telefono is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"telefono":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.telefono), input_name='Telefono')),
                eol_)).encode()))
        if self.correo is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"correo":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.correo), input_name='Correo')),
                eol_)).encode()))
        if self.nombreComercial is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"nombreComercial":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.nombreComercial), input_name='Nombre Comercial (Emisor)')),
                eol_)).encode()))
        if self.tipoEstablecimiento is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"tipoEstablecimiento":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.tipoEstablecimiento), input_name='Tipo de establecimiento (Emisor)')),
                eol_)).encode()))
        if self.codigoMH is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"codigoMH":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.codigoMH), input_name='Nombre Comercial (Emisor)')),
                eol_)).encode()))
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"codigoMH":null,%s' % eol_).encode()))
        if self.codigo is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"codigo":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.codigo), input_name='Nombre Comercial (Emisor)')),
                eol_)).encode()))
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"codigo":null,%s' % eol_).encode()))
        if self.puntoVentaMH is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"puntoVentaMH":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.puntoVentaMH), input_name='Nombre Comercial (Emisor)')),
                eol_)).encode()))
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"puntoVentaMH":null,%s' % eol_).encode()))
        if self.puntoVenta is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"puntoVenta":"%s",%s' % (
                self.gds_encode(
                    self.gds_format_string(quote_xml(self.puntoVenta), input_name='Nombre Comercial (Emisor)')),
                eol_)).encode()))
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"puntoVenta":null,%s' % eol_).encode()))
        if self.direccion is not None:
            self.direccion.export(outfile, level, namespace_, name_='direccion', pretty_print=pretty_print)
        if self.telefono is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"telefono":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.telefono), input_name='Telefono')),
                eol_)).encode()))
        if self.correo is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"correo":"%s"%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.correo), input_name='Correo')),
                eol_)).encode()))


class Direccion(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, departamento=None, municipio=None, complemento=None,):
        self.original_tagname_ = None
        self.departamento = departamento
        self.municipio = municipio
        self.complemento = complemento

    def get_departamento(self):
        return self.departamento

    def set_departamento(self, departamento):
        self.departamento = departamento

    def get_municipio(self):
        return self.municipio

    def set_municipio(self, municipio):
        self.municipio = municipio

    def get_complemento(self):
        return self.complemento

    def set_complemento(self, complemento):
        self.complemento = complemento

    def hasContent_(self):
        if (
                self.departamento is not None or
                self.municipio is not None or
                self.complemento is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='Emisor', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('identificacion')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(
            bytes(('%s"%s":%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        if self.hasContent_():
            outfile.write(bytes(('{%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='Identificacion', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            # outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
            outfile.write(bytes(('%s},%s' % (namespace_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportChildren(self, outfile, level, namespace_='', name_='EmisorType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.departamento is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"departamento":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.departamento), input_name='Dirección: Departamento')),
                eol_)).encode()))
        if self.municipio is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"municipio":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.municipio), input_name='Dirección: Municipio')),
                eol_)).encode()))
        if self.complemento is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"complemento":"%s"%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.complemento), input_name='Dirección: complemento')),
                eol_)).encode()))


class Receptor(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, tipoDocumento=None, numDocumento=None, rnc=None, nit=None, nombre=None, nrc=None, codActividad=None, nombreComercial=None,
                 descActividad=None, direccion=None, telefono=None, correo=None):
        self.original_tagname_ = None
        self.tipoDocumento = tipoDocumento
        self.numDocumento = numDocumento
        self.rnc = rnc
        self.nit = nit
        self.nombre = nombre
        self.nrc = nrc
        self.codActividad = codActividad
        self.descActividad = descActividad
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.nombreComercial = nombreComercial

    def get_nit(self):
        return self.nit

    def set_nit(self, nit):
        self.nit = nit

    def get_nombre(self):
        return self.nombre

    def set_nombre(self, nombre):
        self.nombre = nombre

    def hasContent_(self):
        if (
                self.tipoDocumento is not None or
                self.numDocumento is not None or
                self.nit is not None or
                self.rnc is not None or
                self.nombre is not None or
                self.nrc is not None or
                self.codActividad is not None or
                self.descActividad is not None or
                self.direccion is not None or
                self.telefono is not None or
                self.correo is not None or
                self.nombreComercial is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='Receptor', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('identificacion')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(
            bytes(('%s"%s":%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        if self.hasContent_():
            outfile.write(bytes(('{%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='Identificacion', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            # outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
            outfile.write(bytes(('%s},%s' % (namespace_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportChildren(self, outfile, level, namespace_='', name_='EmisorType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.tipoDocumento is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"tipoDocumento":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.tipoDocumento), input_name='Tipo de documento de identificación (Receptor)')),
                eol_)).encode()))
        if self.numDocumento is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"numDocumento":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.numDocumento), input_name='Número de documento de Identificación (Receptor)')),
                eol_)).encode()))
        if self.rnc is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"rnc":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.rnc), input_name='RNC')),
                eol_)).encode()))
        if self.nit is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"nit":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.nit), input_name='NIT')),
                eol_)).encode()))
        if self.nrc is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"nrc":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.nrc), input_name='NRC (Receptor)')),
                eol_)).encode()))
        if self.nombre is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"nombre":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.nombre), input_name='Nombre')),
                eol_)).encode()))
        if self.codActividad is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"codActividad":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.codActividad), input_name='Código de Actividad Económica (Receptor)')),
                eol_)).encode()))
        if self.descActividad is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"descActividad":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.descActividad), input_name='Actividad Económica (Receptor)')),
                eol_)).encode()))
        if self.nombreComercial is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"nombreComercial":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.nombreComercial), input_name='Nombre Comercial (Receptor)')),
                eol_)).encode()))
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"nombreComercial":null,%s' % eol_).encode()))
        if self.direccion is not None:
            self.direccion.export(outfile, level, namespace_, name_='direccion', pretty_print=pretty_print)
        else:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"direccion":null,%s' % eol_).encode()))
        if self.telefono is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"telefono":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.telefono), input_name='Actividad Económica (Receptor)')),
                eol_)).encode()))
        if self.correo is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"correo":"%s"%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.correo), input_name='Correo electrónico (Receptor)')),
                eol_)).encode()))


class CuerpoDocumento(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, Item=None):
        self.original_tagname_ = None
        if Item is None:
            self.Item = []
        else:
            self.Item = Item

    def get_Item(self):
        return self.Item

    def set_Item(self, Item):
        self.Item = Item

    def add_Item(self, value):
        self.Item.append(value)

    def insertItem_at(self, index, value):
        self.Item.insert(index, value)

    def replace_Item_at(self, index, value):
        self.Item[index] = value

    def hasContent_(self):
        if (
                self.Item
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='identificacion', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('identificacion')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(
            bytes(('%s"%s":%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        if self.hasContent_():
            outfile.write(bytes(('[%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='Identificacion', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            # outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
            outfile.write(bytes(('%s],%s' % (namespace_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportChildren(self, outfile, level, namespace_='', name_='DetalleServicioType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for i, LineaItem_ in enumerate(self.Item, 1):
            LineaItem_.export(outfile, level, namespace_, name_='Item', pretty_print=pretty_print, enu=i, tam=len(self.Item))


class Item(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, numItem, descripcion=None, tipoDte=None, tipoDoc=None, numDocumento=None, fechaEmision=None,
                 ivaRetenido=0.00, montoSujetoGrav=0.00, codigoRetencionMH=None):
        self.original_tagname_ = None
        self.numItem = numItem
        self.descripcion = descripcion
        self.tipoDte = tipoDte
        self.tipoDoc = tipoDoc
        self.numDocumento = numDocumento
        self.fechaEmision = fechaEmision
        self.ivaRetenido = ivaRetenido
        self.montoSujetoGrav = montoSujetoGrav
        self.codigoRetencionMH = codigoRetencionMH

    def get_numItem(self):
        return self.numItem

    def set_numItem(self, numItem):
        self.numItem = numItem

    def get_descripcion(self):
        return self.descripcion

    def set_descripcion(self, descripcion):
        self.descripcion = descripcion

    def get_tipoDte(self):
        return self.tipoDte

    def set_tipoDte(self, tipoDte):
        self.tipoDte = tipoDte

    def get_tipoDoce(self):
        return self.tipoDoc

    def set_tipoDoc(self, tipoDoc):
        self.tipoDoc = tipoDoc

    def get_numDocumento(self):
        return self.numDocumento

    def set_numDocumento(self, numDocumento):
        self.numDocumento = numDocumento

    def get_fechaEmision(self):
        return self.fechaEmision

    def set_fechaEmision(self, fechaEmision):
        self.fechaEmision = fechaEmision

    def get_ivaRetenido(self):
        return self.ivaRetenido

    def set_ivaRetenido(self, ivaRetenido):
        self.ivaRetenido = ivaRetenido

    def get_montoSujetoGrav(self):
        return self.montoSujetoGrav

    def set_montoSujetoGrav(self, montoSujetoGrav):
        self.montoSujetoGrav = montoSujetoGrav

    def get_codigoRetencionMH(self):
        return self.codigoRetencionMH

    def set_codigoRetencionMH(self, codigoRetencionMH):
        self.codigoRetencionMH = codigoRetencionMH

    def hasContent_(self):
        if (
                self.numItem is not None or
                self.descripcion is not None or
                self.tipoDte is not None or
                self.tipoDoc is not None or
                self.numDocumento is not None or
                self.fechaEmision is not None or
                self.ivaRetenido is not None or
                self.montoSujetoGrav is not None or
                self.codigoRetencionMH is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='Item', namespacedef_='', pretty_print=True, enu=None, tam=None):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('identificacion')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(
            # bytes(('%s"%s":%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
            bytes(('%s%s' % (namespace_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        if self.hasContent_():
            outfile.write(bytes(('{%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='Identificacion', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            # outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
            if enu == 1 and tam == 1:
                outfile.write(bytes(('%s}%s' % (namespace_, eol_)).encode()))
            elif enu != tam:
                outfile.write(bytes(('%s},%s' % (namespace_, eol_)).encode()))
            else:
                outfile.write(bytes(('%s}%s' % (namespace_, eol_)).encode()))
        #     outfile.write(bytes(('%s}%s' % (namespace_, eol_)).encode()))
        # else:
        #     outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportChildren(self, outfile, level, namespace_='', name_='EmisorType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.numItem is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"numItem":%s,%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.numItem), input_name='NumItem')),
                eol_)).encode()))
        if self.descripcion is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"descripcion":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.descripcion), input_name='Descripcion')),
                eol_)).encode()))
        if self.tipoDte is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"tipoDte":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.tipoDte), input_name='Descripcion')),
                eol_)).encode()))
        if self.tipoDoc is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"tipoDoc":%s,%s' % (
                self.gds_encode(self.gds_format_integer(self.tipoDoc, input_name='Version')),
                eol_)).encode()))
        if self.numDocumento is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"numDocumento":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.numDocumento), input_name='Descripcion')),
                eol_)).encode()))
        if self.fechaEmision is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"fechaEmision":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.fechaEmision), input_name='Fecha de Generación')),
                eol_)).encode()))
        if self.montoSujetoGrav is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"montoSujetoGrav":%s,%s' % (
                self.gds_encode(self.gds_format_float(self.montoSujetoGrav, input_name='PrecioUni')),
                eol_)).encode()))
        if self.codigoRetencionMH is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"codigoRetencionMH":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.codigoRetencionMH), input_name='Descripcion')),
                eol_)).encode()))
        if self.ivaRetenido is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"ivaRetenido":%s%s' % (
                self.gds_encode(self.gds_format_float(self.ivaRetenido, input_name='PrecioUni')),
                eol_)).encode()))


class Resumen(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, totalSujetoRetencion=0.00, totalIVAretenido=0.00, totalIVAretenidoLetras=None,
                 ):
        self.original_tagname_ = None
        self.totalSujetoRetencion = totalSujetoRetencion
        self.totalIVAretenido = totalIVAretenido
        self.totalIVAretenidoLetras = totalIVAretenidoLetras
        # if pagos is None:
        #     self.pagos = []
        # else:
        #     self.pagos = pagos

    def set_totalIVAretenidoLetras(self, totalIVAretenidoLetras):
        self.totalIVAretenidoLetras = totalIVAretenidoLetras

    def get_totalIVAretenidoLetrasn(self):
        return self.totalIVAretenidoLetras

    def set_totalSujetoRetencion(self, totalSujetoRetencion):
        self.totalSujetoRetencion = totalSujetoRetencion

    def get_totalSujetoRetencion(self):
        return self.totalSujetoRetencion

    def set_totalIVAretenido(self, totalIVAretenido):
        self.totalIVAretenido = totalIVAretenido

    def get_totalIVAretenido(self):
        return self.totalIVAretenido

    def hasContent_(self):
        if (
                self.totalIVAretenidoLetras is not None or
                self.totalSujetoRetencion is not None or
                self.totalIVAretenido is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='Resumen', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('identificacion')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(
            bytes(('%s"%s":%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        if self.hasContent_():
            outfile.write(bytes(('{%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='Identificacion', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            # outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
            outfile.write(bytes(('%s},%s' % (namespace_, eol_)).encode()))
        else:
            outfile.write(bytes(('/>%s' % (eol_,)).encode()))

    def exportChildren(self, outfile, level, namespace_='', name_='EmisorType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.totalIVAretenidoLetras is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"totalIVAretenidoLetras":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.totalIVAretenidoLetras), input_name='Version')),
                eol_)).encode()))
        if self.totalSujetoRetencion is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"totalSujetoRetencion":%s,%s' % (
                self.gds_encode(
                    self.gds_format_float(self.totalSujetoRetencion, input_name='Retención Renta')),
                eol_)).encode()))
        if self.totalIVAretenido is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"totalIVAretenido":%s%s' % (
                self.gds_encode(
                    self.gds_format_float(self.totalIVAretenido, input_name='Retención Renta')),
                eol_)).encode()))


class Tributos(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, Item=None):
        self.original_tagname_ = None
        if Item is None:
            self.Item = []
        else:
            self.Item = Item

    def get_Item(self):
        return self.Item

    def set_Item(self, Item):
        self.Item = Item

    def add_Item(self, value):
        self.Item.append(value)

    def insertItem_at(self, index, value):
        self.Item.insert(index, value)

    def replace_Item_at(self, index, value):
        self.Item[index] = value

    def hasContent_(self):
        if (
                self.Item
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='identificacion', namespacedef_='', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('identificacion')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(
            bytes(('%s"%s":%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        if self.hasContent_():
            outfile.write(bytes(('[%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='Identificacion', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            # outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
            outfile.write(bytes(('%s],%s' % (namespace_, eol_)).encode()))
        else:
            # outfile.write(bytes(('/>%s' % (eol_,)).encode()))
            outfile.write(bytes(('null,%s' % eol_).encode()))

    def exportChildren(self, outfile, level, namespace_='', name_='DetalleServicioType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for i, LineaItem_ in enumerate(self.Item, 1):
            LineaItem_.export(outfile, level, namespace_, name_='Item', pretty_print=pretty_print, enu=i, tam=len(self.Item))


class Tributo(GeneratedsSuper):
    subclass = None
    superclass = None

    def __init__(self, codigo=None, descripcion=None, valor=None):
        self.original_tagname_ = None
        self.codigo = codigo
        self.descripcion = descripcion
        self.valor = valor

    def get_codigo(self):
        return self.codigo

    def set_codigo(self, codigo):
        self.codigo = codigo

    def get_descripcion(self):
        return self.descripcion

    def set_descripcion(self, descripcion):
        self.descripcion = descripcion

    def get_valor(self):
        return self.valor

    def set_valor(self, valor):
        self.valor = valor

    def hasContent_(self):
        if (
                self.codigo is not None or
                self.descripcion is not None or
                self.valor is not None
        ):
            return True
        else:
            return False

    def export(self, outfile, level, namespace_='', name_='Item', namespacedef_='', pretty_print=True, enu=None, tam=None):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('identificacion')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        showIndent(outfile, level, pretty_print)
        outfile.write(
            # bytes(('%s"%s":%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
            bytes(('%s%s' % (namespace_, namespacedef_ and ' ' + namespacedef_ or '',)).encode()))
        if self.hasContent_():
            outfile.write(bytes(('{%s' % (eol_,)).encode()))
            self.exportChildren(outfile, level + 1, namespace_='', name_='Identificacion', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            # outfile.write(bytes(('</%s%s>%s' % (namespace_, name_, eol_)).encode()))
            if enu == 1 and tam == 1:
                outfile.write(bytes(('%s}%s' % (namespace_, eol_)).encode()))
            elif enu != tam:
                outfile.write(bytes(('%s},%s' % (namespace_, eol_)).encode()))
            else:
                outfile.write(bytes(('%s}%s' % (namespace_, eol_)).encode()))

    def exportChildren(self, outfile, level, namespace_='', name_='EmisorType', fromsubclass_=False,
                       pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.codigo is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"codigo":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.codigo), input_name='Resumen Código de Tributo')),
                eol_)).encode()))
        if self.descripcion is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"descripcion":"%s",%s' % (
                self.gds_encode(self.gds_format_string(quote_xml(self.descripcion), input_name='Nombre del Tributo')),
                eol_)).encode()))
        if self.valor is not None:
            showIndent(outfile, level, pretty_print)
            outfile.write(bytes(('"valor":%s%s' % (
                self.gds_encode(self.gds_format_float(self.valor, input_name='Valor del Tributo')),
                eol_)).encode()))
