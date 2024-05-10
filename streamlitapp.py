import streamlit as st
import os

def load_camera_data(file_path):
    """ Reads the camera data, ignoring the header. """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    # Assuming the first line is the header and should be ignored
    return [line.strip() for line in lines[1:] if line.strip()]

def display_images(camera_names):
    """ Displays clickable buttons for each camera, showing images when clicked. """
    st.title('MTA Countdown Clock with Passenger Capacity')
    
    # Two columns layout: left for image display, right for camera list
    col1, col2 = st.columns([3, 1])

    with col2:
        st.subheader("Camera List")
        # Dynamically create buttons for each camera
        for index, name in enumerate(camera_names, start=1):
            if st.button(f'Camera {index} - {name}'):
                st.session_state['selected_camera'] = index

    with col1:
        st.subheader("Image for AI Model")
        if 'selected_camera' in st.session_state:
            image_path = f'/Users/Rm501_09/Documents/MTA_ASR_24/video/consists/results/predict{st.session_state["selected_camera"]}/camera{st.session_state["selected_camera"]}.jpg'
            if os.path.exists(image_path):
                st.image(image_path, caption=f'Camera {st.session_state["selected_camera"]} - Image')
            else:
                st.error("Image not found. Check the camera output directory.")

def main():
    camera_names = load_camera_data('output.txt')
    if camera_names:
        display_images(camera_names)
    else:
        st.error("No camera data found in output.txt")

if __name__ == '__main__':
    main()
