'''
https://www.osgeo.cn/geonetwork/annexes/gallery/gallery.html
测试其中服务
'''
import sys

sys.path.append('./')
from owslib.csw import CatalogueServiceWeb

# request=GetCapabilities&service=CSW&version=2.0.2

geonetwork_svrs = {
    's1': {
        'url': 'http://catalogue.geo-ide.developpement-durable.gouv.fr/catalogue/srv/chi/csw',
        'valid': False,
    },
    's2': {
        'url': 'http://geocatalog.webservice-energy.org/geonetwork/srv/eng/csw',
        'valid': True,
    },
    's3': {
        'url': 'https://geometadatensuche.inspire.gv.at/metadatensuche/srv/ger/csw',
        'valid': False,
    },
    's4': {
        'url': 'http://geoportal.kscnet.ru/geonetwork/srv/eng/csw',
        'valid': True,
    },
    's5': {
        'url': 'https://metawal.wallonie.be/geonetwork/srv/chi/csw?request=GetCapabilities&service=CSW&version=2.0.2',
        'valid': True,
    },
    's6': {
        'url': 'http://salbgeonetwork.grid.unep.ch/geonetwork/srv/eng/csw?request=GetCapabilities&service=CSW&version=2.0.2',
        'valid': False,
        'note': '无法访问',
    },
    's7': {
        'url': 'https://data.apps.fao.org/map/catalog/srv/eng/csw?request=GetCapabilities&service=CSW&version=2.0.2',
        'valid': True,
        'note': 'http://www.fao.org/geonetwork/',
    },
    's8': {
        'url': 'https://www.geoguyane.fr/accueil?request=GetCapabilities&service=CSW&version=2.0.2',
        'valid': False,
    },
    's9': {
        'url': 'https://www.geonorge.no/geonetwork/srv/nor/csw',
        'valid': True,
    },
    's10': {
        'url': 'http://www.geopal.org/accueil',
        'valid': False,
    },
    's11': {
        'url': 'https://metadadosgeo.ibge.gov.br/geonetwork_ibge/srv/eng/csw?',
        'valid': True,
        'note': 'http://www.metadados.geo.ibge.gov.br/geonetwork_ibge/',
    },
    's12': {
        'url': 'http://www.metadados.idesp.sp.gov.br/catalogo/srv/eng/csw?',
        'valid': True,
    },
    's13': {
        'url': 'https://www.nationaalgeoregister.nl/geonetwork/srv/eng/csw?',
        'valid': True,
    },
    's14': {
        'url': 'http://www.sadc.int/geonetwork',
        'valid': False,
    },
    's15': {
        'url': 'http://www.sandre.eaufrance.fr/atlas/srv/chi/csw',
        'valid': True,
    },
    's16': {
        'url': 'http://www.sigloire.fr/',
        'valid': False,
    },
    's17': {
        'url': 'http://www.wodgik.katowice.pl:8080/geonetwork/srv/chi/csw',
        'valid': True,
    },
    's18': {
        'url': 'https://catalogue-imos.aodn.org.au/geonetwork/srv/eng/csw',
        'valid': True,
    },
    's19': {
        'url': 'https://catalogue.grand-chatellerault.fr/',
        'valid': False,
        'note': '无法访问',
    },
    's20': {
        'url': 'https://download.data.grandlyon.com/catalogue/srv/eng/csw',
        'valid': True,
    },
    's21': {'url': 'https://gdk.gdi-de.org/gdi-de/', 'valid': False, 'note': '无法访问'},
    's22': {
        'url': 'https://geocatalogue.apur.org/catalogue/srv/eng/csw',
        'valid': True,
    },
}

for key in geonetwork_svrs:
    if key in ['s22', 's6']:
        pass

    else:
        continue
    print('\033[31m' + 'x' * 120 + '\033[0m')
    svr = geonetwork_svrs[key]
    print(key, svr)

    if svr['valid']:
        csw = CatalogueServiceWeb(svr['url'], version='2.0.2')
        print(csw.identification.type)
