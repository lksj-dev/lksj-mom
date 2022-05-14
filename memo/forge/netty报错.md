如果你翻日志的时候翻到类似如下和 Netty 有关的内容：

```
java.lang.UnsupportedOperationException: Reflective setAccessible(true) disabled
    at io.netty.util.intenral.ReflectionUtil.trySetAccessible(ReflectionUtil.java:31) ~[netty-all-4.1.68.Final.jar%2332!/:4.1.68.Final]
    [以下省略]
```

这是正常现象，和你遇到的任何其他问题都没有关系。请直接无视这一大段。

刷这个栈帧是因为 JEP 396 等 JEP 交付以来 JDK 对其内部实现类的保护越来越严格，表现之一就是限制反射。