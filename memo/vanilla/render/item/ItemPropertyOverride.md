# Item Property Override

原版提供了一种名为`overrides`的机制,可以通过一定的上下文,从有限数目的模型中指定一个进行渲染  

调用`ItemProperties.register(Item pItem, ResourceLocation pName, ItemPropertyFunction pProperty)`  
第一个参数`pItem`即需要绑定的物品  
第二个参数`pName`指的是`overrides`的名称,原版的有[这些](https://minecraft.fandom.com/zh/wiki/%E6%A8%A1%E5%9E%8B#.E7.89.A9.E5.93.81.E6.A0.87.E7.AD.BE.E8.B0.93.E8.AF.8D)  
第三个参数就是给定上下文,返回模型的地方了  

```java
@Deprecated
@OnlyIn(Dist.CLIENT)
public interface ItemPropertyFunction {
   float call(ItemStack pStack, @Nullable ClientLevel pLevel, @Nullable LivingEntity pEntity, int pSeed);
}

@OnlyIn(Dist.CLIENT)
public interface ClampedItemPropertyFunction extends ItemPropertyFunction {
   /** @deprecated */
   @Deprecated
   default float call(ItemStack pStack, @Nullable ClientLevel pLevel, @Nullable LivingEntity pEntity, int pSeed) {
      return Mth.clamp(this.unclampedCall(pStack, pLevel, pEntity, pSeed), 0.0F, 1.0F);
   }

   float unclampedCall(ItemStack pStack, @Nullable ClientLevel pLevel, @Nullable LivingEntity pEntity, int pSeed);
}
```

我们应该使用下面那个函数式接口  

第三个参数pSeed,部分传入为`0`,部分为`ItemEntity的ID`  
理论上也可以自己随意使用  

案例及详细介绍和出处可以参见[这里](https://zomb-676.github.io/CobaltDocs/#/render/itemModel?id=overrides)

案例效果  
![example](https://zomb-676.github.io/CobaltDocs/picture/itemModel/weather_indicator.gif)