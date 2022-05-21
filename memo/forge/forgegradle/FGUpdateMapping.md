[https://gist.github.com/JDLogic/bf16deed3bcf99bd9e1a22eb21148389](https://gist.github.com/JDLogic/bf16deed3bcf99bd9e1a22eb21148389)

记得先备份！

```bash
./gradlew -PUPDATE_MAPPINGS="这里写目标映射表版本号" -PUPDATE_MAPPINGS_CHANNEL="这里写目标映射表种类" updateMappings
```

请在运行完后再修改 `build.gradle` 里的映射表版本！