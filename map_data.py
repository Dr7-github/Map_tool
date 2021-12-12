import osmnx as ox
from Data_structure import MapElement
import pandas as pd

import matplotlib.colors as mcl

def get_map_data(lat,lng,dist,layers,render_settings):
    '''
    使用经纬度和材质球获取地图信息
    '''
    all_map_datas = []
    all_map_element = []
    for idx,name in enumerate(layers):
        print(name)
        cur_layer_data = ox.geometries_from_point(center_point=(lat,lng),tags={name:True},dist=dist)
        cur_layer_geometry = cur_layer_data['geometry'].tolist()
        for geometry in cur_layer_geometry:
            cur_element = MapElement(geometry=geometry)
            cur_element.layer = render_settings[idx]['layer']
            cur_element.line_color = render_settings[idx]['line_color']
            cur_element.line_style = render_settings[idx]['line_style']
            cur_element.line_width = render_settings[idx]['line_width']
            cur_element.face_color = render_settings[idx]['face_color']
            cur_element.opacity = render_settings[idx]['opacity']
            cur_element.zorder = render_settings[idx]['zorder']
            all_map_element.append(cur_element)
        all_map_datas.append(cur_layer_data)

    return all_map_datas,all_map_element

def get_poi(element):
    lat = []
    lon = []
    for item in element['geometry']:
        if item.type == 'Point':
            lat.append(item.y)
            lon.append(item.x)
    df = pd.DataFrame({
        'lat':lat,
        'lon':lon
    })
    return df

def get_land_use_data(land_use_data):
    all_map_land = []
    layer = land_use_data['landuse'].unique()
    color = [y for x,y in mcl.cnames.items()]
    print(color)
    # geometry = land_use_data['geometry'].unique()
    for idx, name in enumerate(layer):
        df = land_use_data[land_use_data['landuse']==name]
        cur_layer_geometry = df['geometry'].tolist()
        for geometry in cur_layer_geometry:
            cur_land = MapElement(geometry=geometry)
            cur_land.layer = name
            cur_land.line_color = '#FFFFFF'
            cur_land.line_style = '-'
            cur_land.line_width = 1
            cur_land.face_color = color[idx]
            cur_land.opacity = 1
            cur_land.zorder = idx
            all_map_land.append(cur_land)

    return all_map_land
