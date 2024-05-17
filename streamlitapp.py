import streamlit as st
import os

def load_data(file_path):
    """Reads the camera and schedule data from the output file."""
    camera_data = []
    schedule_data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    is_schedule_section = False
    for line in lines[1:]:  # Skip the header
        if "Schedules" in line:
            is_schedule_section = True
            continue
        if not is_schedule_section:
            parts = line.split(',')
            camera_data.append((parts[0].strip(), float(parts[1].strip())))
        else:
            schedule_data.append(line.strip())
    
    return camera_data, schedule_data

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

def display_schedule(schedule_data):
    """Displays the schedule information."""
    st.write("Train Schedule Information")
    for schedule in schedule_data:
        st.write(schedule)

def display_images(camera_data, schedule_data):
    """Displays clickable buttons for each camera and the train diagram using buttons."""
    st.title('MTA Countdown Clock with Passenger Capacity')
    
    col1, col2 = st.columns([3, 2])

    sidebar = st.sidebar
    with sidebar:
        st.subheader("Camera List")
        camera_options = [f"{name} - {percent:.2f}%" for name, percent in camera_data]
        selected_camera_option = st.selectbox("Select a camera", camera_options)
        selected_camera = camera_options.index(selected_camera_option) + 1
        st.session_state['selected_camera'] = selected_camera
        
        for index, (name, percent) in enumerate(camera_data, start=1):
            # Proper white to red transition
            red = int(255)
            green_blue = int(255 * (1 - (percent / 100)))
            color = f"rgb({red}, {green_blue}, {green_blue})"
            # Create clickable divs with HTML and JavaScript
            st.markdown(f"""
                <div onclick="document.getElementById('button_{index}').click()" 
                     style='width: 100%; height: 50px; background-color: {color}; color: black; border-radius: 10px; text-align: center; line-height: 50px; cursor: pointer;'>
                    {name} | {int(percent)}%
                </div>
                <button id="button_{index}" style="display:none;" onclick="updateSelectedCamera({index})">Click</button>
            """, unsafe_allow_html=True)

    # Debugging output
    st.write("Debug Information:")
    if 'selected_camera' in st.session_state:
        st.write(f"Selected Camera: {st.session_state['selected_camera']}")
    else:
        st.write("No camera selected.")

    with col1:
        st.subheader("Image for AI Model")
        if 'selected_camera' in st.session_state:
            selected_camera = st.session_state['selected_camera']
            image_path = f'/Users/Rm501_09/Documents/MTA_ASR_24/video/consists/results/predict{selected_camera}/camera{selected_camera}.jpg'
            if os.path.exists(image_path):
                st.image(image_path, caption=f'Image for Camera {selected_camera}')
            else:
                st.error("Image not found. Check the camera output directory.")
    
    with col2:
        st.subheader("Schedule Information")
        display_schedule(schedule_data)

# JavaScript to update the session state
st.markdown("""
    <script>
        function updateSelectedCamera(selectedCamera) {
            window.parent.postMessage({type: 'streamlit:setState', value: {selected_camera: selectedCamera}}, '*');
        }
    </script>
""", unsafe_allow_html=True)

def main():
    camera_data, schedule_data = load_data('output.txt')
    if camera_data:
        display_images(camera_data, schedule_data)
    else:
        st.error("No camera data found in output.txt")

if __name__ == '__main__':
    main()
