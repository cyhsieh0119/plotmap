from PIL import Image
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Plot Map Exercise !" ,page_icon="random" ,layout="wide")

st.markdown("# Plot XY map for some parameters！🎈")
st.sidebar.markdown("# Main page 🎈 of Side Bar")


def main():
	st.title("File Upload Tutorial")
	menu = ["Dataset","DocumentFiles","About"]
	choice = st.sidebar.selectbox("Menu",menu)
	tab1, tab2, tab3 = st.tabs(["SPI", "DB", "AOI"])

	if choice == "Dataset":
		st.subheader("Dataset")
		data_file = st.file_uploader(r"Upload *.csv or *.csv.zip", type=["csv","zip"])
		if data_file is not None:
			file_details = {"filename":data_file.name, "filetype":data_file.type,
				 	"filesize":data_file.size}
			df = pd.read_csv(data_file, skiprows=10, encoding = "utf-8", engine='python')
			spi_items = [ 'Layout No.', 'Pin No.' , 'Pad No.' , 'Area[um2]' , 'Area[%]' , 'X shift' , 'Y shift', 
				     'No solder' , 'Center X', 'Center Y',             ]
			df1 = df.loc[:,spi_items]
			st.write(df1)
			st.sidebar.write(file_details)
			# To View Uploaded Image
			with tab1:
				st.header(data_file.name)				

	elif choice == "DocumentFiles":
		st.subheader("DocumentFiles")




if __name__ == '__main__':
	#initD()
	main()
