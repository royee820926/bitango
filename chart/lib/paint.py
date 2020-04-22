# encoding=utf-8

import os
from django.conf import settings
from pyecharts import options as opts
from pyecharts.charts import Kline

class Paint(object):

    @classmethod
    def kline(cls, result, file_name, title="标题", is_df=False):
        """
        绘制K线
        :param result: 数据
        :param file_name: 保存到指定文件
        :param title: 标题
        :param is_df: 是否是DataFrame类型数据
        :return:
        """
        data = []
        time_list = []
        if is_df:
            result = result.values
            for item in result:
                # 数据
                data.append([
                    float(item[1]),     # open
                    float(item[4]),     # close
                    float(item[3]),     # low
                    float(item[2]),     # high
                ])
                # 时间
                time_list.append(str(item[0]))
        else:
            for item in result:
                # 数据
                data.append([
                    float(item['open']),
                    float(item['close']),
                    float(item['low']),
                    float(item['high']),
                ])
                # 时间
                time_list.append(str(item['candle_begin_time']))

        kline = (
            Kline()
                .add_xaxis(time_list)
                .add_yaxis("K线", data)
                .set_global_opts(
                xaxis_opts=opts.AxisOpts(is_scale=True),
                yaxis_opts=opts.AxisOpts(
                    is_scale=True,
                    splitarea_opts=opts.SplitAreaOpts(
                        is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                    ),
                ),
                datazoom_opts=[opts.DataZoomOpts()],
                title_opts=opts.TitleOpts(title=title),
            )
        )

        kline.render(path=cls.get_save_path(file_name))

    @classmethod
    def get_save_path(cls, file_name):
        """
        获取绘制图像路径，和file_name拼接
        :param file_name:
        :return:
        """
        return os.path.join(settings.BASE_DIR, 'templates', 'chart', 'paint', file_name)
