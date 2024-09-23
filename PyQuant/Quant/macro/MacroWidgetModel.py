#
import json
from PyQt5.QtCore import QUrl, QFileInfo
from pyecharts import options as opts
from pyecharts.charts import Geo


world_data = None
with open('./data/ne_110m_admin_0_countries.json', 'r', encoding='utf-8') as fr:
    world_data = json.load(fr)

class MacroWidgetModel():

    def createWorldChart(self):
        world_geo = (Geo().add_js_funcs("echarts.registerMap('world00',{});".format(world_data))
                     .add_schema(maptype='world00', name_property='NAME')
                     .set_global_opts(title_opts=opts.TitleOpts(title="全球"))
                     )
        world_geo.render("./html/world.html")
        temp_url = QUrl("file://" + QFileInfo("html/world.html").absoluteFilePath())
        return  temp_url