## Ingredient
```java
JsonElement JsonElement = ...;
//...
Ingredient anIngredient = Ingredient.fromJson(JsonElement);
```
JSON格式参考：https://mcforge.readthedocs.io/en/1.18.x/resources/server/recipes/ingredients

## ItemStack
```java
JsonElement JsonElement = ...;
//...
//第二个boolean参数决定是否读取nbt数据
ItemStack anItemStack = CraftingHelper.getItemStack(JsonElement, true);
```
JSON格式参考：
```json
{
    "item": "minecraft:furnace",
    "count": 1,
    "nbt": {
        "...": "..."
    }
}
```

## NBT
```java
JsonElement JsonElement = ...;
//...
CompoundTag aCompoundTag = CraftingHelper.getNBT(JsonElement);
```

## BlockState
```java
JsonElement JsonElement = ...;
//...
CompoundTag aCompoundTag = CraftingHelper.getNBT(JsonElement);
BlockState aBlockState = NBTUtils.readBlockState(aCompoundTag);
```
JSON格式参考：
```json
{
    "Name": "minecraft:stone",
    "Properties":
    {
        "variant": "granite"
    }
}
```
