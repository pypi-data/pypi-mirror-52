# 颜色日志

## 使用说明

```python
from color_log import Logger

log = Logger()
log.info('message')
log.error('message')
```

linux系统使用 `tail -F -s10 -n20 logs/log | perl -pe 's/(INFO)|(WARNING)|(ERROR)/\e[1;34m$1\e[0m\e[1;33m$2\e[0m\e[1;31m$3\e[0m/g'` 实时监控日志变化