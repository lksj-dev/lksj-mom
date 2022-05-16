# Colouring  

与物品一样,方块也可以染色,原理也一致,只不过接口变了而已  
```java
@OnlyIn(Dist.CLIENT)
public interface BlockColor {
   int getColor(BlockState pState, @Nullable BlockAndTintGetter pLevel, @Nullable BlockPos pPos, int pTintIndex);
}
```

但是方块与物品不同,不存在所谓的`BlockStack`,`BlockState`也无法支持任意颜色的方块存在  
因此,我们需要另外的载体,来存储方块所需的数据  

> 一定要使得模型的`BakedQuad`的**_tintindex_**不为默认值-1  

> 如有需要请调用`LevelRender#setBlocksDirty`  
> 否则方块的数据不会**_刷新_**  
> 会被阻拦在`LevelRender#compileChunks`内的`ChunkRenderDispatcher.RenderChunk#isDirty`  
> 详见[RenderChunk的Cache问题](../render/RenderChunk&Cache.md)

案例及出处可以参见[这里](https://zomb-676.github.io/CobaltDocs/#/render/blockModel?id=coloring)  

示例效果:  
![效果](https://zomb-676.github.io/CobaltDocs/picture/blockModel/colorfulBlock.gif)