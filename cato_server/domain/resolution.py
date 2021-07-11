import attr


@attr.s
class Resolution:
    width: int = attr.ib(validator=attr.validators.instance_of(int))
    height: int = attr.ib(validator=attr.validators.instance_of(int))

    @width.validator
    def _validate_width(self, attribute, value):
        if value < 0:
            raise ValueError("Width can not be smaller than 0!")

    @height.validator
    def _validate_height(self, attribute, value):
        if value < 0:
            raise ValueError("Height can not be smaller than 0!")

    def __str__(self):
        return f"{self.width}x{self.height}px"
