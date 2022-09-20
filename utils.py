import pandas as pd
import plotly.express as px
import numpy as np

def read_SPI_file(data_file):
    df = pd.read_csv(data_file, skiprows=10, engine='c', sep=",", compression="zip", low_memory=False, encoding='ISO-8859-1',encoding_errors='ignore')

    spi_items = ['Layout No.', 'Pin No.' , 'Pad No.' , 'Area[um2]' , 'Area[%]' , 'X shift' , 'Y shift', 'No solder' , 'Center X', 'Center Y']
    df1 = df.loc[:,spi_items]
    df1['Pin No.'] = df1['Pin No.'].astype('int')
    df1['Layout No.'] = df1['Layout No.'].astype('int32')
    df1.sort_values(['Layout No.', 'Pin No.'], inplace = True )
    df1.reset_index(drop=True)
    del df
    return df1

def read_COB_file(filename):
    #
    columns=['Time', 'Onload Wafer ID', 'Column', 'Row', 'Panel_ID', 'Cluster' , 'OutputX', 'OutputY', 'OutputID',\
             'Head', 'Postbond X' , 'Postbond Y' , 'Postbond T', 'Device']
    #
    df = pd.read_csv(filename, header=None, names=columns, engine='c')
    start_index=df.index[df[columns[0]]==columns[0]][0]
    df.drop(labels=range(start_index+1), axis=0, inplace=True)
    df.reset_index(inplace = True)
    df.drop('index',axis=1,inplace=True)
    #
    # 新增 Recipe Column for different Tx/Rx Die position design
    Device_name=['13-Kymeta_R_S0', '14-Kymeta_T_S0', '15-Kymeta_T_S180','16-Kymeta_R_S180']
    nC=['1','2','3','4']
    #
    df['Recipe'] = 'NaN'
    df.loc[(df.Device == Device_name[0]) & (df.Cluster == nC[0]), 'Recipe'] = 'R0_S0'
    df.loc[(df.Device == Device_name[0]) & (df.Cluster == nC[1]), 'Recipe'] = 'R90_S0'
    df.loc[(df.Device == Device_name[0]) & (df.Cluster == nC[2]), 'Recipe'] = 'R180_S0'
    df.loc[(df.Device == Device_name[0]) & (df.Cluster == nC[3]), 'Recipe'] = 'R270_S0'
    df.loc[(df.Device == Device_name[1]) & (df.Cluster == nC[0]), 'Recipe'] = 'T0_S0'
    df.loc[(df.Device == Device_name[1]) & (df.Cluster == nC[1]), 'Recipe'] = 'T90_S0'
    df.loc[(df.Device == Device_name[1]) & (df.Cluster == nC[2]), 'Recipe'] = 'T180_S0'
    df.loc[(df.Device == Device_name[1]) & (df.Cluster == nC[3]), 'Recipe'] = 'T270_S0'
    df.loc[(df.Device == Device_name[2]) & (df.Cluster == nC[0]), 'Recipe'] = 'R0_S180'
    df.loc[(df.Device == Device_name[2]) & (df.Cluster == nC[1]), 'Recipe'] = 'R90_S180'
    df.loc[(df.Device == Device_name[3]) & (df.Cluster == nC[0]), 'Recipe'] = 'T0_S180'
    df.loc[(df.Device == Device_name[3]) & (df.Cluster == nC[1]), 'Recipe'] = 'T90_S180'
    #
    df['OutputX'] = pd.to_numeric(df['OutputX'], errors = 'coerce')
    df['OutputY'] = pd.to_numeric(df['OutputY'], errors = 'coerce')
    df['Postbond X'] = pd.to_numeric(df['Postbond X'], errors = 'coerce')
    df['Postbond Y'] = pd.to_numeric(df['Postbond Y'], errors = 'coerce')
    # 相關座標位置的調，讓 SPI and DB 的座標系統是相同
    df["OutputX"].mask(df["Device"] == Device_name[0], -df["OutputX"] + 195.0, inplace=True)
    df["OutputY"].mask(df["Device"] == Device_name[0], -df["OutputY"] + 415.0, inplace=True)
    df["OutputX"].mask(df["Device"] == Device_name[1], -df["OutputX"] + 195.0, inplace=True)
    df["OutputY"].mask(df["Device"] == Device_name[1], -df["OutputY"] + 415.0, inplace=True)
    df["OutputX"].mask(df["Device"] == Device_name[2], df["OutputX"] + 195.0, inplace=True)
    df["OutputY"].mask(df["Device"] == Device_name[2], df["OutputY"] + 415.0, inplace=True)
    df["OutputX"].mask(df["Device"] == Device_name[3], df["OutputX"] + 195.0, inplace=True)
    df["OutputY"].mask(df["Device"] == Device_name[3], df["OutputY"] + 415.0, inplace=True)
    #
    df['Postbond X'] = pd.to_numeric(df['Postbond X'], errors = 'coerce')
    df['Postbond Y'] = pd.to_numeric(df['Postbond Y'], errors = 'coerce')
    df['Postbond T'] = pd.to_numeric(df['Postbond T'], errors = 'coerce')
    df.loc[df['Postbond X']>1000, ['Postbond X','Postbond Y','Postbond T']]= np.nan
    # 新增 Postbond 的絕對距離
    tmp=( df['Postbond X']**2 + df['Postbond Y']**2 )**0.5
    df.insert(loc=13, column= 'Postbond R', value=tmp)
    #
    return df

def ellipse_arc(x_center=0, y_center=0, a=1, b =1, start_angle=0, end_angle=2*np.pi, N=100, closed= False):
    t = np.linspace(start_angle, end_angle, N)
    x = x_center + a*np.cos(t)
    y = y_center + b*np.sin(t)
    path = f'M {x[0]}, {y[0]}'
    for k in range(1, len(t)):
        path += f'L{x[k]}, {y[k]}'
    if closed:
        path += ' Z'
    return path

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

def plotDB(df, panel_id, Citem, fitem, no, xysize):
    Pitem =  'Postbond ' + Citem
    title0 = Pitem + ': COB info of ' + panel_id
    # 定義顏色空間的相關色彩
    color1 = [ "rgb(255, 0, 0)"    ,   "rgb(255, 255, 96)",   "rgb(255, 255, 160)",
               "rgb(0, 0, 0)"      ,
               "rgb(160, 255, 255)",   "rgb(96, 255, 255)",   "rgb(0, 0, 255)"    , ]
    #
    fig=px.scatter(df, x='OutputX', y='OutputY', color=Pitem, color_continuous_scale=color1 ,
                   title=title0, height=xysize[0] ,width=xysize[1], 
                   facet_col=fitem, facet_col_wrap=no ,
                   range_color= (-15,15),hover_data=["Head", 'Recipe']             )
    #
    # 主要是把四分之一圖給畫上去，大小由 size 的變數來決定
    size=412.3
    fig.add_shape(dict(type="path",path= ellipse_arc(a=size, b=size, start_angle=0.0, end_angle=np.pi/2, N=60),
                 line_color= "Red"), row="all", col='all')
    #
    # 主要是把 Segment 外框給畫出來。
    SegmentPath='M 0,0 L 420.050,0 L 420.050,196.761 L 223.289,420.050 L 0,420.050 L 0,0'
    fig.add_shape(dict(type="path",path= SegmentPath,line_color= "Green"), row="all", col='all')
    # 
    # 設計 mark size 大小和， 和圖形的背景資料
    fig.update_traces(marker_size= 4)
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',})    
    return fig
