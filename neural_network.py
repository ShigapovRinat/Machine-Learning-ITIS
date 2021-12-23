import matplotlib.pyplot as plt
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from PIL import Image

# Model / data parameters
num_classes = 10
input_shape = (28, 28, 1)

# the data, split between train and test sets
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# Scale images to the [0, 1] range
x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255
# Make sure images have shape (28, 28, 1)
x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)
print("x_train shape:", x_train.shape)
print(x_train.shape[0], "train samples")
print(x_test.shape[0], "test samples")

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

model = keras.Sequential(
    [
        keras.Input(shape=input_shape),
        layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation="softmax"),
    ]
)

model.summary()

batch_size = 128
epochs = 3

model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1)

score = model.evaluate(x_test, y_test, verbose=0)
print("Test loss:", score[0])
print("Test accuracy:", score[1])

image = Image.open('img_4.png')

tmp = np.full((28, 175), 255)
image_array = (tmp - np.array(Image.open('img_4.png').resize((175, 28)).convert('L'))) / 255

test = Image.fromarray(image_array * 255).convert('RGB')

plt.imshow(image)
plt.show()
plt.imshow(test)
plt.show()

# Подразумеваю, что между цифрами есть "столбец" пустоты, тогда отделю цифры через них
# Алгоритм работает так:
#   Прохожу по всем столбцам картинки и ищу на ней белый пиксель
#   если он есть, значит тут начинается или кончается цифра
#   Если цифра не найдена и найден белый пиксель, отмечаю, что найдена цифра
#   Если цифра найдена и не найден белый пиксель, то отмечаю, что цифра больше
#   не найдена и добавляю цифру в лист с некоторыми изменениями
#   * привожу к размеру 28х28

i = 0
digits = []

# Флаг, что найдена цифра на картинке
digit_found = False
# Индексы начала и конца цифры на картинке
digit_start, digit_end = 0, 0
# Прохожу по всем столбцам
while i < 175:
    # Флаг, что был белый пиксель
    on_digit = False
    # Прохожу по всем строкам столбца
    for j in range(28):
        # Если есть белый пиксель
        if image_array[j, i] > 0.1:
            # Если не найдена цифра, отмечаю это и отмечаю начало цифры
            if not digit_found:
                digit_found = True
                digit_start = i
            # Отмечаю, что найден белый пиксель
            on_digit = True
            break
    # Если белый пиксель не найден и найдено число
    # отмечаю конец цифры, преобразую её в 28х28 массив
    # и добавляю в лист цифр в картинке
    if (not on_digit) & digit_found:
        digit_found = False
        digit_end = i
        temp_digit = image_array[:, digit_start:digit_end]
        digit_tmp = np.full((28, 28, 1), 0)
        # print(len(temp_digit[0]))
        copy_start = int((28 - len(temp_digit[0])) / 2)
        for k in range(copy_start, copy_start + len(temp_digit[0])):
            for l in range(28):
                digit_tmp[l][k] = temp_digit[l][k - copy_start]
        digits.append(digit_tmp)
    i += 1

print(str(len(digits)) + "\n")

result = model.predict(np.array(digits))

ans = ""
for case in np.split(result, len(digits)):
    predicted = np.argmax(case)
    ans += str(predicted)
print(ans)
