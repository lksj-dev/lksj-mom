# IModelData

`forge`对于原版的扩充,基本可以理解为一个`Map<ModelProperty<T>,T>`  
原版未使用的地方,`forge`大多进行了`wrapper`,并传入一个`EmptyModelData.INSTANCE`  
```java
public interface IModelData
{
    /**
     * Check if this data has a property, even if the value is {@code null}. Can be
     * used by code that intends to fill in data for a render pipeline, such as the
     * forge animation system.
     * <p>
     * IMPORTANT: {@link #getData(ModelProperty)} <em>can</em> return {@code null}
     * even if this method returns {@code true}.
     * 
     * @param prop The property to check for inclusion in this model data
     * @return {@code true} if this data has the given property, even if no value is present
     */
    boolean hasProperty(ModelProperty<?> prop);

    @Nullable
    <T> T getData(ModelProperty<T> prop);
    
    @Nullable
    <T> T setData(ModelProperty<T> prop, T data);
}
```
`CTM`这种链接纹理,依靠的就是这个机制

和他一样很重要的是`ModelDataManager`,可以理解为带拥有缓存,刷新等机制的`Map<BlockPos,IModelData>`  
`forge`通过`IForgeBlockEntity`为`BlockEntiy`添加了  
`requestModelDataUpdate()`  
`default @Nonnull IModelData getModelData()`  