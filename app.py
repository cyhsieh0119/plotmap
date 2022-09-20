from PIL import Image
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from utils import read_SPI_file, plotSPI

st.set_page_config(page_title="Plot Map Exercise !" ,page_icon="random" ,layout="wide")

st.markdown("# Plot XY map for some parameters！🎈")
st.sidebar.markdown("# Main page 🎈 of Side Bar")

def main():
	st.title("File Upload Tutorial")
	menu = ["Dataset","DocumentFiles","About"]
	choice = st.sidebar.selectbox("Menu",menu)
	#tab1, tab2, tab3 = st.tabs(["SPI", "DB", "AOI"])

	if choice == "Dataset":
		st.subheader("Dataset")
		tab1, tab2 = st.tabs(["Graph", "Detail Data"])
		data_file = st.file_uploader(r"Upload *.csv or *.csv.zip", type=["csv","zip"])
		if data_file is not None:
			file_details = {"filename":data_file.name, "filetype":data_file.type,
				 	"filesize":data_file.size}
			st.sidebar.write(file_details)
			df1 = read_SPI_file(data_file)

			with tab1:
				panel_id = data_file.name
				fitem = 'Pin No.'
				xysize=[600,600]
				figA = plotSPI(df1, panel_id , spi_check[1], fitem, 3, [50, 150], xysize)
				figx = plotSPI(df1, panel_id , spi_check[2], fitem, 3, [-25, 25], xysize)
				figy = plotSPI(df1, panel_id , spi_check[3], fitem, 3, [-25, 25], xysize)
			
			
			# To View Uploaded Image
			with tab2:
				st.write(df1)				

	elif choice == "DocumentFiles":
		st.subheader("DocumentFiles")


if __name__ == '__main__':
	#initD()
	main()
