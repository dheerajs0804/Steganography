import wx
from PIL import Image
def genData(data):
    newd = []
    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd
def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)
    for i in range(lendata):
        pix = [value for value in imdata.__next__()[:3] +
                                imdata.__next__()[:3] +
                                imdata.__next__()[:3]]

        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                pix[j] -= 1
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1

        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1
        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

def encode(image_name, data, new_img_name):
    image = Image.open(image_name, 'r')
    if (len(data) == 0):
        raise ValueError('Data is empty')

    newimg = image.copy()
    encode_enc(newimg, data)
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))
def decode(image_name):
    image = Image.open(image_name, 'r')
    data = ''
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                imgdata.__next__()[:3] +
                                imgdata.__next__()[:3]]

        binstr = ''
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data
class SteganographyApp(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Steganography', size=(400, 300))
        panel = wx.Panel(self)
        encode_button = wx.Button(panel, label='Encode', pos=(140, 50), size=(200, 30))
        decode_button = wx.Button(panel, label='Decode', pos=(140, 90), size=(200, 30))
        self.result_text = wx.StaticText(panel, label='', pos=(140, 130), size=(200, 30))

        encode_button.Bind(wx.EVT_BUTTON, self.on_encode)
        decode_button.Bind(wx.EVT_BUTTON, self.on_decode)
    def on_encode(self, event):
        image_name = wx.GetTextFromUser('Enter image name (with extension):', 'Image Input')
        data = wx.GetTextFromUser('Enter data to be encoded:', 'Data Input')
        new_img_name = wx.GetTextFromUser('Enter the name of new image (with extension):', 'New Image Name')
        try:
            encode(image_name, data, new_img_name)
            self.result_text.SetLabel('Image encoded successfully!')
        except Exception as e:
            self.result_text.SetLabel('Error: ' + str(e))
    def on_decode(self, event):
        image_name = wx.GetTextFromUser('Enter image name (with extension):', 'Image Input')
        try:
            decoded_data = decode(image_name)
            self.result_text.SetLabel('Decoded Data: ' + decoded_data)
        except Exception as e:
            self.result_text.SetLabel('Error: ' + str(e))
if __name__ == '__main__':
    app = wx.App()
    frame = SteganographyApp()
    frame.Show()
    app.MainLoop()
