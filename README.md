# SCUEC信息门户认证模块

> 声明：写这个模块的初衷是学习Python的模块开发，开源是为了方便有需要的同学用作学习研究。使用者需自行承担因不正常使用此模块而产生的一切后果，本人不负任何责任！使用此模块则代表同意此声明。

## 安装

```python
pip install SCUECAuth -i https://pypi.org/simple
```

## 简单使用

```python
# -*- coding: utf-8 -*-
from scuec_auth import SCUECAuth

sa = SCUECAuth()
session = sa.login('工号/学号', '密码')

# 接下来就可以使用session访问有登录限制的地址了，例如session.get(url)，具体方法参照requests.Session
```

##  详细使用

```python
# -*- coding: utf-8 -*-
from scuec_auth import SCUECAuth, debug

# is_verify : 是否验证登录后的session，默认True
# is_debug  : 是否输出认证过程中的debug信息，默认为False
sa = SCUECAuth(is_verify=False, is_debug=False) # 关闭session验证

# 开启session缓存，登录成功后的session将被缓存，有效期默认为1800秒，即30分钟
sa.open_session_cache(max_age=1800)

# 使用用户信息登录，此session将被缓存
# 30分钟内当前用户多次使用login方法都将得到缓存的session，通过该session访问相关地址会更新其最近使用时间以维持会话
# 当缓存的session最近30分钟一直未被使用，则login方法将获取新的session并再次缓存
session = sa.login('工号/学号', '密码')

# 验证session
if sa.verify_session(session):
    debug(tag='验证', msg='session是有效的')
    # 使用session访问有登录限制的地址，例如session.get(url)，具体方法参照requests.Session

sa.logout(username='') # 默认清理当前用户登录所产生session，可通过username参数清除指定用户session

# 关闭session缓存，所有用户登录缓存都将被清除
sa.close_session_cache()
```