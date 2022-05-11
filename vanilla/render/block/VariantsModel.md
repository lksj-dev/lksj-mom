# Variants Model  

原版拥有两种以`BlockState`描述模型的方式,在[wiki](https://minecraft.fandom.com/wiki/Model#Block_states)都有描述

`Variants Block Model`其思路为排列组合枚举所有的`BlockState`,并要求逐一给出对应的模型  
这里以草方块为例,其拥有一个布尔类型的名为snow的BlockState  

首先是`blockState`的文件,blockstates/grass_block.json  

<details>
<summary>blockstates/grass_block.json</summary>

```json
{
  "variants": {
    "snowy=false": [
      {
        "model": "minecraft:block/grass_block"
      },
      {
        "model": "minecraft:block/grass_block",
        "y": 90
      },
      {
        "model": "minecraft:block/grass_block",
        "y": 180
      },
      {
        "model": "minecraft:block/grass_block",
        "y": 270
      }
    ],
    "snowy=true": {
      "model": "minecraft:block/grass_block_snow"
    }
  }
}
```

</details>

然后是模型文件  

#### **block/grass_block.json**

<details>
<summary>models/block/grass_block</summary>

```json
{   "parent": "block/block",
  "textures": {
    "particle": "block/dirt",
    "bottom": "block/dirt",
    "top": "block/grass_block_top",
    "side": "block/grass_block_side",
    "overlay": "block/grass_block_side_overlay"
  },
  "elements": [
    {   "from": [ 0, 0, 0 ],
      "to": [ 16, 16, 16 ],
      "faces": {
        "down":  { "uv": [ 0, 0, 16, 16 ], "texture": "#bottom", "cullface": "down" },
        "up":    { "uv": [ 0, 0, 16, 16 ], "texture": "#top",    "cullface": "up", "tintindex": 0 },
        "north": { "uv": [ 0, 0, 16, 16 ], "texture": "#side",   "cullface": "north" },
        "south": { "uv": [ 0, 0, 16, 16 ], "texture": "#side",   "cullface": "south" },
        "west":  { "uv": [ 0, 0, 16, 16 ], "texture": "#side",   "cullface": "west" },
        "east":  { "uv": [ 0, 0, 16, 16 ], "texture": "#side",   "cullface": "east" }
      }
    },
    {   "from": [ 0, 0, 0 ],
      "to": [ 16, 16, 16 ],
      "faces": {
        "north": { "uv": [ 0, 0, 16, 16 ], "texture": "#overlay", "tintindex": 0, "cullface": "north" },
        "south": { "uv": [ 0, 0, 16, 16 ], "texture": "#overlay", "tintindex": 0, "cullface": "south" },
        "west":  { "uv": [ 0, 0, 16, 16 ], "texture": "#overlay", "tintindex": 0, "cullface": "west" },
        "east":  { "uv": [ 0, 0, 16, 16 ], "texture": "#overlay", "tintindex": 0, "cullface": "east" }
      }
    }
  ]
}

```

</details>

#### **block/grass_block_snow**

```json
{
  "parent": "minecraft:block/cube_bottom_top",
  "textures": {
    "top": "minecraft:block/grass_block_top",
    "bottom": "minecraft:block/dirt",
    "side": "minecraft:block/grass_block_snow",
    "particle": "minecraft:block/dirt"
  }
}
```

#### **item/grass_block**
```json
{
  "parent": "minecraft:block/grass_block"
}
```

这里我们给出一个多阶段作物的[例子](https://github.com/MalayPrime/rotarism-decorations/blob/master/src/generated/resources/assets/blockstates/canola.json)

示例效果  
![效果](https://zomb-676.github.io/CobaltDocs/picture/blockModel/exampleForVariant.png)