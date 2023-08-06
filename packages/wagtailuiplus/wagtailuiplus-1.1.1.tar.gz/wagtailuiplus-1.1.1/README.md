# Wagtail UI Plus

This Wagtail app provides several ui improvements to the Wagtail editor interface.

**Collapsable panels**
- Click on the panel header to collapse/expand the panel
- Set the default collapsed state
- Supported panel types: `MultiFieldPanel` and `StreamFieldPanel`

**StreamField UI improvements**
- Added border around blocks
- Added spacing between blocks
- Permanently visible add buttons
- Use more of the available space for stream blocks

## Compatibility
- Wagtail 2.5+

## Installation

- `pip install wagtailuiplus`
- Add `wagtailuiplus` to your installed apps

## Usage

**Collapsable panels**

The panels automatically become collapsable. To set the initial collapsed state of panels, add the `wagtailuiplus__panel--collapsed` classname to the panel, for example:

```
class HomePage(Page):
    content_panels = [
        MultiFieldPanel([
            FieldPanel('title'),
        ], 'My multi field panel', classname='wagtailuiplus__panel--collapsed'),
    ]
```

![Screenshot](https://raw.githubusercontent.com/davidcondenl/wagtailuiplus/master/screenshot1.png)

**StreamField UI improvements**

The UI improvements automatically apply. Just create your StreamField as usual, for example:

```
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.blocks import (
  CharBlock,
  StreamBlock,
  StructBlock,
  RichTextBlock,
)
from wagtail.core.fields import StreamField
from wagtail.core.models import Page


class MyCharBlock(CharBlock):
    class Meta:
        icon = 'pilcrow'
        label = 'My char block'


class MyRichTextBlock(RichTextBlock):
    class Meta:
        icon = 'openquote'
        label = 'My rich text block'


class MyStreamBlock(StreamBlock):
    title = MyCharBlock()
    text = MyRichTextBlock()

    class Meta:
        label = 'My stream block'


class MyStructBlock(StructBlock):
    items = MyStreamBlock(required=False)

    class Meta:
        icon = 'list-ul'
        label = 'My struct block'


class HomePage(Page):
    my_stream_field = StreamField([
            ('my_title_block', MyCharBlock()),
            ('my_text_block', MyRichTextBlock()),
            ('my_struct_block', MyStructBlock()),
        ], blank=True, verbose_name='My stream field')

    content_panels = [
        StreamFieldPanel('my_stream_field'),
    ]
```
![Screenshot](https://raw.githubusercontent.com/davidcondenl/wagtailuiplus/master/screenshot2.png)
