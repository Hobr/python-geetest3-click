# 极验3代点字逆向

## 感谢

- [Amorter/biliTicker_gt](https://github.com/Amorter/biliTicker_gt)

## 开发

```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip install poetry virtualenv pre-commit

virtualenv venv
source venv/script/activate
poetry install
pre-commit install

# 更新
poetry update
pre-commit autoupdate
```
