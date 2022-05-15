在Mod的开发过程中我们往往需要阅读大量的Minecraft代码，但是mojang放出的**offcial mappings**并没有给出参数名的映射，于是在阅读代码时就会遇见如下面这样的代码：

`private void addMessage(Component p_93791_, int p_93792_, int p_93793_, boolean p_93794_)`

这样的参数名字是不可读的，而**Parchment**正是这样一个用来反混淆参数名的项目
你只需依照[这里](https://github.com/ParchmentMC/Librarian/blob/dev/docs/FORGEGRADLE.md)的做法更改你的**build.gradle**,然后reload你的gradle项目就可以看见你的参数拥有了可读的参数命名
不过仍然要注意的是**Parchment**的反混淆是人工进行，并不能保证每个地方的参数命名都被反混淆了