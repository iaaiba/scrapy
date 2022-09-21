import dotenv
import os

dotenv.load_dotenv('.env')


class Config:
    MONGO_HOST = os.environ['MONGO_HOST']
    MONGO_PORT = int(os.environ['MONGO_PORT'])
    MONGO_USER = os.environ['MONGO_USER']
    MONGO_PASSWORD = os.environ['MONGO_PASSWORD']
    MONGO_DB = os.environ['MONGO_DB']
    
    KAFKA_BROKER = os.environ['KAFKA_BROKER']
    
    MAX_WORKERS = os.getenv('MAX_WORKERS', 1)
    MAX_MISFIRE = int(os.getenv('MAX_MISFIRE', 3600))
    
    WEATHER_API = os.environ['WEATHER_API']
    
    ARCGIS_USER = os.environ['ARCGIS_USER']
    ARCGIS_PASSWORD = os.environ['ARCGIS_PASSWORD']
    
    SEIA_USER = os.environ['SEIA_USER']
    SEIA_PASSWORD = os.environ['SEIA_PASSWORD']

    SIMA_USER = os.environ['SIMA_USER']
    SIMA_PASSWORD = os.environ['SIMA_PASSWORD']

    HYDROGRAPHY_VECTORS = os.environ['HYDROGRAPHY_VECTORS']
    HYDROGRAPHY_LIMIT_N1 = os.environ['HYDROGRAPHY_LIMIT_N1']
    HYDROGRAPHY_LIMIT_N2 = os.environ['HYDROGRAPHY_LIMIT_N2']
    HYDROGRAPHY_LIMIT_N4 = os.environ['HYDROGRAPHY_LIMIT_N4']
    HYDROGRAPHY_LIMIT_N5 = os.environ['HYDROGRAPHY_LIMIT_N5']
    HYDROGRAPHY_QMLD = os.environ['HYDROGRAPHY_QMLD']
    HYDROGRAPHY_Q90 = os.environ['HYDROGRAPHY_Q90']
    HYDROGRAPHY_WATER_AVAILABILITY = os.environ['HYDROGRAPHY_WATER_AVAILABILITY']
    HYDROGRAPHY_WATER_SAFETY_INDEX = os.environ['HYDROGRAPHY_WATER_SAFETY_INDEX']
    HYDROGRAPHY_WATER_BODIES = os.environ['HYDROGRAPHY_WATER_BODIES']
    HYDROGRAPHY_SAO_FRANCISCO_MICRO_BASINS = os.environ['HYDROGRAPHY_SAO_FRANCISCO_MICRO_BASINS']
    HYDROGRAPHY_SAO_FRANCISCO_BASINS = os.environ['HYDROGRAPHY_SAO_FRANCISCO_BASINS']
    HYDROGRAPHY_AQUIFER = os.environ['HYDROGRAPHY_AQUIFER']
    HYDROGRAPHY_IRRIGATED_AREAS = os.environ['HYDROGRAPHY_IRRIGATED_AREAS']
    HYDROGRAPHY_CENTER_PIVOTS = os.environ['HYDROGRAPHY_CENTER_PIVOTS']
    HYDROGRAPHY_CARINHANHA_BASIN = os.environ['HYDROGRAPHY_CARINHANHA_BASIN']
    HYDROGRAPHY_CORRENTE_BASIN = os.environ['HYDROGRAPHY_CORRENTE_BASIN']
    
    RISK_FIRE = os.environ['RISK_FIRE']
