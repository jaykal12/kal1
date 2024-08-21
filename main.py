import streamlit as st
import hashlib
from PIL import Image
import io

# Dummy user database (replace with a real database)
users = {
    "jaykal": hashlib.sha256("malik".encode()).hexdigest()
}

# Function to hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Login function
def login(username, password):
    if username in users and users[username] == hash_password(password):
        return True
    return False

# Streamlit app
def main():
    st.title("Secure Text & Image Application")

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if 'uploaded_image' not in st.session_state:
        st.session_state.uploaded_image = None

    if not st.session_state.logged_in:
        st.header("Please Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login(username, password):
                st.session_state.logged_in = True
                st.success("Login successful!")
            else:
                st.error("Login failed. Please check your username and password.")
    else:
        st.header("Secure Text")
        text_area = st.text_area("Your secure text", "jaydeep", height=200)
        if st.button("Save Text"):
            st.success("Text saved successfully!")

        st.header("Upload an Image")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format=image.format)
            st.session_state.uploaded_image = img_byte_arr.getvalue()
            st.image(image, caption='Uploaded Image.', use_column_width=True)
            st.success("Image saved successfully!")

        if st.session_state.uploaded_image is not None:
            st.header("Previously Uploaded Image")
            image = Image.open(io.BytesIO(st.session_state.uploaded_image))
            st.image(image, caption='Uploaded Image.', use_column_width=True)

            # Download button
            st.download_button(
                label="Download Image",
                data=st.session_state.uploaded_image,
                file_name="uploaded_image.png",
                mime="image/png"
            )

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.warning("Logged out successfully.")

if __name__ == '__main__':
    main()
