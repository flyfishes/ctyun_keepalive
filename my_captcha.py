import time

# 导入包
try:
    import muggle_ocr
except ImportError:
    class Muggle_OCR():
        from enum import Enum
        class ModelType(Enum):
            Captcha=1
            OCR=2
            
        def SDK(self,model_type):
            return self
        def predict(self,image_bytes):
            return "nofoundOCR"
    muggle_ocr=Muggle_OCR()

def captcha_pic(fname,model_type=muggle_ocr.ModelType.Captcha,loops=1):
    # 初始化；model_type 包含了 ModelType.OCR/ModelType.Captcha 两种
    sdk = muggle_ocr.SDK(model_type=model_type)
    # ModelType.OCR 可识别光学印刷文本
    try:
        with open(fname, "rb") as f:
            b = f.read()
            for i in range(loops):
                st = time.time()
                capt_text = sdk.predict(image_bytes=b)
                print(capt_text, time.time() - st)
    except FileNotFoundError as e:
        capt_text=None
    return capt_text


if __name__ == '__main__':   

    for n in range(1,10):
        fname=f"captcha{n}.jpg"
        code=captcha_pic(fname,muggle_ocr.ModelType.Captcha)
        if(code==None):break