由于`Capability`的`Tag`是独立于`ItemStack`本身的`Tag`的，所以我们需要手动进行同步。

Forge 提供了一组方法方便同步`Capability`。

```java
/**
 *  用来获取待同步的`Tag`，默认实现为获取`ItemStack`本身的 tag。
 *  注意！如果这里覆写方法没有调用 super，可能会导致`ItemStack`本身的同步失效。 
 */
@Nullable
@Override
public CompoundTag getShareTag(ItemStack stack) {
    // 由于默认实现是 getTag，这里就不判空了，直接使用 stack.getOrCreateTag()
    var result = stack.getOrCreateTag();
    // 获取 capability 的值存入 result，这里拿 ENERGY 举例，因为我的上下文确定这里用的一定是 EnergyStorage 所以直接强转了，可以使用 instaceof INBTSerializable serializable 来判断是否可以直接 serializeNBT
    stack.getCapability(CapabilityEnergy.ENERGY).ifPresent(cap -> {
        result.put("energy", ((EnergyStorage) cap).serializeNBT());
    });
    return result;
}

/** 用来在`Tag`同步后读取的方法。 */
@Override
public void readShareTag(ItemStack stack, @Nullable CompoundTagnbt) {
    super.readShareTag(stack, nbt);
    // 他不太可能是 null，但判空保平安，省得爆了再去找原因
    if (nbt == null) {
        return;
    }
    // 同样，获取 capability 的值。
    stack.getCapability(CapabilityEnergy.ENERGY).ifPresent(cap -> {
        ((EnergyStorage) cap).deserializeNBT(nbt.get("energy"));
    });
}
```