如果你配置开发环境时被提示

```
Task 'setupDecompWorkspace' not found in root project
```

说明你在使用 ForgeGradle 3（FG3）及以上版本，`setupDecompWorkspace` 已经不复存在，再执行也没用。

此时的正确做法是直接导入 IDEA 即可。
Eclipse 用户可能需要先执行 `./gradlew eclipse`，然后再导入 Eclipse。