import random

from example.commons import  Faker
from pyecharts import options as opts
from pyecharts.charts import HeatMap
from pyecharts.globals import ThemeType

def heatmap_base() -> HeatMap:
    value = [[i, j, random.randint(0, 60)] for i in range(30) for j in range(7)]
    c = (
        HeatMap(init_opts=opts.InitOpts(theme=ThemeType.CHALK))
        .add_xaxis(Faker.clock)
        .add_yaxis("series0", Faker.week, value)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="HeatMap-基本示例"),
            visualmap_opts=opts.VisualMapOpts(),
        )
    )
    return c
heatmap_base().render('rili.html')