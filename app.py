from PIL import Image
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from utils import read_SPI_file, plotSPI

st.set_page_config(page_title = "Plot Map!" ,page_icon="random" ,layout="wide")
st.sidebar.markdown("# Main page 🎈 of Side Bar")
#st.title("# Plot XY Map for Some Parameter！")

def main():
	#st.title("File Upload Tutorial")
	st.title("# Plot XY Map for Some Parameter！")
	menu = ["Dataset","DocumentFiles","About"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Dataset":
		st.subheader("Dataset")
		data_file = st.file_uploader(r"Upload *.csv or *.csv.zip", type=["csv","zip"])
		#
		tab1, tab2 = st.tabs(["Graph", "Detail Data"])
		if data_file is not None:
			file_details = {"filename":data_file.name, "filetype":data_file.type,
				 	"filesize":data_file.size}
			st.sidebar.write(file_details)
			df1 = read_SPI_file(data_file)

			with tab1:
				panel_id = data_file.name
				spi_check=['Area[um2]', 'Area[%]',  'X shift', 'Y shift' ]
				fitem = 'Pin No.'
				xysize=[600,600]
				figA = plotSPI(df1, panel_id , spi_check[1], fitem, 3, [50, 150], xysize)
				figx = plotSPI(df1, panel_id , spi_check[2], fitem, 3, [-25, 25], xysize)
				figy = plotSPI(df1, panel_id , spi_check[3], fitem, 3, [-25, 25], xysize)
				st.plotly_chart(figA, use_container_width=False)
				st.plotly_chart(figx, use_container_width=False)
				st.plotly_chart(figy, use_container_width=False)	

			# To View Uploaded Image
			with tab2:
				st.write(df1)				

	elif choice == "DocumentFiles":
		st.subheader("DocumentFiles")


if __name__ == '__main__':
	#initD()
	main()
