import streamlit as st
import boto3
import os

# AWS Polly client initialization
polly_client = boto3.client(
    'polly',
    aws_access_key_id='your-access-key',
    aws_secret_access_key='your-secret-access-key',
    region_name='us-east-1'  # Choose your preferred region
)

# Function to generate speech from text using Amazon Polly
def speak_text(input_text, voice_id):
    try:
        response = polly_client.synthesize_speech(
            Text=input_text,
            OutputFormat='mp3',
            VoiceId=voice_id
        )
        audio_file = "output.mp3"
        with open(audio_file, 'wb') as audio_stream:
            audio_stream.write(response['AudioStream'].read())
        return audio_file  # Return the file name for later use
    except Exception as e:
        st.error(f"Error generating speech: {e}")
        return None

# Main function to run the Streamlit app
def main():
    st.title("AI Text to Speech Converter")

    # Input text box
    input_text = st.text_area("Enter text here:", height=200)

    # File uploader for text files
    uploaded_file = st.file_uploader("Upload a text file", type="txt")

    if uploaded_file is not None:
        # Read the contents of the uploaded file
        file_contents = uploaded_file.read().decode("utf-8")
        input_text = file_contents  # Update the text area with the file contents
        st.text_area("File content:", file_contents, height=200)

    # Voice selection
    voice_options = {
        "English - Female (Joanna)": "Joanna",
        "English - Female (Salli)": "Salli",
        "English - Male (Matthew)": "Matthew",
        "English - Male (Brian)": "Brian",
        "Hindi - Female (Aditi)": "Aditi",
        "Hindi - Female (Raveena)": "Raveena"
    }
    
    voice_id = st.selectbox("Select Voice", list(voice_options.keys()))

    # Button to speak the text
    if st.button("Speak"):
        if input_text:
            audio_file = speak_text(input_text, voice_options[voice_id])
            if audio_file:  # Check if audio_file was created successfully
                st.success("Speaking...")
                # Play the audio file
                st.audio(audio_file)
                # Provide a download link for the audio file
                st.markdown(f"[Download Audio]({audio_file})")
                # Optionally remove the audio file after serving it
                # os.remove(audio_file)
        else:
            st.warning("Please enter text or upload a file before clicking 'Speak'.")

if __name__ == "__main__":
    main()

