import streamlit as st
import os

def load_camera_data(file_path):
    """Reads the camera data, ignoring the header and returns camera labels and percentages."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    data = {line.split(',')[0].strip(): float(line.split(',')[1].strip()) for line in lines[1:] if line.strip()}
    return list(data.items())

def display_train_diagram(camera_data):
    """Displays a row of markdown styled boxes as a visual representation of train cars."""
    st.write("Train Car Capacity Visualization")  # Header for the section
    for name, percent in camera_data:
        # Proper white to red transition
        red = int(255)
        green_blue = int(255 * (1 - (percent / 100)))
        color = f"rgb({red}, {green_blue}, {green_blue})"
        # Use markdown to create a visually styled box
        st.markdown(f"<div style='width: 100px; height: 50px; background-color: {color}; color: black; border-radius: 10px; text-align: center; line-height: 50px;'>{name} | {int(percent)}%</div>", unsafe_allow_html=True)

def display_images(camera_data):
    """Displays clickable buttons for each camera and the train diagram using buttons."""
    st.title('MTA Countdown Clock with Passenger Capacity')
    
    col1, col2 = st.columns([3, 1])

    sidebar = st.sidebar
    with sidebar:
        st.subheader("Camera List")
        for index, (name, percent) in enumerate(camera_data, start=1):
            # Proper white to red transition
            red = int(255)
            green_blue = int(255 * (1 - (percent / 100)))
            color = f"rgb({red}, {green_blue}, {green_blue})"
            # Create clickable divs with HTML and JavaScript
            st.markdown(f"""
                <div onclick="streamlitUpdate({index})" 
                     style='width: 100%; height: 50px; background-color: {color}; color: black; border-radius: 10px; text-align: center; line-height: 50px; cursor: pointer;'>
                    {name} | {int(percent)}%
                </div>
            """, unsafe_allow_html=True)

    with col1:
        st.subheader("Image for AI Model")
        if 'selected_camera' in st.session_state:
            selected_camera = st.session_state['selected_camera']
            image_path = f'/Users/Rm501_09/Documents/MTA_ASR_24/video/consists/results/predict{selected_camera}/camera{selected_camera}.jpg'
            if os.path.exists(image_path):
                st.image(image_path, caption=f'Image for Camera {selected_camera}')
            else:
                st.error("Image not found. Check the camera output directory.")

    #with col2:
    #    st.subheader("Train Car Capacity Visualization")
    #    display_train_diagram(camera_data)

# JavaScript to update the session state
st.markdown("""
    <script>
        function streamlitUpdate(selectedCamera) {
            const streamlitEvent = new CustomEvent("streamlit:click", {
                detail: { selectedCamera: selectedCamera }
            });
            window.dispatchEvent(streamlitEvent);
        }

        window.addEventListener('streamlit:click', (event) => {
            const selectedCamera = event.detail.selectedCamera;
            window.parent.postMessage({ type: 'streamlit:setSessionState', key: 'selected_camera', value: selectedCamera }, '*');
        });
    </script>
""", unsafe_allow_html=True)

def main():
    camera_data = load_camera_data('output.txt')
    if camera_data:
        display_images(camera_data)
    else:
        st.error("No camera data found in output.txt")

if __name__ == '__main__':
    main()
