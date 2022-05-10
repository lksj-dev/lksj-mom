# 全局战利品表修改器[^全局战利品表修改器]概述  
*****
## 什么是全局战利品表修改器(GLM)  
&emsp;&emsp;全局战利品表修改器，简称GLM，是 Forge 为方便模组开发者修改战利品表而推出的“数据驱动”型战利品表修改工具。通过不同的战利品表修改器[^战利品表修改器]与不同的战利品表条件[^战利品表条件]组合来对所有满足特定条件的战利品表进行修改。  
&emsp;&emsp;这里需要明确一点：GLM 是“全局”和“数据驱动”的。这意味着GLM可以利用数据包对所有满足特定条件的战利品表进行修改。所以战利品表条件是起决定性作用的，你需要考虑“我应该在什么场合下修改怎么样的战利品表？”。  
***
## 如何使用现成的全局战利品表修改器  
&emsp;&emsp;使用GLM ，你需要在你的数据包内添加以下一些文件：
> 1. "data/forge/loot_modifiers/global_loot_modifiers.json"，用于选取数据包内需要加载的修改器，路径不可变。  
> 2. 一些已经序列化的修改器JSON文件，存储在"data/命名空间[^命名空间]/loot_modifiers"当中。  

&emsp;&emsp;"global_loot_modifiers.json"是用于选取数据包内修改器的**唯一方式**。它的JSON格式类似于标签。我们用一个示例文件为例来讲解它的格式。
```json
  {
    "replace": false, // 必要项
    "entries": [
      // 按以下目录选取修改器：'data/examplemod/loot_modifiers/example_glm.json'
      "examplemod:example_glm",
      "examplemod:example_glm2"
      // 此处可以添加更多的修改器...
    ]
  }
```
&emsp;&emsp;`replace`的取值代表本数据包是否会覆盖所有的GLM，如果为`true`则其他所有GLM都将**直接无效**。模组开发者建议最好不要选`true`以保证模组兼容性；整合包作者如有必要可以改为`true`来确保整合包稳定性。  
&emsp;&emsp;`entries`是该数据包需要加载的修改器的**有序表**，所有的修改器按照行数先后顺序加载。Forge会处理不同数据包里的冲突问题。  

一个序列化过的修改器JSON文件的格式如下。
```json  
{
  "type": "examplemod:example_loot_modifier",
  "conditions": [
    // 这里填写各种战利品表条件
    // ...
  ],
  "prop1": "val1",
  "prop2": 10,
  "prop3": "minecraft:dirt"
}
```  
&emsp;&emsp;其中`prop1`之类的类型是修改器具体的“参数”，它们并非必要项，而且根据该修改器的序列化器也会有所变化。比如有可能填写某个物品，或者填写一个代表特定战利品表的`ID`[^ID]。  
&emsp;&emsp;`type`是该战利品修改器的**序列器**的`ID`，用于决定这个修改器按照哪一种修改器类型对战利品表进行修改。不同的修改器允许使用同一种序列器。
&emsp;&emsp;`conditions`是该修改器起效的条件。所有条件在**大多数情况下**默认为“与”连接，也就是所有条件必须同时满足。你可以利用原版的条件完成“与或非”连接。
***
## 对于模组开发者而言没有现成！
&emsp;&emsp;很遗憾，Forge 虽然推出了 GLM 这个强大的工具，但是没有一个现成的修改器以供开发者们使用。这也是 GLM 饱受诟病的原因之一：大多数开发者**并不知道如何正确使用GLM。** 对于任何一个开发者而言，除非你有一个提供了现成实现的前置之外，**只能自己从头开始写一个修改器。** 值得庆幸的是，Forge 提供了一个修改器的抽象类：`LootModifier`类。   


[^全局战利品表修改器]: 暂译名，即Global Loot Modifier。   
[^战利品表修改器]: 暂译名，即Loot Modifier。  
[^战利品表条件]: 即Loot Condition，译名出自Minecraft中文维基[战利品表](https://minecraft.fandom.com/zh/wiki/%E6%88%98%E5%88%A9%E5%93%81%E8%A1%A8)。
[^命名空间]: 对于模组来说，命名空间一定等于modid。
[^ID]: 全称为命名空间ID，又称为资源路径（Resource location）。它是一个按照"命名空间:名称"格式的字符串。**每一个ID只能唯一对应一种资源！**
