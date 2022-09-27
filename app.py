from PIL import Image
import streamlit as st
import pandas as pd
import plotly.express as px
#from zipfile import ZipFile
import numpy as np
from utils import read_SPI_file, plotSPI, read_db_zip,  plotDB

st.set_page_config(page_title = "Plot Map!" ,page_icon="random" ,layout="wide", initial_sidebar_state="collapsed")
st.sidebar.markdown("# Please Select the Items:")

def main():
	#menu = ["SPI","DB","AOI"]
	#choice = st.sidebar.selectbox("Menu(Only SPI/DB is OK!)",menu)
	st.title(f"# Plot XY Map for SPI/DB information！")
	mcol1, mcol2, mcol3 = st.columns([5,0.1,5])
	#if choice == "SPI":
	with mcol1:
		#
		df_spi = None
		with st.form("spi-form", clear_on_submit=True):
		#	tcol1, tcol2, tcol3 = st.columns([3,1,5])
		#	with tcol1:
			data_file = st.file_uploader(r"Upload *.csv.zip", type=["zip"])
			submitted = st.form_submit_button("UPLOAD!")

			if submitted and data_file is not None:
				st.write("UPLOADED!")
		#			with tcol3:
				spi_file_details = rf"filename":{data_file.name},\n filetype:{data_file.type},\n filesize:{data_file.size}"
				#st.write(file_details)
				st.info(spi_file_details, icon="i")
				df_spi = read_SPI_file(data_file)
	with mcol3:
		df_db = None
		with st.form("db-form", clear_on_submit=True):
			#db_col1, db_col2, db_col3 = st.columns([3,1,5])
			#with db_col1:
			db_zip_file = st.file_uploader(r"Upload *.csv.zip", type=["zip"])
			submitted_db = st.form_submit_button("UPLOAD!")

			if submitted_db and db_zip_file is not None:
				st.write("UPLOADED!")
			#		with db_col3:
				db_file_details = rf"filename:{db_zip_file.name},\n filetype:{db_zip_file.type},\n filesize:{db_zip_file.size}"
				st.info(db_file_details, icon="i")
				#st.write(file_details)
				df_db = read_db_zip(db_zip_file)
#
	gcol1, gcol2, gcol3 = st.columns([5,0.1,5])
	with gcol1:
		#tab1, tab2 = st.tabs(["XY Map", "Histogram"])
		#if data_file is not None:
		if submitted and df_spi is not None:		
			spi_check=['Area[um2]', 'Area[%]',  'X shift', 'Y shift' ]

			#with tab1:
			panel_id = spi_data_file.name
			fitem = 'Pin No.'
			xysize=[450,450]			
			#	col1, col2, col3, col4, col5  = st.columns([9,1,9,1,9])
			#	with col3:
			valueX = st.slider('Select a range of X shift',-40, 40, (-25, 25))
			minX, maxX = valueX[0], valueX[1]
			figx = plotSPI(df_spi, panel_id , spi_check[2], fitem, 3, [minX, maxX], xysize)
			st.plotly_chart(figx, use_container_width=True)
			#	with col5:
			valueY = st.slider('Select a range of Y shift',-40, 40, (-25, 25))
			minY, maxY = valueY[0], valueY[1]
			figy = plotSPI(df_spi, panel_id , spi_check[3], fitem, 3, [minY, maxY], xysize)
			st.plotly_chart(figy, use_container_width=True)
			#	with col1:
			valueA = st.slider('Select a range of Areas',50, 150, (50, 150))
			minA, maxA = valueA[0], valueA[1]
			figA = plotSPI(df_spi, panel_id , spi_check[1], fitem, 3, [minA, maxA], xysize)
			st.plotly_chart(figA, use_container_width=True)				
	#
	with gcol3:
		if submitted_db and df_db is not None:
			if df1.shape[0] == 40994:
				xysize=[500, 500]
				panel_id=df1['Panel_ID'].unique()[0]
				figx = plotDB(df1, panel_id, 'X', None, None, xysize)
				figy = plotDB(df1, panel_id, 'Y', None, None, xysize)
				#db_col1a, db_col2a, db_col3a = st.columns([5,1,5])
				#with db_col1a:					
				st.plotly_chart(figx, use_container_width=True)
				#with db_col3a:
				st.plotly_chart(figy, use_container_width=True)
			else: 
				st.error('There is an error of input file. \n Please check the sample no. of raw datas!', icon="🚨")
			#with st.expander("See detail datas!"):
			#	st.write(df1)
		
	#elif choice == "AOI":
	#	st.subheader("AOI is under constructed! Coming Soon...")
		#

if __name__ == '__main__':
	#initD()
	main()
