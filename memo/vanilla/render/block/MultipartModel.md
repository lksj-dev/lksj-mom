# Multipart Model  

原版拥有两种以`BlockState`描述模型的方式,在[wiki](https://minecraft.fandom.com/wiki/Model#Block_states)都有描述  

`Multipart Model`,与`Variants`不同,这种方式可以视为模型在一系列条件下的叠加  
以原版的栅栏为例  

```json
{
  "multipart": [
    {
      "apply": {"model": "minecraft:block/acacia_fence_post"}
    },
    {
      "when": {"north": "true"},
      "apply": {"model": "minecraft:block/acacia_fence_side","uvlock": true}
    },
    {
      "when": {"east": "true"},
      "apply": {"model": "minecraft:block/acacia_fence_side","y": 90,"uvlock": true}
    },
    {
      "when": {"south": "true"},
      "apply": {"model": "minecraft:block/acacia_fence_side","y": 180,"uvlock": true}
    },
    {
      "when": {"west": "true"},
      "apply": {"model": "minecraft:block/acacia_fence_side","y": 270,"uvlock": true}
    }
  ]
}
```

其渲染流程可视为,对一系列`when`进行判断,如果成立,则`叠加/应用/apply`所指定的模型  
当然这这一系列操作并不会发生在渲染时,在模型加载阶段就已经完成  

在这里我们给出一个管道的[例子](https://github.com/MalayPrime/rotarism-decorations/blob/master/src/generated/resources/assets/blockstates/normal_pipe.json)


示例效果:  
![效果](https://zomb-676.github.io/CobaltDocs/picture/blockModel/exampleForMultiPart.png)
