from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import pandas as pd
class LinearCorrection:
    def __init__(self, image):
        self.image = np.asarray(Image.open(image))
        self.length, self.width= self.image.shape
        self.overall = self.length* self.width
    def get_positions(self):
        dic={}
        horiz = []
        vertic =[]
        y = []
        for i in range(self.length):
            for j in range(self.width):
                dic[(i,j)] = self.image[i][j]
                horiz.append(j)
                vertic.append(i)
                y.append(self.image[i][j])
        return dic, horiz, vertic, y
    def create_image(self, difference):
        count = 0
        target = [[0] * self.width for _ in range(self.length)]
        for i in range(256):
            for j in range(256):
                target[i][j] = difference[count]
                count += 1
        return target
if __name__ == '__main__':
    corrector = LinearCorrection('adjusted_moon.jpg')
    plt.imshow(corrector.image, cmap='gray')
    plt.show()
    dic, horiz, vertic, y  = corrector.get_positions()
    horiz, vertic, y = np.array(horiz), np.array(vertic), np.array(y)
    df = pd.DataFrame()
    df['horiz'] = horiz
    df['vertic'] = vertic
    model = LinearRegression()
    model.fit(df, y)
    predictions = model.predict(df)
    difference = y - predictions
    target = corrector.create_image(difference)
    plt.imshow(target, cmap='gray')
    plt.show()
    poly = PolynomialFeatures(2)
    df = poly.fit_transform(df)
    model.fit(df, y)
    predictions = model.predict(df)
    difference = y - predictions
    target = corrector.create_image(difference)
    plt.imshow(target, cmap='gray')
    plt.show()






























