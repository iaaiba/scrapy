import logging
import os
import shutil
import geopandas
from shapely.geometry import mapping
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from .. import publisher
from . import utils

log = logging.getLogger(__name__)


class ICMBioImporter:
    def __init__(self, download_dir: str = None):
        prefs = {'download.default_directory': download_dir}

        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", prefs)
        options.add_argument('ignore-certificate-errors')
        options.add_argument('disable-dev-shm-usage')
        options.add_argument('disable-gpu')
        # options.add_argument('headless')

        self._driver = webdriver.Chrome(options=options)
        self._url = 'http://mapas.mma.gov.br/i3geo/datadownload.htm'
        self._download_dir = download_dir or '/tmp/icmbio-temp/'
        self._actions = ActionChains(self._driver)

        os.makedirs(self._download_dir, exist_ok=True)

    def set_up(self):
        log.debug(f'URL: {self._url}')
        self._driver.get(self._url)
        self._wait_element((By.ID, 'ygtvt14'))

        log.debug('Expanding menu "Áreas Especiais"')
        self._wait_element((By.ID, 'ygtvt14'), timeout=5)
        self._driver.find_element(By.ID, 'ygtvt14').click()

        log.debug('Expanding menu "Unidades de conservação"')
        self._wait_element((By.ID, 'ygtvt26'), timeout=5)
        self._driver.find_element(By.ID, 'ygtvt26').click()
        self._wait_element((By.CSS_SELECTOR, 'td[title=ucstodas]'))

        log.debug('Expanding menu "Outras áreas"')
        self._wait_element((By.ID, 'ygtvt27'), timeout=5)
        self._driver.find_element(By.ID, 'ygtvt27').click()
        self._wait_element((By.CSS_SELECTOR, 'td[title=indi2010]'))
        self._wait_element((By.CSS_SELECTOR, 'td[title=cprmsitgeo]'))
        self._wait_element((By.CSS_SELECTOR, 'td[title=florestaspublicas]'))
        self._wait_element((By.CSS_SELECTOR, 'td[title=cprmgeoparques]'))
        self._wait_element((By.CSS_SELECTOR, 'td[title=corredores_ppg7]'))


        # Expandir menu para biomas e vegetação
        # Ambiente físico e biodiversidade
        log.debug('Expanding menu "Ambiente físico e biodiversidade"')
        self._wait_element((By.ID, 'ygtvt15'), timeout=5)
        element = self._driver.find_element(By.XPATH, '//*[@id="ygtvt15"]/a')
        self._actions.move_to_element(element)
        self._actions.click()
        self._actions.perform()

        # Vegetação
        self._wait_element((By.ID, 'ygtvt42'), timeout=5)
        log.debug('Expanding menu "Vegetação"')
        element = self._driver.find_element(By.XPATH, '//*[@id="ygtvt42"]/a')
        self._actions.move_to_element(element)
        self._actions.click()
        self._actions.perform()
        self._wait_element((By.CSS_SELECTOR, 'td[title=vegetacao]'), 5)

        # Expandir menu para biomas para lei da mata atlantica
        log.debug('Expanding menu "Biomas"')
        self._wait_element((By.ID, 'ygtvt23'), timeout=5)
        element = self._driver.find_element(By.XPATH, '//*[@id="ygtvt23"]/a')
        self._actions.move_to_element(element)
        self._actions.click()
        self._actions.perform()
        element.click()

        # Mata atlantica
        self._wait_element((By.ID, 'ygtvt50'), timeout=5)
        log.debug('Expanding menu "Mata Atlântica"')
        element = self._driver.find_element(By.XPATH, '//*[@id="ygtvt50"]/a')
        self._actions.move_to_element(element)
        self._actions.click()
        self._actions.perform()


    def get_conservation_units(self):
        log.debug('Getting "Unidades de conservação" shapefile')
        selector = 'td[title=ucstodas]'
        self._wait_element((By.CSS_SELECTOR, selector))
        
        element = self._driver.find_element(By.CSS_SELECTOR, selector)
        self._actions.move_to_element(element)
        self._actions.click()
        self._actions.perform()
        
        columns = [
            'imported_id',
            'name',
            'category',
            'group',
            'sphere',
            'creation_year',
            'quality',
            'legal_act',
            'last_update',
            'original_name',
            'geometry'
        ]

        df = self._download_shape('unidades_de_conservacao')
        df.rename(columns={
            df.columns[0]: columns[0],
            df.columns[1]: columns[1],
            df.columns[3]: columns[2],
            df.columns[4]: columns[3],
            df.columns[5]: columns[4],
            df.columns[6]: columns[5],
            df.columns[8]: columns[6],
            df.columns[9]: columns[7],
            df.columns[10]: columns[8],
            df.columns[12]: columns[9]
        }, inplace=True)
        
        return df[columns]

    def get_indigenous_land(self):
        log.debug('Getting "Terras indígenas" shapefile')
        selector = 'td[title=indi2010]'
        self._wait_element((By.CSS_SELECTOR, selector))
        
        element = self._driver.find_element(By.CSS_SELECTOR, selector)
        self._actions.move_to_element(element)
        self._actions.click()
        self._actions.perform()
        
        columns = [
            'imported_id',
            'location',
            'population',
            'groups',
            'state',
            'city',
            'stage',
            'status',
            'title',
            'document',
            'date',
            'extension',
            'area_name',
            'geometry'
        ]

        df = self._download_shape('terras_indigenas', 'cp437')
        df.rename(columns={
            df.columns[0]: columns[0],
            df.columns[6]: columns[1],
            df.columns[8]: columns[2],
            df.columns[9]: columns[3],
            df.columns[10]: columns[4],
            df.columns[11]: columns[5],
            df.columns[12]: columns[6],
            df.columns[13]: columns[7],
            df.columns[14]: columns[8],
            df.columns[15]: columns[9],
            df.columns[16]: columns[10],
            df.columns[17]: columns[11],
            df.columns[22]: columns[12]
        }, inplace=True)
        
        return df[columns]

    def get_geo_sites(self):
        log.debug('Getting "Sitios geologicos" shapefile')
        selector = 'td[title=cprmsitgeo]'
        self._wait_element((By.CSS_SELECTOR, selector))
        
        element = self._driver.find_element(By.CSS_SELECTOR, selector)
        self._actions.move_to_element(element)
        self._actions.click()
        self._actions.perform()
        
        columns = [
            'imported_id',
            'latitude',
            'longitude',
            'name',
            'state',
            'type',
            'description',
            'geometry'
        ]

        df = self._download_shape('sitios_geologicos')
        df.rename(columns={
            df.columns[0]: columns[0],
            df.columns[2]: columns[1],
            df.columns[3]: columns[2],
            df.columns[5]: columns[3],
            df.columns[6]: columns[4],
            df.columns[7]: columns[5],
            df.columns[9]: columns[6],
        }, inplace=True)
        
        return df[columns]

    def get_florestas_publicas(self):
        log.debug('Getting "Florestas públicas" shapefile')
        selector = 'td[title=florestaspublicas]'
        self._wait_element((By.CSS_SELECTOR, selector))
        
        element = self._driver.find_element(By.CSS_SELECTOR, selector)
        self._actions.move_to_element(element)
        self._actions.click()
        self._actions.perform()
        
        return self._download_shape('florestas_publicas')

    def get_geo_parks(self):
        log.debug('Getting "Parques geologico" shapefile')
        selector = 'td[title=cprmgeoparques]'
        self._driver.find_element(By.CSS_SELECTOR, selector).click()

        columns = [
            'imported_id',
            'name',
            'state',
            'latitude',
            'longitude',
            'type',
            'description',
            'geometry'
        ]

        df = self._download_shape('geoparques')
        df.rename(columns={
            df.columns[0]: columns[0],
            df.columns[1]: columns[1],
            df.columns[2]: columns[2],
            df.columns[3]: columns[3],
            df.columns[4]: columns[4],
            df.columns[5]: columns[5],
            df.columns[6]: columns[6]
        }, inplace=True)
        
        return df[columns]

    def get_corridors(self):
        log.debug('Getting "Corredores" shapefile')
        selector = 'td[title=corredores_ppg7]'
        self._wait_element((By.CSS_SELECTOR, selector))
        element = self._driver.find_element(By.CSS_SELECTOR, selector)
        self._actions.move_to_element(element)
        self._actions.click()
        self._actions.perform()
        columns = ['imported_id', 'name', 'geometry']

        df = self._download_shape('corredores')
        df.rename(columns={
            df.columns[0]: columns[0],
            df.columns[1]: columns[1]
        }, inplace=True)
        
        return df[columns]

    def get_atlantic_forest_law(self):
        log.debug('Getting "Mata atlantica" shapefile')
        selector = 'td[title=mata_atlantica11428]'
        self._wait_element((By.CSS_SELECTOR, selector))
        element = self._driver.find_element(By.CSS_SELECTOR, selector)
        self._actions.move_to_element(element)
        self._actions.click()
        self._actions.perform()

        df = self._download_shape('mata_atlantica11428')
        
        columns = [
            'imported_id_0', 
            'imported_id_1', 
            'name', 
            'geometry'
        ]

        df.rename(columns={
            df.columns[0]: columns[0],
            df.columns[1]: columns[1],
            df.columns[2]: columns[2],
            df.columns[3]: columns[3]
        }, inplace=True)
        
        return df[columns]

    def get_bioma(self):
        log.debug('Getting "Biomas" shapefile')
        selector = 'td[title=bioma]'
        
        element = self._driver.find_element(By.CSS_SELECTOR, selector)
        self._actions.move_to_element(element)
        self._actions.click()
        self._actions.perform()

        df = self._download_shape('bioma')
        
        columns = [
            'ID_0', 
            'name', 
            'ID_2', 
            'geometry'
        ]

        df.rename(columns={
            df.columns[0]: columns[0],
            df.columns[1]: columns[1],
            df.columns[2]: columns[2],
            df.columns[3]: columns[3]
        }, inplace=True)
        
        return df[columns]

    def get_cerrado_vegetation(self):
        log.debug('Getting "Vegetação do cerrado" shapefile')
        selector = 'td[title=vegetacao]'
        self._wait_element((By.CSS_SELECTOR, selector))
        
        element = self._driver.find_element(By.CSS_SELECTOR, selector)
        self._actions.move_to_element(element)
        self._actions.click()
        self._actions.perform()

        df = self._download_shape('vegetacao')
        
        columns = [
            'ID', 
            'NOME', 
            'BIOMA',
            'DESCRICAO',
            'SIGLA',
            'FONTE',
            'geometry'
        ]

        df.rename(columns={
            df.columns[0]: columns[0],
            df.columns[1]: columns[1],
            df.columns[2]: columns[2],
            df.columns[3]: columns[3],
            df.columns[4]: columns[4],
            df.columns[5]: columns[5],
            df.columns[6]: columns[6]
        }, inplace=True)
        
        df = df[df["BIOMA"] == "Cerrado"]
        
        return df[columns]


    def tear_down(self):
        # self._driver.close()
        shutil.rmtree(self._download_dir)

    def _container_close(self):
        xpath = '//*[@id="panellistaarquivos"]/a'
        self._wait_element((By.XPATH, xpath))
        self._driver.find_element(By.XPATH, xpath).click()

    def _wait_element(self, locator: tuple, timeout: int = 60):
        condition = EC.presence_of_element_located(locator)
        WebDriverWait(self._driver, timeout).until(condition)

    def _download_shape(self, shape_name, encoding='utf8'):
        self._wait_element(
            (By.CSS_SELECTOR, '#panellistaarquivos a[href$=shp]')
        )

        shp_file = f'{shape_name}.shp'
        self._download_from_element('a[href$=shp]', shp_file)

        shx_file = f'{shape_name}.shx'
        self._download_from_element('a[href$=shx]', shx_file)

        dbf_file = f'{shape_name}.dbf'
        self._download_from_element('a[href$=dbf]', dbf_file)

        shape = self._extract_shape(shp_file, encoding)

        close_selector = '#panellistaarquivos a.container-close'
        self._driver.find_element(By.CSS_SELECTOR, close_selector).click()

        return shape

    def _download_from_element(self, selector: str, filename: str):
        element = self._driver.find_element(By.CSS_SELECTOR, selector)
        href = element.get_attribute('href')
        path = f'{self._download_dir}{filename}'

        log.debug(f'Downloading {href}')
        success = utils.download_to_file(href, path)

        if not success:
            log.error(f'Failed to download {href}')

    def _extract_shape(self, shp_file: str, encoding: str):
        log.debug(f'Extracting file {shp_file}')
        path = f'{self._download_dir}{shp_file}'

        return geopandas.read_file(path, encoding=encoding)


