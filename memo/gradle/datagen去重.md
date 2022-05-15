将可能自带的一句`sourceSets.main.resources { srcDir 'src/generated/resources' }`换为如下内容：

```groovy
task mergeResources(type: Copy) {
    def generated = files("src/generated/resources")
    def resources = files("src/main/resources")

    from generated
    exclude(str -> {
        def file = file("src/main/resources/" + str.relativePath)
        return file.isFile() && !resources.contains(file)
    })
    into "$buildDir/resources/main"
}

compileJava.dependsOn mergeResources
```

效果是将包含在 generated 但不包含在 main 中的 resources 复制到 build/resources/main 中。