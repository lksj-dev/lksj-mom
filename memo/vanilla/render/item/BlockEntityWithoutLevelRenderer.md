# BlockEntityWithoutLevelRenderer  

如果你需要更加动态的渲染物品或者物品的渲染需要和使用了`BlockEntityRender`的方块渲染效果一致    
那么你需要的是名为`BlockEntityWithoutLevelRenderer`,曾叫做`ItemStackTileEntityRenderer`  
以代码的方式进行渲染,做到你想要的一切  

首先要让MC知道你的物品模型需要`BlockEntityWithoutLevelRenderer`,这需要你的`BakedModel.isCustomRenderer`返回`true`  

因为在`ItemRender#render`内,会以此作为判断

而要实现这一目标,给出两种办法  

一种是让你的`json`模型,直接或间接继承自`builtin/entity`,原因如下  

在`ModelBakery#loadBlockModel`中,如果你的物品模型,继承自`builtin/entity`  
你的模型就会被读取为一个名为`BLOCK_ENTITY_MARKER`的`BlockModel/UnbakedModel`  
在`BlockModel#bakeVanilla`,模型就会被`bake`为`BuiltInModel`,它的`isCustomRender()`返回就为`true`  

另一种就是在`ModelBakeEvent`中进行替换,同上文替换`overrides`一致  

当然你也可以和上文一样,直接定义一个`IModelLoader`走一个模型加载的全套流程  

这样,只要给你的物品复写`public void initializeClient(Consumer<IItemRenderProperties> consumer)`  
给传入的`consumer`传入一个复写了`BlockEntityWithoutLevelRenderer getItemStackRenderer()`的`IItemRenderProperties`即可  
不然则会默认返回`BlockEntityWithoutLevelRenderer(blockEntityRenderDispatcher,/*EntityModelSet*/ entityModels)`  

通过以上操作,物品在渲染时候就会调用你传入的`BlockEntityWithoutLevelRender#renderByItem`  
