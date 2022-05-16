## ModelResourceLocation  

`ModelResourceLocation`,继承自`ResourceLocation`,与之相比多了一个名为`variant`的字段  
与`ResourceLocation`一样,同样拥有`namespace`和`path`字段  
在这里,前者表示模型所处的`命名空间`,即`modID`,而后者则对应所属物品/方块的`registryName`  
而`variant`对于物品,则为`inventory`  
对于方块,则描述了其`BlockState`,若没有BlockState,则为空字符串  
`toString`方法为`<namespace>:<registryName>#<variant>`  

想要拿到`BlockState`对应的`ModelResourceLocation`可以通过`BlockModelShaper#stateToModelLocation`  
物品则可通过`ModelResourceLocation(<item>.registryName, "inventory")`  