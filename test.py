import time

import bili_ticket_gt_python

from util import W

w = W()
click = bili_ticket_gt_python.ClickPy()

try:
    (gt, challenge) = click.register_test(
        "https://passport.bilibili.com/x/passport-login/captcha?source=main_web"
    )
    (_, _) = click.get_c_s(gt, challenge)
    _type = click.get_type(gt, challenge)
    if _type != "click":
        raise Exception("验证码类型错误")
    (c, s, args) = click.get_new_c_s_args(gt, challenge)
    before_calculate_key = time.time()
    key = click.calculate_key(args)
    w = click.generate_w(key, gt, challenge, str(c), s, "abcdefghijklmnop")
    w_use_time = time.time() - before_calculate_key
    print(f"w生成时间: {w_use_time}")
    if w_use_time < 2:
        time.sleep(2 - w_use_time)
    (msg, validate) = click.verify(gt, challenge, w)
    print(validate)
except Exception as e:
    print("识别失败")
    print(e)