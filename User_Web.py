import streamlit as st
from map_data import get_map_data,get_poi,get_land_use_data

from matplot_render import MatplotlibRender
import  matplotlib
matplotlib.use('TkAgg')
from map_data import MapElement

from PIL import Image

import pydeck as pdk

from rhino_file_writer import RhinoFileWriter as rfw


#title
st.title('Map Collection')
st.write('Designed by Zacky Zhang')

#input
st.header('INPUT')
st.write('Data from OpenStreetMap')
start_col1,start_col2,start_col3 = st.columns([1,1,1])
with start_col1:
    lat = st.text_input('Lat')
with start_col2:
    lng = st.text_input('Lng')
with start_col3:
    dist = st.number_input('Scope',min_value=500,max_value=2000,step=100)

#information
building = st.multiselect('Building Layer',['building', 'amenity', 'landuse', 'office','shop','spot','public_transport'] )
road= st.multiselect('Road Layer',['highway','railway'])
land = st.multiselect('land Layer',['leisure','natural', 'water', 'waterway', 'tourism'] )

all_options = building+road+land

#sidebar,color edit
st.sidebar.title('Map Style Editor')

all_render_style = []

for idx,each in enumerate(all_options):
    each_render_style = {}
    st.sidebar.header('{}'.format(each))
    each_render_style['layer'] = each
    each_render_style['line_color'] = st.sidebar.color_picker('Line Color',value='#D27D7D',key=idx)
    each_render_style['line_width'] = st.sidebar.slider('Line Width',value=1,key=idx)
    each_render_style['line_style'] = st.sidebar.text_input('Line Style', value='-',key=idx)
    each_render_style['face_color'] = st.sidebar.color_picker('Face Color',value='#6CB0CE',key=idx)
    each_render_style['opacity'] = st.sidebar.slider('Opacity', key=idx,value=100,max_value=100,step=1)/100
    each_render_style['zorder'] = st.sidebar.slider('Zorder', key=idx,max_value=len(all_options))
    all_render_style.append(each_render_style)

print(all_options)

if st.button('GET'):
    all_map,all_element = get_map_data(lat=float(lat),lng=float(lng),layers=all_options,dist=dist,render_settings=all_render_style)
    print(f'成功爬取数据，正在mapping.......')
    render = MatplotlibRender()
    fig = render.export_img(data=all_element, file_path='Image_path', file_name='res.jpg')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.caption('分層地圖信息：')
    st.pyplot(fig)

    #analyse layers
    for ix,item in enumerate(all_options):
        if item == 'amenity':
            amenity_poi_df = get_poi(all_map[ix])
            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v9',
                initial_view_state=pdk.ViewState(
                    latitude=float(lat),
                    longitude=float(lng),
                    zoom=15,
                    pitch=50,
                ),
                layers=[
                    pdk.Layer(
                        'HexagonLayer',
                        data=amenity_poi_df,
                        get_position='[lon, lat]',
                        radius=20,
                        elevation_scale=4,
                        elevation_range=[0, 100],
                        pickable=True,
                        extruded=True,
                    )
                ],
            ))
        else:
            print(item)
            st.bar_chart(all_map[ix][item].value_counts())
            if item == 'landuse':
                land_use_data = get_land_use_data(all_map[ix])
                print(land_use_data[0].face_color)
                render_l = MatplotlibRender()
                fig_l = render_l.export_img(land_use_data, file_path='Image_path', file_name='lan.jpg')
                st.pyplot(fig_l)

    st.caption('主要道路')
    if 'highway' in all_options:
        idx = all_options.index('highway')
        data_type = list(set([each for each in all_map[idx]['highway'].tolist()]))
        print(data_type)
        highway_data = [[all_map[idx]['highway'].tolist()[i], all_map[idx]['geometry'].tolist()[i]] for i in
                        range(len(all_map[idx]['highway'].tolist()))]
        valid_road_type = ['primary_link', 'motorway_link', 'secondary', 'motorway_junction', 'motorway',
                           'secondary_link', 'tertiary', 'tertiary_link']
        main_road_data = list(filter(lambda each: each[0] in valid_road_type, highway_data))
        # 求解traffic_signals的覆盖范围
        for each in main_road_data:
            # cur_geo = each[1].buffer(0.0005) if isinstance(each[1], Point) else each[1]
            cur_element = MapElement(geometry=each[1])
            cur_element.layer = 'main_road'
            cur_element.line_color = '#FF1744'
            cur_element.line_style = '-'
            cur_element.line_width = 5
            cur_element.face_color = '#ffffff'
            cur_element.opacity = 0.7
            cur_element.zorder = 20
            all_element.append(cur_element)

        # analyse layers
        all_map_elements = list(
            filter(lambda each: each.layer == 'building' or each.layer == 'main_road', all_element))
        fig = render.export_img(data=all_map_elements, file_path='Image_path', file_name='bus_stop_analysis.jpg')
        image = Image.open('Image_path/bus_stop_analysis.jpg')
        st.image(image, caption='#traffic_signals analysis')
        st.header(" ")

    # modle_file_name = 'test.3dm'
    # modle_file_path = 'Modle'
    # rfw(all_element,modle_file_name,modle_file_path).write_3dm_file()

