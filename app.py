from PIL import Image
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from utils import read_SPI_file, plotSPI

st.set_page_config(page_title = "Plot Map!" ,page_icon="random" ,layout="wide", initial_sidebar_state="collapsed")
st.sidebar.markdown("# Please Select the Items:")
#st.title("# Plot XY Map for Some Parameter！")

def main():
	#st.title("File Upload Tutorial")
	st.title("# Plot XY Map for Some Parameter！")
	menu = ["SPI","DB","AOI"]
	choice = st.sidebar.selectbox("Menu(Only SPI is OK!)",menu)

	if choice == "SPI":
		st.subheader("Please use *.csv.zip as the input dataset file !")
		tcol1, tcol2 = st.columns(2)
		with tcol1:
			data_file = st.file_uploader(r"Upload *.csv or *.csv.zip", type=["zip"])
		#
		tab1, tab2 = st.tabs(["XY Map", "Histogram"])
		if data_file is not None:
			with tcol2:
				file_details = {"filename":data_file.name, "filetype":data_file.type, "filesize":data_file.size}
				st.sidebar.write(file_details)
			#
			df1 = read_SPI_file(data_file)
			spi_check=['Area[um2]', 'Area[%]',  'X shift', 'Y shift' ]

			with tab1:
				panel_id = data_file.name
				fitem = 'Pin No.'
				xysize=[450,450]
				figA = plotSPI(df1, panel_id , spi_check[1], fitem, 3, [50, 150], xysize)
				figx = plotSPI(df1, panel_id , spi_check[2], fitem, 3, [-25, 25], xysize)
				figy = plotSPI(df1, panel_id , spi_check[3], fitem, 3, [-25, 25], xysize)
				col1, col2, col3 = st.columns(3)
				with col1:
					st.plotly_chart(figA, use_container_width=True)
				with col2:
					st.plotly_chart(figx, use_container_width=True)
				with col3:
					st.plotly_chart(figy, use_container_width=True)
				
				#st.plotly_chart(figA, use_container_width=False)
				#st.plotly_chart(figx, use_container_width=False)
				#st.plotly_chart(figy, use_container_width=False)

			# To View Uploaded Image
			with tab2:
				hcol1, hcol2, hcol3 = st.columns(3)
				with hcol1:
					st.plotly_chart(px.histogram(df1, x=spi_check[1], title=panel_id, log_y=True) ,use_container_width=True)
				with hcol2:
					st.plotly_chart(px.histogram(df1, x=spi_check[2], title=panel_id, log_y=True) ,use_container_width=True)
				with hcol3:
					st.plotly_chart(px.histogram(df1, x=spi_check[3], title=panel_id, log_y=True) ,use_container_width=True)
				#st.plotly_chart(px.histogram(df1, x=spi_check[1], title=panel_id, log_y=True) )
				#st.plotly_chart(px.histogram(df1, x=spi_check[2], title=panel_id, log_y=True) )
				#st.plotly_chart(px.histogram(df1, x=spi_check[3], title=panel_id, log_y=True) )
				#st.write(df1[spi_check].describe())
				with st.expander("See detail datas!"):
					st.write(df1)				

	elif choice == "DB":
		st.subheader("DB is under constructed! Coming Soon...")
	
	elif choice == "AOI":
		st.subheader("AOI is under constructed! Coming Soon...")


if __name__ == '__main__':
	#initD()
	main()
