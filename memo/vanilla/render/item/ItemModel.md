# ItemModel  

minecraft[wiki](https://minecraft.fandom.com/zh/wiki/%E6%A8%A1%E5%9E%8B#.E7.89.A9.E5.93.81.E6.A8.A1.E5.9E.8B)描述

### Use Block Model  

**_方块对应的物品默认是没有材质的_**  
如果你的物品想要使用方块的模型,例如`BlockItem`的物品模型  
可以直接让`parent`指向方块对应的模型,格式:`<nameSpace>:block/<blockRegisterName>`,`<>`内为根据实际填写的字段  

### Use 3D Model  

如果你想让你的物品使用`BlockBench`生成的模型  
可以直接将`BlockBench`导出的文件命名为`<itemRegistryName>`  
或者将`parent`设置为`<nameSpace>:item/<blockRegisterName>`

### Layer Model  

mc自带的一种生成模型的方式,一多层的`Layer`叠加,为物品生成模型
可以查看`forge`对原版的扩展,在`ItemLayerModel`内,扩展了原版仅支持4个`layer`至无限  

案例及详细介绍和出处可以参见[这里](https://zomb-676.github.io/CobaltDocs/#/render/itemModel?id=_3d-json-model)

示例效果:  
![效果](https://zomb-676.github.io/CobaltDocs/picture/itemModel/empty.png)