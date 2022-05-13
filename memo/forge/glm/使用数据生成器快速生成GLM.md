# 使用数据生成器快速生成GLM   
***
## `GlobalLootModifierProvider`类
&emsp;&emsp;数据生成器需要一个“供应商”——`Provider`，所以我们来写一个GLM的“供应商”。  
```java
public class GLMProvider extends GlobalLootModifierProvider {
    public GLMProvider(DataGenerator gen, String modid) {
        super(gen, modid);
    }

    @Override
    protected void start() {
    }
}
```
&emsp;&emsp;这就是一个最简单的“供应商”了。要想添加一个新的需要生成数据的修改器，只需要在`start`方法中调用`add`方法就可以了。Forge 提供的示例代码如下。  
```java
this.add("example_modifier", EXAMPLE_MODIFIER_SERIALIZER, new ExampleModifier(
  new LootItemCondition[] {
    WeatherCheck.weather().setRaining(true).build() // 雨天生效
  },
  "val1", // "prop1=val1"
  10, // "prop2=10"
  Items.DIRT // "prop3=minecraft:dirt"
));
```
&emsp;&emsp;从上面的代码中我们可以看出`add`方法总共有三个参数：第一个字符串参数代表最终生成结果的ID的“path”；第二个则是该修改器序列化器的实例，如果你注册规范的话直接获取实例就可以使用了；第三个则是一个该修改器的实例，直接创建新实例就可以了。 
***
## 战利品表条件数组  
&emsp;&emsp;战利品表条件是有序加载的。
> &emsp;&emsp;如果你要表示**同时满足所有条件**完成与连接，直接添加一个数组元素就可以了。通常来说你的修改器继承的都是`LootModifier`类，所以他们一定是并列关系。  
> &emsp;&emsp;如果你要表示**满足任一条件**完成或连接，则在你的元素中调用`or`方法嵌套一个条件，生成器会自动转换。  
> &emsp;&emsp;条件可以组合使用**与或连接**。  
> &emsp;&emsp;如果你的情况比较特殊，则根据你的实际情况进行处理。  
