你可能因为某种奇怪的原因构建失败，并看到各种奇怪的报错，这可能是由于之前强行停止了 `Forge Gradle Task` 导致的（比如runClient构建到一半时强行停止），解决方法是找到 `C:/Users/user/.gradle/caches/forge_gradle` 文件夹并删除（注意，它并不在项目文件夹下面），然后重新导入项目即可。
