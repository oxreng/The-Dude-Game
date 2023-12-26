def sprites_update(sprites, player):
    for sprite in sprites:
        sprite.update()
        if isinstance(sprite, ...):
            sprite.full_update(player)

            if sprite.can_attack(player):
                ....damage()
                ....get_damage(3)

                if not sprite.is_dead:
                    sprite.attack()
                    player.damage(sprite.damage)
            else:
                sprite.stop_attack()
        elif isinstance(sprite, ...):
            if sprite.can_pick(player.pos):
                sprite.pick()
                player.pick(sprite.type)
    return sprites