from keras.layers import GlobalAveragePooling2D
from keras import applications
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import  Dense
from keras.models import Model
from keras import initializers

img_width, img_height = 150, 150
train_data_dir = 'C:/Users/Yaroslav/Desktop/train'
validation_data_dir = 'C:/Users/Yaroslav/Desktop/train'
nb_train_samples = 20
nb_validation_samples = 800
epochs = 1
batch_size = 16

base_model = applications.VGG16(weights='imagenet', include_top=False)
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu',
          kernel_initializer=initializers.RandomUniform(minval=-0.0019, maxval=0.0019, seed=None))(x)

predictions = Dense(2, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

for layer in base_model.layers:
    layer.trainable = False

model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

datagen = ImageDataGenerator(rescale=1. / 255)
train_generator = datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical')

validation_generator = datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical')

model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples)

model_json = model.to_json()

json_file = open("vgg16_cat_dogstest.json", "w")
json_file.write(model_json)
json_file.close()

model.save_weights("vgg16_cat_dogstest.h5")