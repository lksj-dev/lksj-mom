# BlockState

打开游戏,按下f3,可以看到右侧的`Targeted Block`和`Targeted Fluid`下,除了显示所指向的方块名称
在以`#`为标识的`Tag`之上,有的方块/流体还显示了一些别的信息,这就是`BlockState`  

在Minecraft内创建世界的时候,有一种隐藏的世界类型称之为`debug mode`,见[wiki](https://minecraft.fandom.com/wiki/Debug_mode)  
里面枚举所有方块/流体的BlockState  

想要为你的方块添加`BlockState`,你需要复写`protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> pBuilder)`  
原版已定义的在类`BlockStateProperties`内,可以直接引用  

若你想创建自己的BlockState,可以选择实现抽象类`net.minecraft.world.level.block.state.properties.Property>`  
当然,原版已经有特化实现`BooleanProperty`,`DirectionProperty`,`EnumProperty`,`IntegerProperty`  

> 方块所持有的`BlockState`会在加载模型时候,穷举其所有排列组合,即笛卡尔积  
> 请确保其枚举总可能结果数量在一个合理的范围内

`BlockState`的切换需要你手动设置,可以覆写诸如    
`getStateForPlacement`在放置时设置  
`neighborChanged`毗邻方块更新时设置  
`updateIndirectNeighbourShapes`,`updateShape`等