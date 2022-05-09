不论你在干什么，如果你看到了这个错误提示

```
javax.net.ssl.SSLHandshakeException: sun.security.validator.ValidatorException: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target
```

或者任何有类似 `PKIX path building failed` 字样的错误或者日志，请更新你的 JDK。

如果你电脑上有不止一个 JDK，请确认你没选错 JDK。

查阅「PKIXPath长版」以了解这个错误背后的故事。