import importlib
import pip

class packages:
    def install_and_import(self,package):
        try:
            importlib.import_module(package)
        except ImportError:
            pip.main(['install', package])
        finally:
            globals()[package] = importlib.import_module(package)

    def intial_requirments(self):
        list = ['pandas','numpy','sklearn','matplotlib','plotly','shapely','pykrige','folium']
        for modules in list:
            self.install_and_import(modules)