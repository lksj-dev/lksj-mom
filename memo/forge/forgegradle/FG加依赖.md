```groovy
buildscript {
    // 这里面不要碰！
}

respositories {
    // 在这里加依赖所在的仓库，请根据实际情况填写！
    maven {
        url 'https://fake.repo.invalid/'
    }
}

dependencies {
    // 如果你的依赖是一个正常的 Mod，这样就够了
    // 不要再把你的 Mod 丢进 run/mods 目录下了！丢进 run/mods 没用的！
    implementation fg.deobf('这里换成那个依赖项的 maven coordiante，那个项目肯定会给你这个')
}

// 但如果你的依赖并不是 Mod，而是一般的 jar，会比较麻烦，你需要下面两个东西：
configurations {
    library
	implementation.extendsFrom library
}

minecraft.runs.all {
	lazyToken('minecraft_classpath') {
		configurations.library.copyRecursive().resolve().collect { it.absolutePath }.join(File.pathSeparator)
	}
}

dependencies {
    // 然后这样就可以正常在开发环境使用不是 Mod 的 jar 包了
    library '这里换成那个依赖项的 maven coordiante'
}

publish {
    // 这里面不要碰！
}
```