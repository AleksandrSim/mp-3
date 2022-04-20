from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
class HistNorm:
    def __init__(self, image):
        self.image = np.asarray(Image.open(image))
        self.length, self.width, channels = self.image.shape
    def convert_to_gray(self, red=0.2989, green=0.5870,blue=0.1140):
        target = [[0] * self.width for i in range(self.length)]
        for i in range(self.length):
            for j in range(self.width):
                target[i][j] = int(red * self.image[i][j][0]) + int(green * self.image[i][j][1]) + int(blue * self.image[i][j][2])
        return target

    def calculate_pixel_count(self, target):
        one_vec = []
        dic = {}
        for i in range(self.length):
            for j in range(self.width):
                if target[i][j] in dic:
                    dic[target[i][j]] += 1
                else:
                    dic[target[i][j]] = 1
                one_vec.append(target[i][j])
        return dic, one_vec

    def cum_distrib(self, dic_values):
        sorted_tuples = sorted(list(dic_values.items()), key=lambda x: [x[0]])
        values = [i[0] for i in sorted_tuples]
        counts = [i[1] for i in sorted_tuples]

        dic = {}
        current_su = 0
        for i in range(len(counts)):
            current_su += counts[i]
            dic[values[i]] = current_su
        return dic


    def extract_values(self, dic_values):
        sorted_tuples_clm = sorted(list(dic_values.items()), key=lambda x: [x[0]])
        new_values = [i[0] for i in sorted_tuples_clm]
        new_counts = [i[1] for i in sorted_tuples_clm]

        return new_values, new_counts

    def mapping(self, new_counts, new_values):
        results = []
        dic = {}
        for i in range(len(new_counts)):
            results.append(round((new_counts[i] - min(new_counts)) * 255 / ((256 * 256) - min(new_counts))))
            dic[new_values[i]] = round((new_counts[i] - min(new_counts)) * 255 / ((256 * 256) - min(new_counts)))

        return dic, results


    def light_correction(self, target, dic):
        length, width = len(target), len(target[0])

        new_image = [[0] * width for i in range(length)]
        for i in range(length):
            for j in range(width):
                new_image[i][j] = dic[target[i][j]]

        return new_image


    def sort_dic(self, dic_values):
        sorted_tuples = sorted(list(dic_values.items()), key=lambda x: [x[0]])
        values = [i[0] for i in sorted_tuples]
        counts = [i[1] for i in sorted_tuples]
        return values, counts

    def show(self, values, counts):
        plt.plot(values, counts)
        plt.show()




if __name__ == '__main__':
    corrector = HistNorm('moon.bmp')
    plt.imshow(corrector.image, cmap='gray')
    plt.show()
    target = corrector.convert_to_gray()
    dic_values, one_vec = corrector.calculate_pixel_count(target)
    values, counts = corrector.sort_dic(dic_values)
    corrector.show(values, counts)
    plt.hist(one_vec)
    plt.show()
    cu_dic = corrector.cum_distrib(dic_values)
    new_values, new_counts = corrector.sort_dic(cu_dic)
    corrector.show(new_values, new_counts)
    dic, results = corrector.mapping(new_counts, new_values)
    plt.plot(results)
    plt.show()
    new_image = corrector.light_correction(target, dic)
    plt.imshow(new_image, cmap='gray')
    plt.show()
    #new hist
    dic_values, one_vec = corrector.calculate_pixel_count(new_image)
    plt.hist(one_vec)
    plt.show()



















