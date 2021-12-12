from rhino3dm._rhino3dm import File3dm, Point3d, Layer, Group, ObjectAttributes, Curve, Polyline, Extrusion
from shapely.geometry import Polygon, LineString, Point
from shapely.ops import orient
from typing import List, Tuple
from random import randint
import os


class RhinoFileWriter:
    def __init__(self, all_elements: list, file_name: str, file_path: str):
        self.all_elements = all_elements
        self.file_name = file_name
        self.file_path = file_path
        self.doc = File3dm()
        # 寫入的rhino版本
        self.WRITE_VERSION = 6

    def _add_layer_to_file(self):
        """
        将all_elements中的layer转变成图层
        :param :
        :return:
        """
        # 取出所有图层
        layer_names = list(set(map(lambda each: each.layer, self.all_elements)))
        if len(layer_names) > 0:
            for name in layer_names:
                cur_layer = Layer()
                cur_layer.Name = name
                cur_layer.Visible = True
                cur_layer.Color = (randint(0, 255), randint(0, 255), randint(0, 255), 255)
                self.doc.Layers.Add(cur_layer)
        else:
            cur_layer = Layer()
            cur_layer.Name = '0'
            cur_layer.Visible = True
            cur_layer.Color = (randint(0, 255), randint(0, 255), randint(0, 255), 255)
            self.doc.Layers.Add(cur_layer)

    def _transform_elements_to_rhino_objects(self, element) -> Tuple[List[Point3d], List[List[Point3d]], List[Polyline]]:
        points = []
        lines = []
        polylines = []

        geometry = element.geometry
        # 轉換點
        if isinstance(geometry, Point):
            point_object = Point3d(geometry.x, geometry.y, 0.)
            points.append(point_object)
        # 轉換短的多段綫
        elif isinstance(geometry, LineString) and len(list(geometry.coords)) == 2:
            short_line_points = [Point3d(coord[0], coord[1], 0.) for coord in list(geometry.coords)]
            lines.append(short_line_points)
        # 轉換多段綫
        elif isinstance(geometry, LineString) and len(list(geometry.coords)) > 2:
            line_points = [Point3d(coord[0], coord[1], 0.) for coord in list(geometry.coords)]
            line_object = Polyline(line_points)
            polylines.append(line_object)
        # 轉換多邊形
        elif isinstance(geometry, Polygon):
            polygon_points = [Point3d(coord[0], coord[1], 0.) for coord in list(orient(geometry).exterior.coords)]
            polygon_object = Polyline(polygon_points)
            polylines.append(polygon_object)

        return points, lines, polylines

    def _data_structure_processor(self):
        """
        转化data model为rhino内部格式
        :param data_model:
        :return:
        """
        # 添加图层
        self._add_layer_to_file()
        # 图层名
        layer_index = [each.Index for each in self.doc.Layers]
        layer_name = [each.Name for each in self.doc.Layers]
        layer_info = list(map(lambda index, name: (index, name), layer_index, layer_name))
        # 转换对象，匹配图层并写入到该3dm文件中
        for element in self.all_elements:
            layer_index = [item[0] for item in layer_info if item[1] == element.layer]
            # 转换物件
            id_list = []
            attribute = ObjectAttributes()
            points, lines, polylines = self._transform_elements_to_rhino_objects(element=element)
            if points:
                for point in points:
                    id = self.doc.Objects.AddPoint(point)
                    id_list.append(id)
            if lines:
                for line in lines:
                    id = self.doc.Objects.AddLine(line[0], line[1])
                    id_list.append(id)
            if polylines:
                for polyline in polylines:
                    id = self.doc.Objects.AddPolyline(polyline, attribute)
                    id_list.append(id)
            # 匹配物件信息
            for object_id in id_list:
                cur_object = self.doc.Objects.FindId(str(object_id))
                cur_object.Attributes.LayerIndex = layer_index[0]

    def write_3dm_file(self):
        """
        根据输入的数据类型选择处理方式
        :param data_model:
        :return:
        """
        self._data_structure_processor()
        save_path = os.path.join(os.path.abspath(self.file_path), self.file_name)
        self.doc.Write(save_path, version=self.WRITE_VERSION)