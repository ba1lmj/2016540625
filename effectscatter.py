from  pyecharts import Polar
radius =['周一', '周二', '周三', '周四', '周五', '周六', '周日']
polar =Polar("极坐标系-堆叠柱状图示例", width=1200, height=600)
polar.add("a", [1, 2, 3, 4, 3, 5, 1], radius_data=radius, type='barAngle', is_stack=True)
polar.add("b", [2, 4, 6, 1, 2, 3, 1], radius_data=radius, type='barAngle', is_stack=True)
polar.add("c", [1, 2, 3, 4, 1, 2, 5], radius_data=radius, type='barAngle', is_stack=True)
polar.show_config()
polar.render()