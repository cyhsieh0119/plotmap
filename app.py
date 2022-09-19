from PIL import Image
import streamlit as st
import numpy as np
import plotly.express as px

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
				 	            "filesize":image_file.size}
			st.sidebar.write(file_details)
			# To View Uploaded Image
			with tab1:
				st.header(data_file.name)				

	elif choice == "DocumentFiles":
		st.subheader("DocumentFiles")




if __name__ == '__main__':
	#initD()
	main()
