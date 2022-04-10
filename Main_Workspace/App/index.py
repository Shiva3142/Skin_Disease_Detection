from flask import Flask,render_template,redirect,request,send_from_directory,jsonify
import numpy
import pandas
import tensorflow
import time
import os
import cv2
filename=""

classes_list=['Acne and Rosacea Photos','Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions','Atopic Dermatitis Photos','Bullous Disease Photos','Cellulitis Impetigo and other Bacterial Infections','Eczema Photos','Exanthems and Drug Eruptions','Hair Loss Photos Alopecia and other Hair Diseases','Herpes HPV and other STDs Photos','Light Diseases and Disorders of Pigmentation','Lupus and other Connective Tissue diseases','Melanoma Skin Cancer Nevi and Moles','Nail Fungus and other Nail Disease','Poison Ivy Photos and other Contact Dermatitis','Psoriasis pictures Lichen Planus and related diseases','Scabies Lyme Disease and other Infestations and Bites','Seborrheic Keratoses and other Benign Tumors','Systemic Disease','Tinea Ringworm Candidiasis and other Fungal Infections','Urticaria Hives','Vascular Tumors','Vasculitis Photos','Warts Molluscum and other Viral Infections']
def printClassList():
    for class_name in classes_list:
        print(f"{classes_list.index(class_name)} -->  {class_name}")
# printClassList()   
def getClassvalue(index):
    return classes_list[index]


app=Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
    # return 'hello world'

@app.route('/detection')
def detection():
    return render_template('detection.html')

@app.route('/about')
def about():
    return "about page"

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')
    # return "analytics page"


@app.route('/getresult',methods=['POST','GET'])
def getresult():
    global filename
    if request.method=='POST':
        if filename!="":
            # image_path="C:\\Users\\Pankaj singh\\OneDrive\\Desktop\\Python Development\\Temporary\\Artificial intelligence\\Skin_Disease_Detection\\Main_Workspace\\Data\\train\\Bullous Disease Photos\\benign-"
            # image_data=image.load_img(image_path,target_size=IMAGE_SIZE)
            # image_array=image.img_to_array(image_data)
            # image_array_expanded_dimansion=numpy.expand_dims(image_array,axis=0)
            trained_model=tensorflow.keras.models.load_model('./model1_using_only_one_layers.h5')
            image_array=cv2.imread(os.path.dirname(__file__)+f"\\static\\images\\data\\{filename}",cv2.IMREAD_GRAYSCALE)
            image_array=cv2.resize(image_array,(224,224))
            prediction=trained_model.predict(numpy.expand_dims(numpy.expand_dims(image_array,axis=-1),axis=0)).round(5)*100
            print(list(prediction[0]))
            predicted_classes=list(prediction[0])
            sorted_indexes={}
            temp_array=[i for i in predicted_classes]
            for i in predicted_classes:
                index_value=list(temp_array).index(max(temp_array))
                sorted_indexes.update({index_value:max(temp_array)})
                temp_array[index_value]=-1
            # print(temp_array)
            print(sorted_indexes.keys())
            print(max(prediction[0]))
            class_value=list(prediction[0]).index(max(prediction[0]))
            print(class_value)
            response_value=""
            if max(prediction[0])>1:
                response_value=response_value+'  <h2 class="red">DETECTED</h2> <h2>Predictions are : </h2>'
                counter=0
                for key,value in sorted_indexes.items():    
                    print(f"{value} % --> ",end="")
                    print(getClassvalue(key))
                    response_value= response_value+f"<h4>{value.round(2)} % --> {getClassvalue(key)}</h4>"
                    if counter>4:
                        break
                    counter+=1
            else:
                response_value=response_value+' <h2 class="green">NOT DETECTED</h2> '
            print(response_value)
            return jsonify({
            "data":response_value
            })
        else:
            return "ERROR"
    else:
        return "ERROR"


@app.route('/upload',methods=['POST','GET'])
def upload():
    global filename
    if request.method=='POST':
        print(request.files['file'])
        # print(request.files)
        file=request.files['file']
        filename=file.filename
        extension=filename.split(".")[-1]
        print(extension)
        miliseconds_value=round(time.time()*1000)
        filename=f"{miliseconds_value}.{extension}"
        print(filename)
        file_path=f"/static/images/data/{filename}"
        file.filename=filename
        print(file)
        file.save(os.path.dirname(__file__)+f"\\static\\images\\data\\{filename}")
        return jsonify({'image_path':file_path})
    else:
        return "error"

@app.errorhandler(404)
def home(e):
    print(e)
    return redirect('/')
    # return 'hello world'


if __name__=='__main__':
    app.run(debug=True)
