`BaseEntityBlock` 默认覆写了
```java
public RenderShape getRenderShape(BlockState pState) {
   return RenderShape.INVISIBLE;
}
```
在自己继承的类改为
```java
@Override
public RenderShape getRenderShape(BlockState pState) {
    return RenderShape.MODEL;
}
```
即可