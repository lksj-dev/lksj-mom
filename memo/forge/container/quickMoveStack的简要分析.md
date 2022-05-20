```java
@NotNull
@Override
public ItemStack quickMoveStack(Player playerIn, int index)
{
    //自定义容器的物品槽数量，这里以13为例子
    int customContainerSlotNum = 13;
    ItemStack itemstack = ItemStack.EMPTY;
    Slot slot = this.slots.get(index);
    if(slot != null && slot.hasItem())
    {
        ItemStack stack = slot.getItem();
        itemstack = stack.copy();
        //在这个范围内，都是自定义物品槽，所以要尝试把他们移动到玩家栏
        if(index < customContainerSlotNum)
        {
            //尝试移动到玩家栏，失败则返回空值

            //moveItemStackTo四个参数为：
            //要移动的itemStack
            //移动槽位的起始ID（包含）
            //移动槽位的结束ID（不包含）
            //是否优先移动到ID较大的槽位
            if(!this.moveItemStackTo(stack, customContainerSlotNum, customContainerSlotNum +36, true))
            {
                return ItemStack.EMPTY;
            }
            slot.onQuickCraft(stack, itemstack);
        }
        //在这个范围内，都是玩家栏，所以要尝试把他们移动到自定义物品槽
        else
        {
            //尝试移动到自定义物品槽，失败则尝试在快捷栏和背包之间互相移动
            if(!this.moveItemStackTo(stack, 0, customContainerSlotNum, false))
            {
                //在这个范围内，都是玩家背包，所以要尝试把他们移动到快捷栏
                if(index < customContainerSlotNum + 27)
                {
                    //尝试移动到快捷栏，失败则返回空值
                    if(!this.moveItemStackTo(stack, customContainerSlotNum + 27, customContainerSlotNum + 36, false))
                    {
                        return ItemStack.EMPTY;
                    }
                }
                //尝试移动到玩家背包，失败则返回空值
                else if(index < customContainerSlotNum + 36 && !this.moveItemStackTo(stack, customContainerSlotNum, customContainerSlotNum + 27, false))
                {
                    return ItemStack.EMPTY;
                }
            }
        }

        if(stack.isEmpty())
        {
            slot.set(ItemStack.EMPTY);
        }
        else
        {
            slot.setChanged();
        }

        if(stack.getCount() == itemstack.getCount())
        {
            return ItemStack.EMPTY;
        }

        slot.onTake(playerIn, stack);
    }

    return itemstack;
}
```
