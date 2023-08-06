from click import Group as ClickGroup


class AliasedGroup(ClickGroup):
    def get_command(self, ctx, cmd_name):
        rv = ClickGroup.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx) if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return ClickGroup.get_command(self, ctx, matches[0])
        ctx.fail("Too many matches: %s" % ", ".join(sorted(matches)))