def _publish(topic, reg):
    payload = reg[1].to_dict()
    payload['geometry'] = mapping(payload['geometry'])
    key = payload['imported_id']

    publisher.publish(topic, payload, key)


def icmbio():
    importer = ICMBioImporter()
    importer.set_up()
    success = 0

    for reg in importer.get_corridors().iterrows():
        try:
            _publish('ICMBIO_CORRIDOR', reg)
            success += 1
        except Exception as e:
            log.error(e)

    for reg in importer.get_geo_sites().iterrows():
        try:
            _publish('ICMBIO_SITE', reg)
            success += 1
        except Exception as e:
            log.error(e)

    for reg in importer.get_conservation_units().iterrows():
        try:
            _publish('ICMBIO_CONSERVATION_UNIT', reg)
            success += 1
        except Exception as e:
            log.error(e)

    for reg in importer.get_indigenous_land().iterrows():
        try:
            _publish('ICMBIO_INDIGENOUS_LAND', reg)
        except Exception as e:
            log.error(e)

    for reg in importer.get_geo_parks().iterrows():
        try:
            _publish('ICMBIO_GEOPARK', reg)
            success += 1
        except Exception as e:
            log.error(e)

    for reg in importer.get_atlantic_forest_law().iterrows():
        try:
            # TODO: topico kafka para lei da mata
            # _publish('ICMBIO_ATLANTIC_FOREST_LAW', reg)
            log.debug(reg)
            success += 1
        except Exception as e:
            log.error(e)

    for reg in importer.get_bioma().iterrows():
        try:
            # TODO: topico kafka para bioma
            # _publish('ICMBIO_ATLANTIC_FOREST_LAW', reg)
            log.debug(reg)
            success += 1
        except Exception as e:
            log.error(e)

    for reg in importer.get_cerrado_vegetation().iterrows():
        try:
            # TODO: topico kafka para bioma
            # _publish('CERRADO VEGETATION', reg)
            log.debug(reg)
            success += 1
        except Exception as e:
            log.error(e)

    importer.tear_down()
    log.debug(f'{success} stored')
