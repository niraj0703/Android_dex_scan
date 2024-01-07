import numpy as np
from cv2 import cv2

# cv2.getGaborKernel(ksize, sigma, theta, lambda, gamma, psi, ktype)
# ksize - size of gabor filter (n, n)
# sigma - standard deviation of the gaussian function
# theta - orientation of the normal to the parallel stripes
# lambda - wavelength of the sunusoidal factor
# gamma - spatial aspect ratio
# psi - phase offset
# ktype - type and range of values that each pixel in the gabor kernel can hold
def cal_color_moment(img):
    img_h, img_w = img.shape
    img_mean = np.sum(img)/(img_h*img_w)
    img_deviation = (img-img_mean)**2
    img_variance_t = (np.sum(img_deviation))/(img_h*img_w)
    img_variance  = np.sqrt(img_variance_t)#**(1./2.)
    #print(img_variance_t)
    img_deviation = (img-img_mean)**3
    img_skewness_t = (np.sum(img_deviation))/(img_h*img_w)
    #print(img_skewness_t)
    img_skewness = np.cbrt(img_skewness_t)#**(1./3.)
    return img_mean, img_variance, img_skewness

def build_filters():
    """ returns a list of kernels in several orientations
    """
    filters = []
    ksize = 21
    for theta in np.arange(0, np.pi, np.pi / 8):
        params = {'ksize':(ksize, ksize), 'sigma':8.0, 'theta':theta, 'lambd':10.0,
                  'gamma':0.5, 'psi':0, 'ktype':cv2.CV_32F}
        kern = cv2.getGaborKernel(**params)
        for i in range(1,5):
            kern *= i
        #filters.append((kern,params))
            filters.append(kern)
    return filters

#g_kernel = cv2.getGaborKernel((21, 21), 8.0, np.pi/4, 10.0, 0.5, 0, ktype=cv2.CV_32F)

img = cv2.imread('greyscale.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#print img.shape
#print len(img)
filters = build_filters()
print(len(filters))
texture_feature = [] #meand of the grid image(4*4)
for filter in filters:
    filtered_img = cv2.filter2D(img, cv2.CV_8UC3, filter)
    #print len(filtered_img)
    #cv2.imshow('image', img)
    #cv2.imshow('filtered image', filtered_img)
    #break
    size_x = filtered_img.shape[1]
    size_y = filtered_img.shape[0]
    #print img.shape, size_x, size_y
    #blocks = np.array_split(filtered_img, 883)
    #blocks = filtered_img.reshape(1024/4, 4, -1, 4).swapaxes(1,2).reshape(-1,4,4)
    '''for block in blocks:
        cv2.imshow(block)'''
    #print(type(filtered_img))
    for i in range(0, 4):
      for j in range(0,4):
        #print(int(i*size_y/4),int(i*size_y/4 + size_y/4),int(j*size_x/4),int(j*size_x/4+ size_x/4) )
        roi = filtered_img[int(i*size_y/4): int(i*size_y/4 + size_y/4), int(j*size_x/4):int(j*size_x/4+ size_x/4)]
        texture_feature.append(np.mean(roi))

print(len(texture_feature))
#cv2.imshow('512-D', texture_feature)
img_2nd  = cv2.imread("image2.png")
yuv = cv2.cvtColor(img_2nd, cv2.COLOR_BGR2YUV)
Y_i,U_i,V_i = cv2.split(yuv)
cv2.imwrite("yuv_Y.png", Y_i)
cv2.imwrite("yuv_U.png", U_i)
cv2.imwrite("yuv_V.png", V_i)
Y_m,Y_v,Y_s = cal_color_moment(Y_i)
U_m,U_v,U_s = cal_color_moment(U_i)
V_m,V_v,V_s = cal_color_moment(V_i)
color_moment_feature =[Y_m,U_m, V_m,Y_v,U_v, V_v,Y_s,U_s, V_s]
print(color_moment_feature)

#h, w = g_kernel.shape[:2]
#g_kernel = cv2.resize(g_kernel, (3*w, 3*h), interpolation=cv2.INTER_CUBIC)
#cv2.imshow('gabor kernel (resized)', g_kernel)
#cv2.waitKey(0)
#cv2.destroyAllWindows()'''