import os
from PIL import Image
import pytesseract
import replicate
import streamlit as st

# Path to the image file
image_path = r"E:\Project\New folder\OCR\Images"

# Function to extract and process text from an image file


def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)

        # Convert to lowercase
        text = text.lower()

        # Remove extra spaces
        text = ' '.join(text.split())

        return text
    except Exception as e:
        print(f"Could not process {image_path}: {e}")
        return None


# Processing the specified image file
extracted_text = extract_text_from_image(image_path)
if extracted_text:
    print(
        f"Extracted text from {os.path.basename(image_path)}:\n{extracted_text}\n")

# LLaMA AI Integration with Streamlit
st.set_page_config(page_title="Invoice Generator with LLaMA AI")

# Replicate Credentials
with st.sidebar:
    st.title('Invoice Generator Bot')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('API key already provided!', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input(
            'Enter Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api) == 40):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')

    st.subheader('Models and parameters')
    selected_model = st.selectbox('Choose a Llama2 model', [
                                  'Llama2-7B', 'Llama2-13B', 'Llama2-70B'], key='selected_model')
    if selected_model == 'Llama2-7B':
        llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_model == 'Llama2-13B':
        llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    else:
        llm = 'replicate/llama70b-v2-chat:e951f18578850b652510200860fc4ea62b3b16fac280f83ff32282f87bbd2e48'

    temperature = st.slider('Temperature', min_value=0.01,
                            max_value=5.0, value=0.1, step=0.01)
    top_p = st.slider('Top_p', min_value=0.01,
                      max_value=1.0, value=0.9, step=0.01)
    max_length = st.slider('Max Length', min_value=64,
                           max_value=4096, value=512, step=8)

os.environ['REPLICATE_API_TOKEN'] = replicate_api

# Function for generating LLaMA2 response based on extracted text


def generate_llama2_response(prompt_input):
    string_dialogue = f"You are an assistant generating an invoice based on extracted text: {prompt_input}"

    output = replicate.run(llm,
                           input={"prompt": f"{string_dialogue} Assistant: ",
                                  "temperature": temperature, "top_p": top_p, "max_length": max_length, "repetition_penalty": 1})
    return output


# Generate the response using LLaMA AI
if extracted_text:
    invoice_response = generate_llama2_response(extracted_text)
    st.write("### Generated Invoice Details:")
    st.write(invoice_response)

    # You can further process the LLaMA response to generate a structured invoice as needed.
