from descartes import PolygonPatch
import matplotlib.pyplot as plt
from shapely.geometry import GeometryCollection, MultiPolygon, LineString, MultiLineString, Point, Polygon
import os

class MatplotlibRender:

    def __init__(self):
        self.ax = None
        self._basic_config()
        self.font_config = {
            'color':'black',
            'size':10,
        }
        self.fig = None

    def _basic_config(self):
        figsize = ((960/540)*10, 10)
        # here for the main settings
        fig = plt.figure(1, figsize=figsize, dpi=120)  # set the size and Dpi of the plot
        ax = plt.subplot2grid((1, 1), (0, 0), colspan=1, rowspan=1)  # layout setting of the whole plot
        self.ax = ax
        plt.axis('off')  # display the axis or not
        plt.gca().set_aspect('equal', adjustable='box')  # keep the right scale of the plot
        self.fig = fig

    def _plot_text(self, position, text):
        """
        render text english only
        :param position:
        :param text:
        :return:
        """
        plt.text(position[0], position[1], text, fontdict=self.font_config)

    def _plot_point(self, obj:Point, color:str, zorder:int):
        """
        render point object
        :param obj:
        :return:
        """
        x, y = obj.xy
        self.ax.plot(x, y,'o', color=color, zorder=zorder)

    def _plot_line(self, obj:LineString, color:str, zorder:int, line_style:str, line_width:float, opacity:float):
        """
        render line object
        :param obj:
        :param color:
        :param zorder:
        :param line_style:
        :param line_width:
        :param opacity:
        :return:
        """
        x, y = obj.xy
        self.ax.plot(x, y,
                     color=color,
                     alpha=opacity,
                     linestyle=line_style,
                     linewidth=line_width,
                     solid_capstyle='projecting',
                     zorder=zorder)

    def _plot_polygon(self, obj:Polygon, edge_color:str,face_color:str, zorder:int, line_width:float, opacity:float):
        """
        render line object
        :param obj:
        :param color:
        :param zorder:
        :param line_style:
        :param line_width:
        :param opacity:
        :return:
        """
        patch = PolygonPatch(obj, alpha=opacity,
                             facecolor=face_color,
                             edgecolor=edge_color,
                             linewidth=line_width,
                             zorder=zorder)
        self.ax.add_patch(patch)

    def render(self, data):
        """
        render some data
        :param data:
        :return:
        """
        for each in data:
            if isinstance(each.geometry, LineString):
                self._plot_line(obj=each.geometry, color=each.line_color, line_style=each.line_style, line_width=each.line_width, opacity=each.opacity, zorder=each.zorder)
            elif isinstance(each.geometry, Polygon):
                self._plot_polygon(obj=each.geometry, line_width=each.line_width, opacity=each.opacity, zorder=each.zorder, edge_color=each.line_color, face_color=each.face_color)
        plt.show()

    def export_img(self, data, file_path, file_name):
        """
        export a img
        :param data:
        :param file_path:
        :param file_name:
        :return:
        """
        save_path = os.path.join(os.path.abspath(file_path), file_name)
        for each in data:
            if isinstance(each.geometry, LineString):
                self._plot_line(obj=each.geometry, color=each.line_color, line_style=each.line_style,
                                line_width=each.line_width, opacity=each.opacity, zorder=each.zorder)
            elif isinstance(each.geometry, Polygon):
                self._plot_polygon(obj=each.geometry, line_width=each.line_width, opacity=each.opacity,
                                   zorder=each.zorder, edge_color=each.line_color, face_color=each.face_color)
        plt.savefig(save_path, bbox_inches='tight')
        print(f'成功保存图片到{save_path}')
        return self.fig

