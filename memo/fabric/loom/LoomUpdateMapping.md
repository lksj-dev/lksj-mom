[https://fabricmc.net/wiki/tutorial:migratemappings](https://fabricmc.net/wiki/tutorial:migratemappings)

```bash
./gradlew migrateMappings --mappings "目标映射表版本号"
```

转换结果在 `remappedSrc` 目录。请在运行完后再修改 `build.gradle` 里的映射表版本！