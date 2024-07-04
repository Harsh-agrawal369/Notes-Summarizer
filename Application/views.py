from django.shortcuts import render
from django.http import HttpResponse
import os, shutil
from pdf2image import convert_from_path
import easyocr
import cv2
from groq import Groq
from decouple import config
from fpdf import FPDF
# Create your views here.

def home(request):
    return render(request, 'index.html')

def upload_file(request):
    if request.method == 'POST':
        if 'notesFile' in request.FILES:
            noteFile = request.FILES['notesFile']
            
            current_directory = os.path.dirname(__file__)
            outputpath = os.path.join(current_directory, 'Dir2')
            inputpath = os.path.join(current_directory, 'Dir1')
            txt_files_path = os.path.join(current_directory, 'txtFiles')
            
            file_path = os.path.join(inputpath, noteFile.name)
            
            empty_dir("Dir1")  # Ensure Dir1 is emptied before use
            empty_dir("txtFiles")
            empty_dir(txt_files_path)

            # Save the file to the specified path
            with open(file_path, 'wb') as destination:
                for chunk in noteFile.chunks():
                    destination.write(chunk)
            
            print(current_directory, inputpath, outputpath)
            files = os.listdir(inputpath)
            print("Files:", files)

            # Process each PDF in the input directory
            for element in files:
                path = os.path.join(inputpath, element)
                print(path)
                element_name = os.path.splitext(element)[0]  # Extract the element name without the extension
                element_dir = os.path.join(outputpath, element_name + '_dir')  # Create a directory for the element
                os.makedirs(element_dir, exist_ok=True)  # Ensure the directory exists

                pdf_to_image(path, element_dir, element_name)

            files_out = os.listdir(outputpath)

            # Initialize EasyOCR reader
            reader = easyocr.Reader(['en'])

            text = ""

            # Process each generated image directory
            for subdir in files_out:
                subdir_path = os.path.join(outputpath, subdir)
                if os.path.isdir(subdir_path):
                    images = os.listdir(subdir_path)
                    for img in images:
                        img_path = os.path.join(subdir_path, img)
                        print(f"Processing image: {img_path}")
                        # Read text from image using EasyOCR
                        output = reader.readtext(img_path)
                        for item in output:
                            text += item[1] + "\n"

            output_text_path = os.path.join(txt_files_path, "Output.txt")
            with open(output_text_path, "w") as text_file:
                text_file.write(text)

            # Clean Dir2
            empty_dir(outputpath)
            
            client = Groq(
                api_key = config('API_KEY')
            )

            # Read the content of output.txt
            with open(output_text_path, "r") as file:
                text = file.read()

            # Create the chat completion request to summarize the text
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"Summarize the following text:\n\n{text}\n\n Make points in form of bullets",
                    }
                ],
                model="llama3-8b-8192",
            )

            # Print the summarized content
            # print(chat_completion.choices[0].message.content)
            
            empty_dir(txt_files_path)

            summary_text_path = os.path.join(txt_files_path, "Summary.txt")
            with open(summary_text_path, "w") as summary_file:
                summary_file.write(chat_completion.choices[0].message.content)
                
            create_summary_pdf(summary_text_path, os.path.join(txt_files_path, "Summary.pdf"))
            
            return render(request, "download.html")
        else:
            return HttpResponse("No file uploaded. Please select a file to upload.", status=400)
    else:
        return HttpResponse("Invalid request method. Use POST to upload files.", status=405)
    

def empty_dir(dir_name):
    current_directory = os.path.dirname(__file__)
    directory_path = os.path.join(current_directory, dir_name)

    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        return f'{dir_name} has been emptied.'
    else:
        return f'{dir_name} does not exist.'
    

# Function to convert PDF to images
def pdf_to_image(path_file, DOWNLOAD_FOLDER, elemnt):
    # converting pdf file page to jpg and storing in list
    pages = convert_from_path(path_file, dpi=220, poppler_path=r'C:\Program Files\poppler-23.07.0\Library\bin')
    image_counter = 1
    page_lst = []
    # saving all jpg file one by one in same location
    for page in pages:
        filename = os.path.join(DOWNLOAD_FOLDER, f"{image_counter-1}_{elemnt}.jpg")
        page.save(filename, 'JPEG')
        p_img = cv2.imread(filename)
        height, width, channel = p_img.shape
        # if image is vertically aligned then rotate image to 90 degrees
        if height < width:
            img_rot = cv2.rotate(p_img, cv2.ROTATE_90_CLOCKWISE)
            cv2.imwrite(filename, img_rot)
        page_lst.append(filename)
        image_counter += 1
    filelimit = image_counter - 1
    print('Total no. of pages: ', filelimit)
    return page_lst

def create_summary_pdf(txt_file_path, pdf_file_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    with open(txt_file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Summary", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    for line in lines:
        pdf.multi_cell(0, 10, line)
    
    pdf.output(pdf_file_path)

    print(f"Summary PDF created at: {pdf_file_path}")

def pdf(request):
    current_directory = os.path.dirname(__file__)
    pdf_dir = os.path.join(current_directory, "txtFiles")
    
    pdf_file = None
    files_in_dir = os.listdir(pdf_dir)
    
    for file_name in files_in_dir:
        if file_name.lower().endswith(".pdf"):
            pdf_file = file_name
            break

    if pdf_file:
        pdf_file_path = os.path.join(pdf_dir, pdf_file)
        
        with open(pdf_file_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            
        response['Content-Disposition'] = f'attachment; filename= "{os.path.basename(pdf_file_path)}"'       
        return response
    else:
        return HttpResponse("No PDF Found", status=404)