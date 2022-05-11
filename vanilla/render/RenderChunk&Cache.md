# RenderChunk的缓存问题

`ChunkRenderDispatcher.RenderChunk`存在一个缓存机制,仅在内部变量`dirty`被设置后才会更新  
如果不依赖`BlockState`变化想要使用`BlockColor`会遇到无法即使更新的情况  
对单个方块进行`dirty`标记的方法为`LevelRender#setBlockDirty`如下

```java
public void setBlockDirty(BlockPos pPos, BlockState pOldState, BlockState pNewState) {
   if (this.minecraft.getModelManager().requiresRender(pOldState, pNewState)) {
      this.setBlocksDirty(pPos.getX(), pPos.getY(), pPos.getZ(), pPos.getX(), pPos.getY(), pPos.getZ());
   }
}
```
可以看到判断新旧`BlockState`所需的模型是否相等,在这里我们按照它的调用方式调用  
`setBlocksDirty(int pMinX, int pMinY, int pMinZ, int pMaxX, int pMaxY, int pMaxZ)`  
即可标记`dirty`

同理的还有`dirty` `section`的方法