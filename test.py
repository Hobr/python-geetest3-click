import bili_ticket_gt_python

slide = bili_ticket_gt_python.SlidePy()

try:
    (gt, challenge) = slide.register_test("http://127.0.0.1:5000/pc-geetest/register")
    (_, _) = slide.get_c_s(gt, challenge)
    _type = slide.get_type(gt, challenge)
    if _type != "slide":
        raise Exception("验证码类型错误")
    (c, s, args) = slide.get_new_c_s_args(gt, challenge)

    challenge = args[0]
    key = slide.calculate_key(args)

    w = slide.generate_w(key, gt, challenge, str(c), s, "abcdefghijklmnop")
    (msg, validate) = slide.verify(gt, challenge, w)
    print(validate)
except Exception as e:
    print("识别失败")
    print(e)
