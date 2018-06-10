from keras.models import model_from_json
json_file = open("vgg16_cat_dogstest.json", "r")
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("vgg16_cat_dogstest.h5")
loaded_model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
print ("Загрузили Model")

import numpy as np
from keras.preprocessing import image

def cat_or_dog():
    img_path = 'local-filename.jpg'

    img_to_detect = image.load_img(img_path, target_size=(150, 150))
    array = image.img_to_array(img_to_detect)
    array /= 255
    array = np.expand_dims(array, axis=0)
    prediction = loaded_model.predict(array)
    print(prediction)
    classes = ['Cat', 'Dog']

    return classes[np.argmax(prediction)]

