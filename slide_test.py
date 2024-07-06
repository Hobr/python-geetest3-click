import bili_ticket_gt_python

from util import W

slide = bili_ticket_gt_python.SlidePy()

for _i in range(50):
    try:
        (gt, challenge) = slide.register_test("?")
        (_, _) = slide.get_c_s(gt, challenge)
        _type = slide.get_type(gt, challenge)
        if _type != "slide":
            raise Exception("验证码类型错误")
        (c, s, args) = slide.get_new_c_s_args(gt, challenge)
        # 注意滑块验证码这里要刷新challenge
        challenge = args[0]
        key = slide.calculate_key(args)
        # rt固定即可
        # 此函数是使用项目目录下的slide.exe生成w参数，如果文件不存在会报错，你也可以自己接入生成w的逻辑函数
        w = W(key=key, gt=gt, challenge=challenge, c=str(c), s=s).SlideCalculate()
        (msg, validate) = slide.verify(gt, challenge, w)
        print(validate)
    except Exception as e:
        print("识别失败")
        print(e)
