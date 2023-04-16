import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image


label =  ['Bacterial spot', 'Early blight', 'Late blight', 'Leaf Mold', 'Septoria leaf spot', 'Twospottedspider mite', 'Target Spot', 'Yellow Leaf Curl Virus', 'mosaic virus', 'healthy']


# model_path = "media/model/litemodel.tflite"
model_path=
img_size = 255

interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


def predictDisease(img_path):
    loadimage = image.load_img(img_path,target_size=(img_size,img_size))

    imgtoarray = image.img_to_array(loadimage)
    # imgtoarray = imgtoarray.reshape((1,)+imgtoarray.shape)
    imgtoarray = imgtoarray/255.0
    imgtoarray = tf.expand_dims(imgtoarray,0)

   
    interpreter.set_tensor(input_details[0]['index'],imgtoarray)
    interpreter.invoke()

    output = interpreter.get_tensor(output_details[0]['index'])
    predicted_disease = np.argmax(output[0])

    confidence =  round(100* (np.max(output[0])))

    result = label[predicted_disease]
    return (confidence,result)

