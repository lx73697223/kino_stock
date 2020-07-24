
import talib
import pandas
from pyecharts import options
from pyecharts.charts import Line, Kline, Bar, Grid

from com.kino.stock.configs.local_config import load_local_config
from com.kino.stock.common_utils import time_utils
from com.kino.stock.repository.dao import stock_bar_dao

pandas.set_option('expand_frame_repr', False)   # 打印时不要折叠列
pandas.set_option('display.max_rows', 200)      # 打印最多200行数据


if __name__ == '__main__':
    load_local_config()

    ts_codes = ["600519.SH"]
    start_date = time_utils.delta_and_format_time(months=-12, _format="%Y%m%d")
    end_date = time_utils.delta_and_format_time(_format="%Y%m%d")
    cci_thresh = 50

    bar_data = stock_bar_dao.get_stock_bar(ts_codes, start_date, end_date, freq="D", adj="qfq", order_by="trade_date")
    print(bar_data)

    # 计算并画出cci
    cci = talib.CCI(bar_data['high'].values, bar_data['low'].values, bar_data['close'].values, timeperiod=14)
    print(cci)

    # 简单择时策略，当cci>50则持仓，当cci<50则空仓
    position = [cci_thresh if idx >= cci_thresh else 0 for idx in cci]
    print(position)

    # 绘制cci折线图
    cci_line = Line()
    cci_line.add_xaxis(bar_data['trade_date'])
    cci_line.add_yaxis(
        'cci', cci,
        # is_connect_nones=True,
        # markpoint_opts=options.MarkPointOpts(data=[
            # options.MarkPointItem(type_='min'), options.MarkPointItem(type_='max'),
            # options.MarkLineItem(type_='average')
        # ])
    )
    cci_line.set_global_opts(
        tooltip_opts=options.TooltipOpts(is_show=False),
        title_opts=options.TitleOpts(title='日K-CCI'),
        # xaxis_opts=options.AxisOpts(type_='value'),
        # yaxis_opts=options.AxisOpts(name='price', type_='value', is_scale=True,
        #                             splitline_opts=options.SplitLineOpts(is_show=True))
    )
    cci_line.render('/userdata/output_data/cci.html')

    # 绘制持仓
    bar = Bar()
    bar.add_xaxis(bar_data['trade_date'])
    bar.add_yaxis('持仓', position)
    bar.set_global_opts(
        title_opts=options.TitleOpts(title="持仓", subtitle="Bar"),
        datazoom_opts=options.DataZoomOpts()
    )
    bar.render('/userdata/output_data/bar.html')

    # 将持仓和cci重叠在一个图中
    cci_overlap = bar.overlap(cci_line)
    cci_overlap.render('/userdata/output_data/cci_bar.html')

    # 画出K线图
    price = [[open, close, lowest, highest] for open, close, lowest, highest in
             zip(bar_data['open'], bar_data['close'], bar_data['low'], bar_data['high'])]
    kline = Kline()
    kline.add_xaxis(bar_data['trade_date'])
    kline.add_yaxis("贵州茅台", price)
    kline.set_global_opts(
        title_opts=options.TitleOpts(title="贵州茅台-Kline"),
        datazoom_opts=[options.DataZoomOpts()],
        xaxis_opts=options.AxisOpts(is_scale=True),
        yaxis_opts=options.AxisOpts(
            splitarea_opts=options.SplitAreaOpts(is_show=True, areastyle_opts=options.AreaStyleOpts(opacity=1)),
            is_scale=True
        )
    )
    kline.render('/userdata/output_data/kline.html')

    # 将cci折线图和K线图合并到一张图表中
    grid = Grid()
    grid.add(kline, grid_opts=options.GridOpts(), is_control_axis_index=True)
    grid.add(cci_overlap, grid_opts=options.GridOpts(), is_control_axis_index=True)
    grid.render('/userdata/output_data/kline-cci-pos.html')
    print(grid)
