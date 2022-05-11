# RenderType

[原帖](https://zomb-676.github.io/CobaltDocs/#/render/renderType)支持更多的渲染样式

`RenderType`可以说是mc渲染中最为重要的一部分,而它实际上是一些列对于`OpenGL context`操作的合集

处于继承树顶层的`RenderStateShard`拥有三个字段,`String name`,`Runnable setupState`,`Runnable clearState`  
正如起名,`setupState`,`clearState`分别在`renderType`配合调用`drawCall`前后被调用,用于便利的控制`opengl context`  
其他的派生类只是对所需改变上下文所需字段的特化

## overview table

| class/instance name        | name                     | extra/comment                                                                                     |
|----------------------------|--------------------------|---------------------------------------------------------------------------------------------------|
| **DepthTestStateShard**    | **depth_test**           | **String functionName**                                                                           |
| NO_DEPTH_TEST              |                          | functionName:always                                                                               |
| EQUAL_DEPTH_TEST           |                          | functionName:==                                                                                   |
| LEQUAL_DEPTH_TEST          |                          | functionName:<=                                                                                   |
| **LineStateShard**         | **line_width**           | **OptionalDouble width**                                                                          |
| DEFAULT_LINE               |                          | width:1.0                                                                                         |
| **ShaderStateShard**       | **shader**               | **Optional<Supplier<ShaderInstance>> shader**                                                     |
| **TransparencyStateShard** |                          |                                                                                                   |
| NO_TRANSPARENCY            | no_transparency          |                                                                                                   |
| ADDITIVE_TRANSPARENCY      | additive_transparency    | blendFunc(SRC.ONE,DEST.ONE)                                                                       |
| LIGHTNING_TRANSPARENCY     | lightning_transparency   | blendFunc(SRC.SRC_ALPHA,DEST.ONE)                                                                 |
| GLINT_TRANSPARENCY         | glint_transparency       | blendFuncSeparate<br/>SRC.SRC_COLOR,DEST.ONE<br/>SRC.ZERO,DEST.ONE                                |
| CRUMBLING_TRANSPARENCY     | crumbling_transparency   | blendFuncSeparate<br/>DEST.DST_COLOR,DEST.PME<br/>SRC.ONE,DEST.ZERO                               |
| TRANSLUCENT_TRANSPARENCY   | translucent_transparency | blendFuncSeparate<br/>SRC.SRC_ALPHA,DEST.ONE_MINUS_SRC_ALPHA<br/>SRC.ONE,DEST.ONE_MINUS_SRC_ALPHA |
| **WriteMaskStateShard**    | **write_mask_state**     | **boolean writeColor<br>boolean writeDepth**                                                      |
| COLOR_DEPTH_WRITE          |                          | writeColor:true<br/>writeDepth:true                                                               |
| COLOR_WRITE                |                          | writeColor:true<br/>writeDepth:false                                                              |
| DEPTH_WRITE                |                          | writeColor:false<br/>writeDepth:true                                                              |
| **OutputStateShard**       |                          |                                                                                                   |
| MAIN_TARGET                | main_target              | getMainRenderTarget()                                                                             |
| OUTLINE_TARGET             | outline_target           | levelRenderer.entityTarget()                                                                      |
| TRANSLUCENT_TARGET         | translucent_target       | levelRenderer.getTranslucentTarget()                                                              |
| PARTICLES_TARGET           | particles_target         | levelRenderer.getParticlesTarget()                                                                |
| WEATHER_TARGET             | weather_target           | levelRenderer.getWeatherTarget()                                                                  |
| CLOUDS_TARGET              | clouds_target            | levelRenderer.getCloudsTarget()                                                                   |
| ITEM_ENTITY_TARGET         | item_entity_target       | levelRenderer.getItemEntityTarget()                                                               |
| **LayeringStateShard**     |                          |                                                                                                   |
| NO_LAYERING                | no_layering              |                                                                                                   |
| POLYGON_OFFSET_LAYERING    | polygon_offset_layering  | polygonOffset(factor:-1.0F,units:-10.0F)                                                          |
| VIEW_OFFSET_Z_LAYERING     | view_offset_z_layering   | scale(x:0.99975586F,y:0.99975586F,z:0.99975586F)                                                  |
| **EmptyTextureStateShard** | **texture**              | **Optional<ResourceLocation> cutoutTexture()**                                                    |
| NO_TEXTURE                 |                          |                                                                                                   |
| **MultiTextureStateShard** |                          |                                                                                                   |
| **TextureStateShard**      |                          | **Optional<ResourceLocation> texture<br/>boolean blur<br/>boolean mipmap**                        |
| BLOCK_SHEET_MIPPED         |                          | texture:TextureAtlas.LOCATION_BLOCKS<br/>blur:false<br/>mipmap:true                               |
| BLOCK_SHEET                |                          | texture:TextureAtlas.LOCATION_BLOCKS<br/>blur:false<br/>mipmap:false                              |
| **TexturingStateShard**    |                          |                                                                                                   |
| DEFAULT_TEXTURING          | default_texturing        |                                                                                                   |
| GLINT_TEXTURING            | glint_texturing          | setupGlintTexturing(8.0F);                                                                        |
| ENTITY_GLINT_TEXTURING     | entity_glint_texturing   | setupGlintTexturing(0.16F);                                                                       |
| OffsetTexturingStateShard  | offset_texturing         |                                                                                                   |
| **BooleanStateShard**      |                          | **bool enabled**                                                                                  |
| **CullStateShard**         | **cull**                 | **bool useCull**                                                                                  |
| CULL                       |                          | useCull:true                                                                                      |
| NO_CULL                    |                          | useCull:false                                                                                     |
| **LightmapStateShard**     | **lightmap**             | **bool useLightMap**                                                                              |
| LIGHTMAP                   |                          | useLightMap:true                                                                                  |
| NO_LIGHTMAP                |                          | useLightMap:false                                                                                 |
| **OverlayStateShard**      | **overlay**              | **bool useLightmap**                                                                              |
| OVERLAY                    | overlay                  | useLightmap:true                                                                                  |
| NO_OVERLAY                 | overlay                  | useLightmap:false                                                                                 |

`CompositeState`正是每种`RenderStateShard`合集,mj还提供了`CompositeStateBuilder`用`Builder模式`来构造对象  
而`RenderType`则是`VertexFormat`,`bufferSize`,`CompositeState`的合集  

## example

利用`RenderType`简化上次的代码

```kotlin
@Suppress("unused")
@Mod.EventBusSubscriber(Dist.CLIENT)
object VertexFillByRenderType {

    private class RenderTypeHolder : RenderType("any", DefaultVertexFormat.POSITION_COLOR, VertexFormat.Mode.QUADS, 256, false, false, {}, {}) {
        companion object {
            @Suppress("INACCESSIBLE_TYPE")
            val renderType: RenderType = create(
                "posColorRenderType", DefaultVertexFormat.POSITION_COLOR, VertexFormat.Mode.QUADS, 256, false, false,
                CompositeState.builder()
                    .setShaderState(POSITION_COLOR_SHADER)
                    .setCullState(NO_CULL)
                    .setDepthTestState(NO_DEPTH_TEST)
                    .setTransparencyState(TRANSLUCENT_TRANSPARENCY)
                    .createCompositeState(false)
            )
        }
    }

    @SubscribeEvent
    @JvmStatic
    fun renderLevelLastEvent(event: RenderLevelLastEvent) {
        if (Minecraft.getInstance().player!!.mainHandItem.item != Items.ANVIL) {
            return
        }
        val bufferSource = Minecraft.getInstance().renderBuffers().bufferSource()
        val buffer = bufferSource.getBuffer(RenderTypeHolder.renderType)
        dataFill(event,buffer,Blocks.ANVIL)
        RenderSystem.disableDepthTest()
        bufferSource.endBatch(RenderTypeHolder.renderType)
    }
}
```

> 这里我们使用一个`RenderTypeHolder`  
> 是因为许多需要使用的字段访问级别仅为`protected`  
> 通过继承父类来暴露`protected`  
> 所以`holder`并不会被构造  

可以看到调用处,还是简洁了不少  
请无视最后的`RenderSystem.disableDepthTest()`,为什么有这个我折叠了,正常是不需要的

<details>
<summary>为什么呢</summary>

```java
public static class DepthTestStateShard extends RenderStateShard {
    private final String functionName;

    public DepthTestStateShard(String pFunctionName, int pDepthFunc) {
        super("depth_test",/*setupState*/ () -> {
            if (pDepthFunc != GL_ALWAYS) {
                RenderSystem.enableDepthTest();
                RenderSystem.depthFunc(pDepthFunc);
            }

        }, /*clearState*/ () -> {
            if (pDepthFunc != GL_ALWAYS) {
                RenderSystem.disableDepthTest();
                RenderSystem.depthFunc(GL_LEQUAL);
            }
        });
        this.functionName = pFunctionName;
    }

    public String toString() {
       return this.name + "[" + this.functionName + "]";
    }
}

protected static final RenderStateShard.DepthTestStateShard NO_DEPTH_TEST 
    = new RenderStateShard.DepthTestStateShard("always", GL_ALWAYS);

```
可以看到,对于`NO_DEPTH_TEST`,实际上就是...什么都不做  
这就导致`DisableDepthTest`的调用,完全取决于使用`RenderType`或者在手动调用`enable`后再次`disable`  
然后在笔者所处的环境中...mj没有配对的调用`disable`,只能手动添加

</details>

## bufferSource & batch

从调用的函数名`endBatch`暗示了`RenderType`配合`BufferSource`其实是用于批量渲染的  

```java
@OnlyIn(Dist.CLIENT)
public interface MultiBufferSource {
   static MultiBufferSource.BufferSource immediate(BufferBuilder pBuilder) {
      return immediateWithBuffers(ImmutableMap.of(), pBuilder);
   }

   static MultiBufferSource.BufferSource immediateWithBuffers(Map<RenderType, BufferBuilder> pMapBuilders, BufferBuilder pBuilder) {
      return new MultiBufferSource.BufferSource(pBuilder, pMapBuilders);
   }

   VertexConsumer getBuffer(RenderType pRenderType);

   @OnlyIn(Dist.CLIENT)
   public static class BufferSource implements MultiBufferSource {
      protected final BufferBuilder builder;
      protected final Map<RenderType, BufferBuilder> fixedBuffers;
      protected Optional<RenderType> lastState = Optional.empty();
      protected final Set<BufferBuilder> startedBuffers = Sets.newHashSet();

      protected BufferSource(BufferBuilder pBuilder, Map<RenderType, BufferBuilder> pFixedBuffers) {
         this.builder = pBuilder;
         this.fixedBuffers = pFixedBuffers;
      }

      public VertexConsumer getBuffer(RenderType pRenderType) {
         Optional<RenderType> optional = pRenderType.asOptional();
         BufferBuilder bufferbuilder = this.getBuilderRaw(pRenderType);
         if (!Objects.equals(this.lastState, optional)) {
            if (this.lastState.isPresent()) {
               RenderType rendertype = this.lastState.get();
               if (!this.fixedBuffers.containsKey(rendertype)) {
                  this.endBatch(rendertype);
               }
            }

            if (this.startedBuffers.add(bufferbuilder)) {
               bufferbuilder.begin(pRenderType.mode(), pRenderType.format());
            }

            this.lastState = optional;
         }

         return bufferbuilder;
      }

      private BufferBuilder getBuilderRaw(RenderType pRenderType) {
         return this.fixedBuffers.getOrDefault(pRenderType, this.builder);
      }
   }
}
```

可以发现,如果我们传入的`renderType`包含在`pMapBuilders/fixedBuffer`内,那么每次拿到的`BufferBuilder`  
便是该`renderType`独占的,达到`batch`的效果  
否则,将会共享`pBuilder`,并且还会直接`endBatch`上一次对应的`renderType`和`bufferBuilder`避免污染  

<details>
<summary>fixedBuffer</summary>

```java
	private final SortedMap<RenderType, BufferBuilder> fixedBuffers = Util.make(new Object2ObjectLinkedOpenHashMap<>(), (map) -> {
		map.put(Sheets.solidBlockSheet(), this.fixedBufferPack.builder(RenderType.solid()));
		map.put(Sheets.cutoutBlockSheet(), this.fixedBufferPack.builder(RenderType.cutout()));
		map.put(Sheets.bannerSheet(), this.fixedBufferPack.builder(RenderType.cutoutMipped()));
		map.put(Sheets.translucentCullBlockSheet(), this.fixedBufferPack.builder(RenderType.translucent()));
		put(map, Sheets.shieldSheet());
		put(map, Sheets.bedSheet());
		put(map, Sheets.shulkerBoxSheet());
		put(map, Sheets.signSheet());
		put(map, Sheets.chestSheet());
		put(map, RenderType.translucentNoCrumbling());
		put(map, RenderType.armorGlint());
		put(map, RenderType.armorEntityGlint());
		put(map, RenderType.glint());
		put(map, RenderType.glintDirect());
		put(map, RenderType.glintTranslucent());
		put(map, RenderType.entityGlint());
		put(map, RenderType.entityGlintDirect());
		put(map, RenderType.waterMask());
		ModelBakery.DESTROY_TYPES.forEach((item) -> {
		   put(map, item);
		});
	});
```

</details>

至于`endBatch`则会调用`RenderType`内的如下方法  
`setupState`->`BufferUploader.end(buffer)`->`clearState`  

```java
public void end(BufferBuilder pBuffer, int pCameraX, int pCameraY, int pCameraZ) {
   if (pBuffer.building()) {
      if (this.sortOnUpload) {
         pBuffer.setQuadSortOrigin((float)pCameraX, (float)pCameraY, (float)pCameraZ);
      }

      pBuffer.end();
      this.setupRenderState();
      BufferUploader.end(pBuffer);
      this.clearRenderState();
   }
}
```

## blockEntityRender

大致过程如下,摘自`LevelRender#renderLevel`  

#### **BlockEntity in frustum**
```java
for(LevelRenderer.RenderChunkInfo levelrenderer$renderchunkinfo : this.renderChunksInFrustum) {
   List<BlockEntity> list = levelrenderer$renderchunkinfo.chunk.getCompiledChunk().getRenderableBlockEntities();
   if (!list.isEmpty()) {
      for(BlockEntity blockentity1 : list) {
         if(!frustum.isVisible(blockentity1.getRenderBoundingBox())) continue;
         BlockPos blockpos4 = blockentity1.getBlockPos();
         MultiBufferSource multibuffersource1 = multibuffersource$buffersource;
         pPoseStack.pushPose();
         pPoseStack.translate((double)blockpos4.getX() - d0, (double)blockpos4.getY() - d1, (double)blockpos4.getZ() - d2);
         SortedSet<BlockDestructionProgress> sortedset = this.destructionProgress.get(blockpos4.asLong());
         if (sortedset != null && !sortedset.isEmpty()) {
            int j1 = sortedset.last().getProgress();
            if (j1 >= 0) {
               PoseStack.Pose posestack$pose1 = pPoseStack.last();
               VertexConsumer vertexconsumer = new SheetedDecalTextureGenerator(this.renderBuffers.crumblingBufferSource().getBuffer(ModelBakery.DESTROY_TYPES.get(j1)), posestack$pose1.pose(), posestack$pose1.normal());
               multibuffersource1 = (p_194349_) -> {
                  VertexConsumer vertexconsumer3 = multibuffersource$buffersource.getBuffer(p_194349_);
                  return p_194349_.affectsCrumbling() ? VertexMultiConsumer.create(vertexconsumer, vertexconsumer3) : vertexconsumer3;
               };
            }
         }

         this.blockEntityRenderDispatcher.render(blockentity1, pPartialTick, pPoseStack, multibuffersource1); //!!!
         pPoseStack.popPose();
      }
   }
}
```
#### **Global BlockEntity**
```java
synchronized(this.globalBlockEntities) {
   for(BlockEntity blockentity : this.globalBlockEntities) {
      if(!frustum.isVisible(blockentity.getRenderBoundingBox())) continue;
      BlockPos blockpos3 = blockentity.getBlockPos();
      pPoseStack.pushPose();
      pPoseStack.translate((double)blockpos3.getX() - d0, (double)blockpos3.getY() - d1, (double)blockpos3.getZ() - d2);
      this.blockEntityRenderDispatcher.render(blockentity, pPartialTick, pPoseStack, multibuffersource$buffersource); 
      //!! 这里就会调用我们写的BlockEntityRender内的render方法
      pPoseStack.popPose();
   }
}
```
#### **batch render**
```java
this.checkPoseStack(pPoseStack);
multibuffersource$buffersource.endBatch(RenderType.solid()); //?
multibuffersource$buffersource.endBatch(RenderType.endPortal());
multibuffersource$buffersource.endBatch(RenderType.endGateway());
multibuffersource$buffersource.endBatch(Sheets.solidBlockSheet());
multibuffersource$buffersource.endBatch(Sheets.cutoutBlockSheet());
multibuffersource$buffersource.endBatch(Sheets.bedSheet());
multibuffersource$buffersource.endBatch(Sheets.shulkerBoxSheet());
multibuffersource$buffersource.endBatch(Sheets.signSheet());
multibuffersource$buffersource.endBatch(Sheets.chestSheet());
```

一种`RenderType`被`endBatch`应该仅代表在此之后,本帧不会在使用??


## normal block

---

### special? not special

相信各位都见过  

#### **TheGreyGhost**
![chunkBufferLayers](../picture/renderType/chunkBufferLayers.png)  
来自[TheGreyGhost](https://greyminecraftcoder.blogspot.com/2020/04/block-rendering-1144.html)  
#### **3T**
![chunkBufferLayers](../picture/renderType/blockRenderType.png)
  
并且配合`ItemBlockRenderTypes#setRenderLayer`或者层叫做`RenderTypeLookup#setRenderLayer`的方法为流体/方块设置`RenderLayer`?  
但是,这里的参数确实是`RenderType`啊,这几个并没有什么特殊的啊  
确实如此,但真正特殊的其实在于它们被渲染的代码块  
大多数时候,我们只关心于`entity`.`blockEntity`,`gui`的渲染,它们的数量与遍布每个角落的渲染方式与之相比平平无奇的方块少的多的多  
面对这种较大的数量级,mj对于它们采用了特殊的方式  

`RenderType`类内
```java
public static List<RenderType> chunkBufferLayers() {
	return ImmutableList.of(solid(), cutoutMipped(), cutout(), translucent(), tripwire());
}
```
<details>
<summary>关于tripwire</summary>

好像在以前是没有的  
在尚未有`RenderType`的的1.12.2,前面四个都放在一个叫做`BlockRenderLayer`的枚举类中  
此时,tripwire方块的的renderLayer为`BlockRenderLayer.TRANSLUCENT;`  
在1.16.5,mcp表这个方法叫做`getBlockRenderTypes`就存在`tripwire`  
而forge的`multiLayerModel`中最早提早有相关信息的在[这里](https://github.com/MinecraftForge/MinecraftForge/blob/ce3d8b40cf37924caf1708cdde6842ae6fdcee31/src/main/java/net/minecraftforge/client/model/MultiLayerModel.java#L247)  
里面就已经包含了有关内容,但那次提交所处时间位于1.16.4与1.16.5之间  
在1.18.1,对`translucent`和`tripwire`进行对比,可以发现除了`bufferSize`,`outputState`,`vsh`有非常小的差别外,一模一样  

</details>

可以看到,它们与区块的渲染有密切相关

### concrete

仅列出与提交数据有关的部分

```java
profilerfiller.popPush("terrain_setup");
this.setupRender(pCamera, frustum, pHasCapturedFrustrum, this.minecraft.player.isSpectator());
profilerfiller.popPush("compilechunks");
this.compileChunks(pCamera);
profilerfiller.popPush("terrain");
this.renderChunkLayer(RenderType.solid(), pPoseStack, cameraX, camerY, cameraZ, pProjectionMatrix);
this.minecraft.getModelManager().getAtlas(TextureAtlas.LOCATION_BLOCKS).setBlurMipmap(false, this.minecraft.options.mipmapLevels > 0); // FORGE: fix flickering leaves when mods mess up the blurMipmap settings
this.renderChunkLayer(RenderType.cutoutMipped(), pPoseStack, cameraX, camerY, cameraZ, pProjectionMatrix);
this.minecraft.getModelManager().getAtlas(TextureAtlas.LOCATION_BLOCKS).restoreLastBlurMipmap();
this.renderChunkLayer(RenderType.cutout(), pPoseStack, cameraX, camerY, cameraZ, pProjectionMatrix);
```

`this.renderChunkLayer(RenderType.solid(), pPoseStack, d0, d1, d2, pProjectionMatrix);`  
这是最终调用`drawCall`的部分  

最关键的一步在于`this.compileChunks(pCamera);`

<details>
<summary>相关内容,可不看</summary>

罗列一车与渲染有关的chunk类  
`static`前缀表明这是一个静态内部类,构造时,无需外部类,内部不含外部类引用

| class name                                 | field/method                                                  | description                             |
|--------------------------------------------|---------------------------------------------------------------|-----------------------------------------|
| RenderRegionCache                          | Long2ObjectMap<RenderRegionCache.ChunkInfo> chunkInfoCache    | long:ChunkPos.asLong()                  |
| static RenderRegionCache.ChunkInfo         | LevelChunk chunk                                              | map entry?                              |
|                                            | RenderChunk renderChunk                                       |                                         |
| RenderChunk                                | Map<BlockPos, BlockEntity> blockEntities                      |                                         |
|                                            | List<PalettedContainer<BlockState>> sections                  |                                         |
|                                            | boolean debug                                                 |                                         |
|                                            | LevelChunk wrapped                                            |                                         |
|                                            | BlockEntity getBlockEntity(BlockPos)                          |                                         |
|                                            | BlockState getBlockState(BlockPos)                            |                                         |
| RenderChunkDispatcher.RenderChunk          | static final int SIZE = 16                                    |                                         |
|                                            | final int index                                               |                                         |
|                                            | AtomicInteger initialCompilationCancelCount                   |                                         |
|                                            | ChunkRenderDispatcher.RenderChunk.RebuildTask lastRebuildTask |                                         |
|                                            | ChunkRenderDispatcher.RenderChunk.ResortTransparencyTask      |                                         |
|                                            | Set<BlockEntity> globalBlockEntities                          |                                         |
|                                            | Map<RenderType, VertexBuffer> buffers                         |                                         |
| static RenderChunkDispatcher.CompiledChunk | ChunkRenderDispatcher.CompiledChunk UNCOMPILED                |                                         |
|                                            | Set<RenderType> hasBlocks                                     |                                         |
|                                            | Set<RenderType> hasLayer                                      |                                         |
|                                            | boolean isCompletelyEmpty                                     |                                         |
|                                            | List<BlockEntity> renderableBlockEntities                     |                                         |
|                                            | BufferBuilder.SortState transparencyState                     |                                         |
| static LevelRender.RenderInfoMap           | LevelRenderer.RenderChunkInfo[] infos                         | ChunkRenderDispatcher.RenderChunk.index |
| static LevelRender.RenderChunkStorage      | LevelRenderer.RenderInfoMap renderInfoMap                     |                                         |
|                                            | LinkedHashSet<LevelRenderer.RenderChunkInfo> renderChunks     |                                         |
| static LevelRender.RenderChunkInfo         | ChunkRenderDispatcher.RenderChunk chunk                       |                                         |
|                                            | byte sourceDirections                                         |                                         |
|                                            | byte directions                                               |                                         |
|                                            | int step                                                      |                                         |

```java
private void compileChunks(Camera camera) {
   this.minecraft.getProfiler().push("populate_chunks_to_compile");
   RenderRegionCache renderregioncache = new RenderRegionCache();
   BlockPos blockpos = camera.getBlockPosition();
   List<ChunkRenderDispatcher.RenderChunk> list = Lists.newArrayList();

   for(LevelRenderer.RenderChunkInfo levelrenderer$renderchunkinfo : this.renderChunksInFrustum) {
      ChunkRenderDispatcher.RenderChunk chunkrenderdispatcher$renderchunk = levelrenderer$renderchunkinfo.chunk;
      ChunkPos chunkpos = new ChunkPos(chunkrenderdispatcher$renderchunk.getOrigin());
      if (chunkrenderdispatcher$renderchunk.isDirty() && this.level.getChunk(chunkpos.x, chunkpos.z).isClientLightReady()) {
         boolean flag = false;
         if (this.minecraft.options.prioritizeChunkUpdates != PrioritizeChunkUpdates.NEARBY) {
            if (this.minecraft.options.prioritizeChunkUpdates == PrioritizeChunkUpdates.PLAYER_AFFECTED) {
               flag = chunkrenderdispatcher$renderchunk.isDirtyFromPlayer();
            }
         } else {
            BlockPos blockpos1 = chunkrenderdispatcher$renderchunk.getOrigin().offset(8, 8, 8);
            flag = !net.minecraftforge.common.ForgeConfig.CLIENT.alwaysSetupTerrainOffThread.get() && (blockpos1.distSqr(blockpos) < 768.0D || chunkrenderdispatcher$renderchunk.isDirtyFromPlayer()); // the target is the else block below, so invert the forge addition to get there early
         }

         if (flag) {
            this.minecraft.getProfiler().push("build_near_sync");
            this.chunkRenderDispatcher.rebuildChunkSync(chunkrenderdispatcher$renderchunk, renderregioncache);
            chunkrenderdispatcher$renderchunk.setNotDirty();
            this.minecraft.getProfiler().pop();
         } else {
            list.add(chunkrenderdispatcher$renderchunk);
         }
      }
   }

   this.minecraft.getProfiler().popPush("upload");
   this.chunkRenderDispatcher.uploadAllPendingUploads();
   this.minecraft.getProfiler().popPush("schedule_async_compile");

   for(ChunkRenderDispatcher.RenderChunk chunkrenderdispatcher$renderchunk1 : list) {
      chunkrenderdispatcher$renderchunk1.rebuildChunkAsync(this.chunkRenderDispatcher, renderregioncache);
      chunkrenderdispatcher$renderchunk1.setNotDirty();
   }

   this.minecraft.getProfiler().pop();
}
```

`this.renderChunksInFrustum`的设置在`setupRender`内调用的`applyFrustum`

</details>


其大致内容,是根据当前区块渲染的策略,同步或异步的将`ChunkRenderDispatcher.RenderChunk`进行build的操作  
最终它们都会调用到`ChunkCompileTask#doTask`  
它有两个实现,一个是`RebuildTask`另一个是`ResortTransparencyTask`,抛去其所有线程调度逻辑  

对于前者,最核心的的代码在于

```java
ChunkRenderDispatcher.CompiledChunk compiledChunk = new ChunkRenderDispatcher.CompiledChunk();
Set<BlockEntity> set = this.compile(cameraX, cameraY, cameraZ, compiledChunk, pBuffers);
RenderChunk.this.updateGlobalBlockEntities(set);

List<CompletableFuture<Void>> list = Lists.newArrayList();
compiledChunk.hasLayer.forEach((item : RenderType) -> {
   list.add(ChunkRenderDispatcher.this.uploadChunkLayer(pBuffers.builder(item), RenderChunk.this.getBuffer(item)));
});
```

在`compile`函数内,会对范围内所有的`BlockPos`逐个判定  
并且根据对应坐标内的方块/流体/BlockEntity做出不同的渲染操作  
调用`BlockRenderDispatcher#renderBatched/renderLiquid`,分别对应了`ModelBlockRenderer`与`LiquidBlockRenderer`内的函数  
同时设置传入的`CompiledChunk`的一系列参数  
而返回的`Set<BlockEntity>`则被同步进`ChunkRenderDispatcher.globalBlockEntities`  
同时,如果内部有`translucent`的方块,则会设置`QuadSortOrigin`

而后面的foreach则分别将`BufferBuilder`内的数据上传  

对于后者,它仅在调用`renderChunkLayer`传入的`RenderType`为`translucent`时被立刻执行  
用于重新设置`BufferBuilder`的`QuadSortOrigin`