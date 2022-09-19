import pandas as pd
import plotly.express as px

def plotSPI(df,  panel_id, Citem, fitem, no , rang, xysize):
    # 定義顏色空間的相關色彩
    color1 = [ "rgb(255, 0, 0)"    ,   "rgb(255, 255, 96)",   "rgb(255, 255, 160)",
               "rgb(0, 0, 0)"      ,
               "rgb(160, 255, 255)",   "rgb(96, 255, 255)",   "rgb(0, 0, 255)"    , ]
    #
    Pitem = Citem
    title0 = Pitem + f': SPI info of <br> {panel_id} '
    fig=px.scatter(df, x='Center X', y='Center Y', title=title0, 
                   color=Pitem, color_continuous_scale= color1 , 
                   height=xysize[0] ,width=xysize[1],
                   #facet_col=fitem, facet_col_wrap=no ,
                   range_color= (rang[0], rang[1])
                    )
    #
    # 主要是把四分之一圖給畫上去，大小由 size 的變數來決定
    size=432000
    fig.add_shape(dict(type="path",path= ellipse_arc(a=size, b=size, start_angle=0.0, end_angle=np.pi/2, N=60),
                 line_color= "Red"), row="all", col='all')
    #
    # 主要是把 Segment 外框給畫出來。
    SegmentPath1='M 0,0 L 432050,0 L 432050,196761 L 223289,432050 L 0,432050 L 0,0'
    fig.add_shape(dict(type="path",path= SegmentPath1,line_color= "Green"), row="all", col='all')
    # 設計 mark size 大小和， 和圖形的背景資料
    fig.update_traces(marker_size= 2)
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',})    
    #
    #fig.write_image(f"/content/{Citem}.jpeg")
    return fig
