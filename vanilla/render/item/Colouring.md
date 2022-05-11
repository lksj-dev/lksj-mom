# Colouring  

Minecraft为物品提供了一种染色的方式  
```java
@OnlyIn(Dist.CLIENT)
public interface ItemColor {
   int getColor(ItemStack pStack, int pTintIndex);
}
```
利用此接口,返回值为`rgb`,`pTintIndex`为`json`模型内参数  

注册通过`ItemColors.register(ItemColor pItemColor, ItemLike... pItems)`  

具体原理为:在提交渲染的最小抽象单位`BakedQuad`前,mc会对`TintIndex`判断,默认情况下,若是不为默认值`-1`则会调用物品对应的`ItemColor#getColor`  

所以我们可以通过将颜色信息存储在`ItemStack`中,被调用`getColor`时,从中获得颜色信息并返回

案例及详细介绍和出处可以参见[这里](https://zomb-676.github.io/CobaltDocs/#/render/itemModel?id=colouring)

案例效果  
![效果](https://zomb-676.github.io/CobaltDocs/picture/itemModel/colorfulChalk.gif)