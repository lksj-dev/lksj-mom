新建一个 configuration

```groovy
configurations {
    shade
    implementation.extendsFrom shade
}
```

使用这个 configuration 为项目添加依赖

```groovy
dependencies {
    shade "org.lwjgl:lwjgl-assimp:$lwjglVersion"
}
```

最后在 jar 块中打包

```groovy
jar {
    into('lib') {
        from configurations.shade
    }
}
```

然后这个 configuration 导入的依赖就会在 .jar 里的 lib 文件夹内出现了。