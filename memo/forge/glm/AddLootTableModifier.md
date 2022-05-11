# AddLootTableModifier——用额外的战利品表作为GLM的参数  
基于Minecraft Forge 1.18.2 40.0.44。**低版本内容可能会有所变化。**  
*****  
## `AddLootTableModifier`的起源与发展
&emsp;&emsp;这个类是先由 Commoble 编写，后被 vectorwing 用于农夫乐事的奖励箱修改。具体的出处目前暂不得知，有可能是 Commoble 直接为 vectorwing 编写了这个类也说不定。目前能确定的首次使用是农夫乐事。因为代码简短清晰、可拓展性强、易于使用等优点集于一身，它是GLM的优秀实例之一。本文提供的代码则是由作者一定优化过后的版本。  
*****  
## `AddLootTableModifier`代码
完整代码[^完整代码]如下。
```java
import com.google.gson.JsonObject;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.GsonHelper;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.storage.loot.LootContext;
import net.minecraft.world.level.storage.loot.LootTable;
import net.minecraft.world.level.storage.loot.predicates.LootItemCondition;
import net.minecraftforge.common.loot.GlobalLootModifierSerializer;
import net.minecraftforge.common.loot.LootModifier;
import javax.annotation.Nonnull;
import java.util.List;

public class AddLootTableModifier extends LootModifier {
    private final ResourceLocation lootTable;

    public AddLootTableModifier(LootItemCondition[] conditionsIn, ResourceLocation lootTable) {
        super(conditionsIn);
        this.lootTable = lootTable;
    }

    public boolean canApplyModifier() {
        return true;
    }

    @Nonnull
    @Override
    protected List<ItemStack> doApply(List<ItemStack> generatedLoot, LootContext context) {
        if(this.canApplyModifier()) {
            LootTable extraTable = context.getLootTable(this.lootTable);
            extraTable.getRandomItemsRaw(context, LootTable.createStackSplitter(generatedLoot::add));
        }
        return generatedLoot;
    }

    public static class Serializer extends GlobalLootModifierSerializer<AddLootTableModifier> {
        @Override
        public AddLootTableModifier read(ResourceLocation location, JsonObject object, LootItemCondition[] conditions) {
            ResourceLocation lootTable = new ResourceLocation(GsonHelper.getAsString(object, "lootTable"));
            return new AddLootTableModifier(conditions, lootTable);
        }

        @Override
        public JsonObject write(AddLootTableModifier instance) {
            JsonObject object = this.makeConditions(instance.conditions);
            object.addProperty("lootTable", instance.lootTable.toString());
            return object;
        }
    }
}
```  
&emsp;&emsp;即便无法看懂以上内容**也没有关系**。这个代码是可以直接复制并使用的。这个类也适用于需要数据包生成器的场合，因为我们的序列化器允许我们这样做。

[^完整代码]: 不包括package语句
