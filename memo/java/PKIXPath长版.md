不论你在干什么，如果你看到了这个错误提示

```
javax.net.ssl.SSLHandshakeException: sun.security.validator.ValidatorException: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target
```

或者任何有类似 `PKIX path building failed` 字样的错误或者日志，这说明你现在在跑的程序无法验证从某个地方发来的 SSL/TLS 证书，并因此抛出异常。

这个错误很容易出现在部署 Mod 开发环境的时候，因为这个过程经常涉及到从一些网站上下载文件，而这些网站中有很多都在使用近年颁发的根证书所签发的 SSL/TLS 证书来启用 HTTPS。

解决方法很简单：更新你的 JDK，因为新版 JDK 发布时往往也会更新其自带的根证书信息。

如果你电脑上有不止一个 JDK，那基本可以确认你选用了一个旧版的 JDK。请确认你没选错 JDK。
