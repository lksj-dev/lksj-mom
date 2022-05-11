# Vertex  

mojang对整个过程进行了封装,顶点的容器被封装为`BufferBuilder`  
一个函数若同时拥有float/double和int类型的参数的重载,则表明其值范围不同
float/double表明参数需要`标准化/归一化`必须处于0-1,而int一般表明其值位于0-255  
接口`VertexConsumer`还继承自`IForgeVertexConsumer`,里面也是`balk`版本的函数

那么我们该如何获取我们想要的`VertexBuilder`呢?

借助`RenderType`我们可以通过`MultiBufferSource#getBuffer`  
前者若上下文无法获取,可以通过`Minecraft.getInstance().renderBuffers().bufferSource()`

也可以直接通过`Tesselator.getInstance().getBuilder()`或者直接使用`BufferBuilder`的构造函数  
在上传数据时候,前者通过`Tesselator#end`,后者需要`BufferBuilder#end`和`BufferUploader.end(buffer)`



这里给出一个提交数据的例子  
```kotlin
fun dataFill(event: RenderLevelLastEvent, buffer: VertexConsumer,block:Block) {
    val stack = event.poseStack
    val cameraPos = Minecraft.getInstance().gameRenderer.mainCamera.position
    stack.translate(-cameraPos.x, -cameraPos.y, -cameraPos.z)
    val playerPos = Minecraft.getInstance().player!!.blockPosition()
    val x = playerPos.x
    val y = playerPos.y
    val z = playerPos.z
    val pos = BlockPos.MutableBlockPos()
    for (dx in (x - 15)..(x + 15)) {
        pos.x = dx
        for (dy in (y - 15)..(y + 15)) {
            pos.y = dy
            for (dz in (z - 15)..(z + 15)) {
                pos.z = dz
                val blockState = Minecraft.getInstance().level!!.getBlockState(pos)
                if (blockState.block == block) {
                    stack.pushPose()
                    stack.translate(pos.x.toDouble(), pos.y.toDouble(), pos.z.toDouble())
                    val lastPose = stack.last().pose()

                    buffer.vertex(lastPose, 0f, 0f, 0f).color(1f, 0f, 0f, 0.75f).endVertex()
                    buffer.vertex(lastPose, 0f, 1f, 0f).color(0f, 1f, 0f, 0.75f).endVertex()
                    buffer.vertex(lastPose, 1f, 1f, 0f).color(1f, 1f, 1f, 0.75f).endVertex()
                    buffer.vertex(lastPose, 1f, 0f, 0f).color(1f, 1f, 1f, 0.75f).endVertex()

                    //                        buffer.vertex(lastPose.pose(),1f,0f,0f).color(1f,1f,1f,1f).endVertex()
                    //                        buffer.vertex(lastPose.pose(),1f,1f,0f).color(1f,1f,1f,1f).endVertex()
                    //                        buffer.vertex(lastPose.pose(),0f,1f,0f).color(1f,1f,1f,1f).endVertex()
                    //                        buffer.vertex(lastPose.pose(),0f,0f,0f).color(1f,0f,0f,1f).endVertex()
                    stack.popPose()
                }
            }
        }
    }
}
```

可以看到下方的注释块于上方仅有顺序上的差别  
原因在于顶点提交的数据决定了面的朝向,有时你需要改变递交的顺序来达到你想要的效果

详细介绍和出处可以参见[这里](https://zomb-676.github.io/CobaltDocs/#/render/vertexLife)